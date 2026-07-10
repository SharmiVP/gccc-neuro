# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import logging
from typing import Any
from typing import Dict
from typing import Union

import requests

# pylint: disable=import-error
from neuro_san.interfaces.coded_tool import CodedTool

# pylint: enable=import-error

logger = logging.getLogger(__name__)

EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"


class DisasterMonitor(CodedTool):
    """
    CodedTool implementation that fetches active climate disaster events from
    the NASA EONET API and filters them by region keyword.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Fetch active disaster events from NASA EONET and filter by region.

        :param args: Expected key: "region" (str) — geographic region to filter events.
        :param sly_data: Supplementary data passed through the agent network (unused here).
        :return: Dictionary containing a list of up to 10 active disaster events for the region,
                 or an error message string.
        """
        region: str = args.get("region", "").strip().lower()

        try:
            response = requests.get(EONET_URL, params={"status": "open"}, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            logger.exception("Failed to fetch EONET data")
            return f"Error fetching disaster data from NASA EONET: {exc}"

        events = data.get("events", [])

        if region:
            filtered = []
            for event in events:
                title_match = region in event.get("title", "").lower()
                geo_match = any(
                    region in str(geo.get("coordinates", "")).lower()
                    for geo in event.get("geometry", [])
                )
                category_match = any(
                    region in cat.get("title", "").lower()
                    for cat in event.get("categories", [])
                )
                if title_match or geo_match or category_match:
                    filtered.append(event)
        else:
            filtered = events

        top_events = filtered[:10]

        results = []
        for event in top_events:
            geometry = event.get("geometry", [])
            latest_geo = geometry[-1] if geometry else {}
            results.append(
                {
                    "id": event.get("id"),
                    "title": event.get("title"),
                    "categories": [c.get("title") for c in event.get("categories", [])],
                    "sources": [s.get("url") for s in event.get("sources", [])],
                    "latest_date": latest_geo.get("date"),
                    "coordinates": latest_geo.get("coordinates"),
                    "magnitude_value": latest_geo.get("magnitudeValue"),
                    "magnitude_unit": latest_geo.get("magnitudeUnit"),
                }
            )

        return {
            "region_filter": region or "global",
            "total_open_events": len(events),
            "matched_events": len(filtered),
            "top_10_events": results,
        }
