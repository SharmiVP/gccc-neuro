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
import os
from typing import Any
from typing import Dict
from typing import Union

import requests

# pylint: disable=import-error
from neuro_san.interfaces.coded_tool import CodedTool

# pylint: enable=import-error

logger = logging.getLogger(__name__)

ACLED_API_URL = "https://api.acleddata.com/acled/read"

# Static conflict reference data. Sources: ACLED, UNHCR, OCHA (2024–2025 estimates).
CONFLICT_DATA: Dict[str, Dict[str, Any]] = {
    "sudan": {
        "conflict_intensity": "extreme",
        "displaced_persons": 10_700_000,
        "escalation_trend": "escalating",
        "humanitarian_access": "severely restricted",
        "active_parties": ["SAF", "RSF"],
        "primary_conflict_type": "civil war",
    },
    "ukraine": {
        "conflict_intensity": "extreme",
        "displaced_persons": 6_500_000,
        "escalation_trend": "ongoing",
        "humanitarian_access": "partially restricted",
        "active_parties": ["Ukrainian Armed Forces", "Russian Armed Forces"],
        "primary_conflict_type": "interstate war",
    },
    "myanmar": {
        "conflict_intensity": "high",
        "displaced_persons": 2_600_000,
        "escalation_trend": "escalating",
        "humanitarian_access": "severely restricted",
        "active_parties": ["Tatmadaw (SAC)", "resistance forces (PDF, EAOs)"],
        "primary_conflict_type": "civil war",
    },
    "drc": {
        "conflict_intensity": "high",
        "displaced_persons": 6_900_000,
        "escalation_trend": "escalating",
        "humanitarian_access": "restricted",
        "active_parties": ["FARDC", "M23 / RDF", "various armed groups"],
        "primary_conflict_type": "multi-party armed conflict",
    },
    "somalia": {
        "conflict_intensity": "high",
        "displaced_persons": 3_800_000,
        "escalation_trend": "volatile",
        "humanitarian_access": "restricted",
        "active_parties": ["Somali National Army", "Al-Shabaab"],
        "primary_conflict_type": "insurgency",
    },
    "ethiopia": {
        "conflict_intensity": "medium",
        "displaced_persons": 4_400_000,
        "escalation_trend": "declining (post-Tigray ceasefire)",
        "humanitarian_access": "improving but patchy",
        "active_parties": ["ENDF", "Fano militia", "OLA"],
        "primary_conflict_type": "multiple sub-national conflicts",
    },
    "yemen": {
        "conflict_intensity": "high",
        "displaced_persons": 4_500_000,
        "escalation_trend": "volatile (Houthi Red Sea escalation)",
        "humanitarian_access": "severely restricted",
        "active_parties": ["Houthis (Ansar Allah)", "Presidential Leadership Council forces"],
        "primary_conflict_type": "civil war with regional dimensions",
    },
    "haiti": {
        "conflict_intensity": "high",
        "displaced_persons": 700_000,
        "escalation_trend": "escalating",
        "humanitarian_access": "severely restricted",
        "active_parties": ["Viv Ansanm gang coalition", "Haitian National Police"],
        "primary_conflict_type": "gang violence / state fragility",
    },
    "afghanistan": {
        "conflict_intensity": "medium",
        "displaced_persons": 3_200_000,
        "escalation_trend": "stable but fragile",
        "humanitarian_access": "restricted (Taliban restrictions on aid workers)",
        "active_parties": ["Taliban (IEA)", "ISKP"],
        "primary_conflict_type": "insurgency / occupation",
    },
    "nigeria": {
        "conflict_intensity": "medium",
        "displaced_persons": 2_200_000,
        "escalation_trend": "volatile",
        "humanitarian_access": "restricted (northeast)",
        "active_parties": ["Nigerian Armed Forces", "Boko Haram / ISWAP", "Bandits"],
        "primary_conflict_type": "multi-front insurgency",
    },
    "palestine": {
        "conflict_intensity": "extreme",
        "displaced_persons": 1_900_000,
        "escalation_trend": "ongoing",
        "humanitarian_access": "critically restricted",
        "active_parties": ["Israeli Defence Forces", "Hamas", "other armed groups"],
        "primary_conflict_type": "armed conflict / occupation",
    },
}


class ConflictMonitor(CodedTool):
    """
    CodedTool implementation that monitors active armed conflicts.
    Attempts to query the ACLED API using credentials from environment variables
    (ACLED_API_KEY and ACLED_EMAIL); falls back to a static conflict reference
    dataset when credentials are unavailable or the request fails.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Return conflict intelligence for a given region.

        Tries ACLED API first; falls back to static data if unavailable.

        :param args: Expected key: "region" (str) — country or region name.
        :param sly_data: Supplementary data passed through the agent network (unused here).
        :return: Dictionary with conflict_intensity, displaced_persons, escalation_trend,
                 humanitarian_access, and source, or an error message string.
        """
        region: str = args.get("region", "").strip()

        acled_key = os.environ.get("ACLED_API_KEY", "").strip()
        acled_email = os.environ.get("ACLED_EMAIL", "").strip()

        if acled_key and acled_email:
            result = self._fetch_acled(region, acled_key, acled_email)
            if result is not None:
                return result

        return self._static_lookup(region)

    def _fetch_acled(
        self, region: str, api_key: str, email: str
    ) -> Union[Dict[str, Any], None]:
        """
        Query the ACLED API for recent conflict events in the given region.

        :param region: Country or region name to filter events.
        :param api_key: ACLED API key.
        :param email: Registered ACLED email address.
        :return: Formatted result dict on success, None on failure.
        """
        params = {
            "key": api_key,
            "email": email,
            "country": region,
            "limit": 50,
            "fields": "event_date|event_type|sub_event_type|actor1|actor2|country|location|fatalities|notes",
        }
        try:
            response = requests.get(ACLED_API_URL, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            logger.warning("ACLED API request failed for region '%s'; falling back to static data.", region)
            return None

        events = data.get("data", [])
        if not events:
            logger.info("No ACLED events returned for region '%s'; falling back to static data.", region)
            return None

        total_fatalities = sum(int(e.get("fatalities", 0) or 0) for e in events)
        event_types = list({e.get("event_type", "") for e in events if e.get("event_type")})
        actors = list({e.get("actor1", "") for e in events if e.get("actor1")})

        return {
            "region": region,
            "source": "ACLED API (live)",
            "events_retrieved": len(events),
            "total_fatalities_in_sample": total_fatalities,
            "event_types_observed": event_types,
            "active_actors": actors[:10],
            "conflict_intensity": self._estimate_intensity(total_fatalities, len(events)),
            "displaced_persons": "See UNHCR for displacement figures",
            "escalation_trend": "See latest ACLED trend reports",
            "humanitarian_access": "See OCHA for humanitarian access status",
        }

    def _estimate_intensity(self, fatalities: int, event_count: int) -> str:
        """Estimate conflict intensity from fatality and event counts in the sample."""
        if fatalities > 500 or event_count > 30:
            return "extreme"
        if fatalities > 100 or event_count > 15:
            return "high"
        if fatalities > 20 or event_count > 5:
            return "medium"
        return "low"

    def _static_lookup(self, region: str) -> Dict[str, Any]:
        """
        Return conflict data from the static reference dictionary.

        :param region: Country or region name to look up.
        :return: Conflict data dict, or a not-found dict listing covered regions.
        """
        key = region.strip().lower()
        match = CONFLICT_DATA.get(key)

        if match is None:
            for ckey, value in CONFLICT_DATA.items():
                if key and (key in ckey or ckey in key):
                    match = value
                    key = ckey
                    break

        if match is None:
            covered = sorted(CONFLICT_DATA.keys())
            return {
                "region_filter": region,
                "source": "static reference data (fallback)",
                "status": "not_found",
                "message": (
                    f"No conflict data available for '{region}'. "
                    f"Covered regions: {', '.join(covered)}."
                ),
                "covered_regions": covered,
            }

        return {
            "region": key,
            "source": "static reference data (ACLED / UNHCR / OCHA 2024–2025 estimates)",
            "conflict_intensity": match["conflict_intensity"],
            "displaced_persons": match["displaced_persons"],
            "escalation_trend": match["escalation_trend"],
            "humanitarian_access": match["humanitarian_access"],
            "active_parties": match.get("active_parties", []),
            "primary_conflict_type": match.get("primary_conflict_type", ""),
        }
