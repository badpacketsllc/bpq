"""
Bad Packets Cyber Threat Intelligence API client. This client queries the Bad
Packets API, reads the results to a `dict` and outputs the results to `stdout`.

Author: Mathew Woodyard
Copyright (C) 2022 Okta, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys
import re
import logging
import json
import csv
import platform
import urllib.request
import urllib.parse
import urllib.error
import bpq


class BadPacketsHttpApiClient:
    """Python client for the Bad Packets Cyber Threat Intelligence API.

    Attributes:
        bad_packets_api_token: token to use when authenticating against the
          Bad Packets Cyber Threat Intelligence API.
        base_url: base URL to use when querying the Bad Packets Cyber Threat
          Intelligence API. Defaults to `https://api.badpackets.net/v1/query?`.
        __rest_api_fields: list of valid fields .
          See https://docs.badpackets.net/ for an up-to-date list of all availbale parameters.
        result_dict: dictionary with the results from the last query against
          the Bad Packets Cyber Threat Intelligence API.
        __platform__: API client's platform.
        request_headers: HTTP headers used in the client's HTTP request.

    To use:
    In [1]: # Import the API client and libraries needed to set constants
   ...: from bpq.client import BadPacketsHttpApiClient
   ...: import os

    In [3]: # Pull API token from environment variables.
    ...: # You can set this however you like, but it's best not to
    ...: # keep secrets in code.
    ...: BAD_PACKETS_API_TOKEN = os.environ.get('BAD_PACKETS_API_TOKEN')

    In [4]: bad_packets_http_api_client = BadPacketsHttpApiClient(BAD_PACKETS_API_TOKEN)

    In [5]: bad_packets_http_api_client.query_data(source_ip_address='80.82.65.234')

    In [6]: bad_packets_http_api_client.result_dict['results'][0]
    Out [6]:
    {'event_id': '22258c1d94d6b536d75e7a910e922b43fe00f21ea0f048c73f002b67ab4f4faa',
     'source_ip_address': '80.82.65.234' # results truncated
    }
    """

    def __init__(self,
                 bad_packets_api_token=os.environ.get('BAD_PACKETS_API_TOKEN'),
                 base_url='https://api.badpackets.net/v1/query?',
                 log_level='ERROR'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=log_level.upper())

        try:
            if re.search(r'\w+', bad_packets_api_token):
                self.bad_packets_api_token = bad_packets_api_token
            else:
                raise ValueError
        except (ValueError, TypeError):
            self.logger.error(
                'API token cannot be empty. Make sure that either the '
                '`$BAD_PACKETS_API_TOKEN` environment variable is set or '
                '`--bad-packets-api-token` is specified and that you have an '
                'active subscription. '
                'See `bpq --help` and https://docs.badpackets.net/ for more.'
            )
            sys.exit(1)

        self.base_url = base_url
        self.__rest_api_fields = [
            'event_id',
            'source_ip_address',
            'target_port',
            'protocol',
            'user_agent',
            'payload',
            'post_data',
            'country',
            'first_seen_before',
            'first_seen_after',
            'last_seen_before',
            'last_seen_after',
            'tags',
            'event_count',
            'limit',
            'offset',
            'ordering',
        ]

        self.result_dict = {'count': 0,
                            'results': [{}]}

        self.__platform__ = platform.platform()

        self.request_headers = {
            'Authorization': f'Token {self.bad_packets_api_token}',
            'User-Agent': f'Bad Packets ETL script/{bpq.__version__} ({self.__platform__})'
        }

    def query_data(self, max_results=None, **kwargs):
        """Queries data using any supported parameter
        (see https://docs.badpackets.net/#operation/query) specified as
        arguments to the method.

        Example:
            # Queries the Bad Packets REST API for malicious traffic observed
            # from 80.82.65.234 seen after 2020-03-31T17:58:50Z
            bad_packets_http_api_client.query_data(source_ip_address='80.82.65.234',
                                                   last_seen_after='2020-03-31T17:58:50Z')
        """
        params = {key: value for key, value in kwargs.items()
                  if key in self.__rest_api_fields and value is not None}
        if max_results:
            params['limit'] = max_results
        query_parameters = urllib.parse.urlencode(params)
        request_url = f'{self.base_url}{query_parameters}'
        self.logger.info('Querying API using the url %s '
                         'and parameters %s.', request_url, query_parameters)

        request = urllib.request.Request(request_url,
                                         headers=self.request_headers)

        try:
            with urllib.request.urlopen(request) as r:
                result = json.loads(r.read())
                self.result_dict = {'count': result['count'],
                                    'results': result['results']}
                if max_results is None:
                    max_results = self.result_dict['count']
                while result['next'] and \
                        len(self.result_dict['results']) < max_results:
                    request = urllib.request.Request(
                        result['next'],
                        headers=self.request_headers
                    )
                    with urllib.request.urlopen(request) as next_r:
                        result = json.loads(next_r.read())
                        self.result_dict['results'] += result['results']
        except urllib.error.HTTPError as e:
            if e.code == 403:
                self.logger.error(
                    'Caught %s. '
                    'Make sure that either the `$BAD_PACKETS_API_TOKEN` '
                    'environment variable is set or `--bad-packets-api-token` '
                    'is specified and that you have an active subscription. '
                    'See `bpq --help` and https://docs.badpackets.net/ for '
                    'more.',
                    e
                )

    def output_data(self, output_format='csv'):
        """Prints result data to stdout."""
        output_format = output_format.lower()
        self.logger.info('Printing results to `stdout` in %s format', output_format)
        if output_format == 'json':
            print(json.dumps(self.result_dict))
        elif output_format == 'csv':
            result_list = self.result_dict['results']
            try:
                header = result_list[0].keys()
            except IndexError as e:
                self.logger.debug('The API returned no results, printing an '
                                  'empty line. Caught %s.', e)
                header = []
            writer = csv.DictWriter(sys.stdout,
                                    header,
                                    dialect='unix')
            try:
                writer.writeheader()
                for item in result_list:
                    writer.writerow(item)
            except IOError:
                # this line needed because programs like `head` might close the
                # `stdout` pipe before python does.
                pass
