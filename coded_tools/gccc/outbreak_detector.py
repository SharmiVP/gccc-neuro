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
from typing import List
from typing import Union

import requests
from bs4 import BeautifulSoup

# pylint: disable=import-error
from neuro_san.interfaces.coded_tool import CodedTool

# pylint: enable=import-error

logger = logging.getLogger(__name__)

WHO_DON_URL = "https://www.who.int/csr/don/en/"


class OutbreakDetector(CodedTool):
    """
    CodedTool implementation that scrapes the WHO Disease Outbreak News page
    and returns active outbreak entries filtered by region keyword.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Scrape WHO Disease Outbreak News and filter results by region.

        :param args: Expected key: "region" (str) — geographic region or country to filter outbreaks.
        :param sly_data: Supplementary data passed through the agent network (unused here).
        :return: Dictionary containing matched outbreak entries, or an error message string.
        """
        region: str = args.get("region", "").strip().lower()

        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; OutbreakDetector/1.0)"}
            response = requests.get(WHO_DON_URL, headers=headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception("Failed to fetch WHO DON page")
            return f"Error fetching WHO Disease Outbreak News: {exc}"

        soup = BeautifulSoup(response.text, "html.parser")
        outbreaks = self._parse_outbreaks(soup)

        if region:
            filtered = [o for o in outbreaks if region in o["title"].lower() or region in o["summary"].lower()]
        else:
            filtered = outbreaks

        return {
            "region_filter": region or "global",
            "total_found": len(outbreaks),
            "matched_outbreaks": len(filtered),
            "outbreaks": filtered,
        }

    def _parse_outbreaks(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Parse outbreak entries from the WHO DON page HTML.

        :param soup: Parsed BeautifulSoup object of the WHO DON page.
        :return: List of outbreak dictionaries with title, date, url, and summary.
        """
        results = []
        base_url = "https://www.who.int"

        # WHO DON uses list items inside an article listing container
        items = soup.select("li.list-view--item") or soup.select("div.sf-content-block")

        # Fallback: find all anchor tags that look like DON links
        if not items:
            anchors = soup.find_all("a", href=lambda h: h and "/csr/don/" in h and h != "/csr/don/en/")
            for anchor in anchors:
                title = anchor.get_text(strip=True)
                href = anchor.get("href", "")
                if title and href:
                    results.append(
                        {
                            "title": title,
                            "date": "",
                            "url": base_url + href if href.startswith("/") else href,
                            "summary": "",
                        }
                    )
            return results

        for item in items:
            anchor = item.find("a")
            if not anchor:
                continue
            title = anchor.get_text(strip=True)
            href = anchor.get("href", "")
            date_tag = item.find(class_=lambda c: c and "date" in c.lower()) if item else None
            date = date_tag.get_text(strip=True) if date_tag else ""
            summary_tag = item.find("p")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            results.append(
                {
                    "title": title,
                    "date": date,
                    "url": base_url + href if href.startswith("/") else href,
                    "summary": summary,
                }
            )

        return results
