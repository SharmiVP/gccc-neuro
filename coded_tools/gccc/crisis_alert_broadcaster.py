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

# pylint: disable=import-error
from neuro_san.interfaces.coded_tool import CodedTool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# pylint: enable=import-error

logger = logging.getLogger(__name__)

SEVERITY_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
}

DEFAULT_CHANNEL = "#crisis-alerts"


class CrisisAlertBroadcaster(CodedTool):
    """
    CodedTool implementation that broadcasts a formatted crisis alert to a
    Slack channel using the Slack WebClient.

    If SLACK_BOT_TOKEN is not configured, returns a message_preview dict
    instead of raising an error, allowing the agent network to continue.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Post a crisis alert to Slack.

        :param args: Expected keys:
            - "summary" (str): Brief description of the crisis situation.
            - "severity" (str): One of CRITICAL, HIGH, MEDIUM, LOW (case-insensitive).
            - "region" (str): Affected geographic region.
            - "action_plan" (str): Recommended immediate actions.
        :param sly_data: Supplementary data passed through the agent network (unused here).
        :return: Dictionary confirming the Slack post (with ts and channel), or a
                 message_preview dict if no token is configured, or an error string.
        """
        summary: str = args.get("summary", "No summary provided.")
        severity: str = args.get("severity", "MEDIUM").strip()
        region: str = args.get("region", "Unknown region")
        action_plan: str = args.get("action_plan", "No action plan provided.")

        token: str = os.environ.get("SLACK_BOT_TOKEN", "").strip()
        channel: str = os.environ.get("SLACK_CRISIS_CHANNEL", DEFAULT_CHANNEL).strip()

        severity_key = severity.lower()
        emoji = SEVERITY_EMOJI.get(severity_key, "⚪")
        severity_label = severity.upper()

        blocks = self._build_blocks(emoji, severity_label, region, summary, action_plan)
        fallback_text = f"{emoji} [{severity_label}] Crisis Alert — {region}: {summary}"

        if not token:
            logger.warning(
                "SLACK_BOT_TOKEN not set. Returning message preview without posting to Slack."
            )
            return {
                "status": "not_sent",
                "reason": "SLACK_BOT_TOKEN environment variable is not configured.",
                "message_preview": {
                    "channel": channel,
                    "text": fallback_text,
                    "blocks": blocks,
                },
            }

        client = WebClient(token=token)
        try:
            response = client.chat_postMessage(
                channel=channel,
                text=fallback_text,
                blocks=blocks,
            )
            logger.info("Crisis alert posted to Slack channel '%s' (ts=%s).", channel, response["ts"])
            return {
                "status": "sent",
                "channel": response["channel"],
                "ts": response["ts"],
                "severity": severity_label,
                "region": region,
            }
        except SlackApiError as exc:
            error_msg = exc.response.get("error", str(exc))
            logger.exception("Slack API error when posting crisis alert")
            return f"Failed to post crisis alert to Slack: {error_msg}"

    def _build_blocks(
        self,
        emoji: str,
        severity_label: str,
        region: str,
        summary: str,
        action_plan: str,
    ) -> list:
        """
        Build the Slack Block Kit payload for the crisis alert message.

        :param emoji: Severity emoji character.
        :param severity_label: Upper-cased severity string.
        :param region: Affected region name.
        :param summary: Crisis summary text.
        :param action_plan: Recommended actions text.
        :return: List of Slack Block Kit block dicts.
        """
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} CRISIS ALERT — {severity_label}",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Region:*\n{region}"},
                    {"type": "mrkdwn", "text": f"*Severity:*\n{emoji} {severity_label}"},
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Crisis Summary:*\n{summary}",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Recommended Action Plan:*\n{action_plan}",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "_Broadcast by the Global Crisis Command Center (GCCC) agent network._",
                    }
                ],
            },
        ]
