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

# pylint: disable=import-error
from neuro_san.interfaces.coded_tool import CodedTool

# pylint: enable=import-error

logger = logging.getLogger(__name__)

# IPC Phase labels per the Integrated Food Security Phase Classification standard
IPC_LABELS = {
    1: "Minimal",
    2: "Stressed",
    3: "Crisis",
    4: "Emergency",
    5: "Famine / Catastrophe",
}

# Static IPC reference data. Sources: IPC/CH reports, FEWS NET, WFP (2024–2025 estimates).
IPC_DATA: Dict[str, Dict[str, Any]] = {
    "somalia": {
        "ipc_phase": 4,
        "population_at_risk": 4_300_000,
        "primary_drivers": ["prolonged drought", "conflict", "displacement", "market disruption"],
        "alert_level": "critical",
    },
    "sudan": {
        "ipc_phase": 5,
        "population_at_risk": 8_000_000,
        "primary_drivers": ["armed conflict", "displacement", "collapsed health system", "flooding"],
        "alert_level": "famine declared",
    },
    "yemen": {
        "ipc_phase": 4,
        "population_at_risk": 17_100_000,
        "primary_drivers": ["protracted conflict", "economic collapse", "import dependency", "currency devaluation"],
        "alert_level": "critical",
    },
    "ethiopia": {
        "ipc_phase": 4,
        "population_at_risk": 15_800_000,
        "primary_drivers": ["drought (El Niño)", "Tigray conflict aftermath", "displacement", "poor harvest"],
        "alert_level": "critical",
    },
    "myanmar": {
        "ipc_phase": 3,
        "population_at_risk": 13_300_000,
        "primary_drivers": ["military conflict", "economic crisis", "displacement", "restricted humanitarian access"],
        "alert_level": "serious",
    },
    "haiti": {
        "ipc_phase": 4,
        "population_at_risk": 5_400_000,
        "primary_drivers": ["gang violence", "political instability", "supply chain collapse", "displacement"],
        "alert_level": "critical",
    },
    "afghanistan": {
        "ipc_phase": 4,
        "population_at_risk": 14_600_000,
        "primary_drivers": ["economic collapse", "drought", "frozen assets", "restricted aid access"],
        "alert_level": "critical",
    },
    "drc": {
        "ipc_phase": 4,
        "population_at_risk": 25_800_000,
        "primary_drivers": ["armed conflict (eastern DRC)", "displacement", "cholera", "limited infrastructure"],
        "alert_level": "critical",
    },
    "nigeria": {
        "ipc_phase": 3,
        "population_at_risk": 26_500_000,
        "primary_drivers": ["Boko Haram insurgency (northeast)", "flooding", "inflation", "displacement"],
        "alert_level": "serious",
    },
}


class FamineRiskAssessor(CodedTool):
    """
    CodedTool implementation that returns IPC-based famine risk assessments
    for high-risk countries using a static reference dataset.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Return famine risk data for a given region using the static IPC lookup.

        :param args: Expected key: "region" (str) — country or region name to look up.
        :param sly_data: Supplementary data passed through the agent network (unused here).
        :return: Dictionary with ipc_phase, ipc_label, population_at_risk, primary_drivers,
                 and alert_level, or a not-found message with the list of covered countries.
        """
        region: str = args.get("region", "").strip().lower()

        # Try exact match first, then partial match
        match = IPC_DATA.get(region)
        if match is None:
            for key, value in IPC_DATA.items():
                if region and (region in key or key in region):
                    match = value
                    region = key
                    break

        if match is None:
            covered = sorted(IPC_DATA.keys())
            return {
                "region_filter": args.get("region", ""),
                "status": "not_found",
                "message": (
                    f"No IPC data available for '{args.get('region', '')}'. "
                    f"Covered countries: {', '.join(covered)}."
                ),
                "covered_countries": covered,
            }

        ipc_phase = match["ipc_phase"]
        return {
            "region": region,
            "ipc_phase": ipc_phase,
            "ipc_label": IPC_LABELS.get(ipc_phase, "Unknown"),
            "population_at_risk": match["population_at_risk"],
            "primary_drivers": match["primary_drivers"],
            "alert_level": match["alert_level"],
            "data_note": "Static reference data based on IPC/CH reports and FEWS NET (2024–2025 estimates).",
        }
