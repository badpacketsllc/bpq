#!/usr/bin/env python3

"""
Bad Packets Cyber Threat Intelligence API CLI entrypoint.

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
import argparse
from datetime import datetime
from datetime import timedelta
import bpq
from bpq.client import BadPacketsHttpApiClient


def main():
    """Main entrypoint function for Bad Packets API tools CLI."""

    parser = argparse.ArgumentParser(
        prog='bpq',
        description='''
            Pulls Bad Packets CTI data.
            All arguments given at the command line can be specified using
            environment variables. For example, a command line option of
            `--output-format csv` is equivalent to setting the environment variable
            `OUTPUT_FORMAT=csv`. Any argument not specified will be populated with
            an environment variable or the default value indicated in `--help`.
            ''',
    )

    parser.add_argument('--bad-packets-api-token', '-t', '--token', type=str,
                        help='Authenticate using this Bad Packets API token.  '
                             'Attempts to read the $BAD_PACKETS_API_TOKEN '
                             'environment variable before evaluating the command '
                             'line option.',
                        default=os.environ.get('BAD_PACKETS_API_TOKEN'))

    parser.add_argument('--output-format', type=str,
                        choices=['csv', 'json', 'CSV', 'JSON'],
                        help='Output results using this format. '
                             'Defaults to CSV format.',
                        default=os.environ.get('OUTPUT_FORMAT', 'csv').lower())

    parser.add_argument('--event_id', '--event-id', type=str,
                        help='Unique event identifier.')

    parser.add_argument('--source_ip_address', '--source-ip-address', type=str,
                        help="Host's IP address.")

    parser.add_argument('--target_port', '--target-port', '--port', type=int,
                        help='Port targeted.')

    parser.add_argument('--protocol', type=str,
                        help='Protocol used.')

    parser.add_argument('--user_agent', '--user-agent', type=str,
                        help='User-Agent used.')

    parser.add_argument('--payload', type=str,
                        help='Payload captured including HTTP Method, URI, and '
                             'request type/version.')

    parser.add_argument('--post_data', '--post-data', type=str,
                        help='POST data captured (when applicable).')

    parser.add_argument('--country', type=str,
                        help='ISO 3166-1 two letter country code.')

    parser.add_argument('--tags', type=str, nargs='+',
                        help='Query for the specified tags. '
                             'Example use specifying one tag: '
                             '`--tags \'Mirai-like Scan\'` '
                             'Example use specifying multiple tags: '
                             '`--tags \'Mirai-like Scan\' \'CVE-2020-0688\'')

    parser.add_argument('--event_count', '--event-count', type=int,
                        help='Count of events detected from a host.')

    parser.add_argument('--time-delta', type=int,
                        help='Pull data from the last `t` minutes. '
                             'Defaults to 60 minutes.',
                        default=60)

    parser.add_argument('--max-results', type=int,
                        help='Return only the first `n` results rather than '
                             'attempting to page through all matches from Bad '
                             'Packets RESTful API. Useful for testing when you '
                             'want quicker API reply times. Attempts to pull '
                             'all results by default.')

    parser.add_argument('--log-level', type=str,
                        choices=['ERROR',
                                 'WARNING',
                                 'DEBUG',
                                 'INFO',
                                 'error',
                                 'warning',
                                 'debug',
                                 'info'],
                        help='Set log level. Defaults to ERROR.',
                        default=os.environ.get('LOG_LEVEL', default='ERROR').upper())

    parser.add_argument('-v', '--version', action='version',
                        version=bpq.__version__)

    args = parser.parse_args()

    bad_packets_http_api_client = BadPacketsHttpApiClient(
        bad_packets_api_token=args.bad_packets_api_token,
        log_level=args.log_level
    )

    # Get current time and deltas
    current_time = datetime.utcnow()
    delta_time = current_time - timedelta(minutes=args.time_delta)
    delta_time = delta_time.isoformat()

    try:
        for tag in args.tags:
            query_params = {key: _ for key, _ in args.__dict__.items()
                            if key != 'tags'}
            bad_packets_http_api_client.query_data(**query_params,
                                                   tags=tag,
                                                   last_seen_after=delta_time)
    except TypeError:
        bad_packets_http_api_client.query_data(**args.__dict__,
                                               last_seen_after=delta_time)

    bad_packets_http_api_client.output_data(output_format=args.output_format)


if __name__ == '__main__':
    main()
