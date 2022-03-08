#!/bin/bash
# Citrix NetScaler vulnerability CVE-2019-19781 events detected since
# January 1, 2022.
#
# Author: Mathew Woodyard
# Copyright (C) 2020-2022 Bad Packets, LLC ("Bad Packets")
# https://www.badpackets.net
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

curl -H "accept:application/json" -H "Authorization:Token ${BAD_PACKETS_API_TOKEN}" \
  "https://api.badpackets.net/v1/query?last_seen_after=2022-01-01T00%3A00%3A01Z&tags=CVE-2019-19781"
