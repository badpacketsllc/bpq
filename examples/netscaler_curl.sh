#!/bin/bash
# Citrix NetScaler vulnerability CVE-2019-19781 events detected since
# January 1, 2022.
#
# Author: Mathew Woodyard
# Copyright (C) 2022 Okta, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

curl -H "accept:application/json" -H "Authorization:Token ${BAD_PACKETS_API_TOKEN}" \
  "https://api.badpackets.net/v1/query?last_seen_after=2022-01-01T00%3A00%3A01Z&tags=CVE-2019-19781"
