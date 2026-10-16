"""Central emoji registry for FriendBot.

Custom application emojis are configured by their exact Discord emoji name and ID.
If an ID is blank or invalid, the registry falls back to a Unicode emoji so the bot
continues to work before custom emojis are configured.
"""
from __future__ import annotations

import os
import re

DEFAULT_EMOJIS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "box": "📦",
    "type": "🧩",
    "tier": "🏆",
    "country": "🌍",
    "source": "📥",
    "report": "🚨",
    "owner": "👑",
    "loading": "⏳",
    "database": "🗃️",
    "ping": "🏓",
}


def emoji(key: str) -> str:
    """Return custom emoji markup when configured, otherwise a Unicode fallback.

    Configure e.g. EMOJI_SUCCESS_NAME=success and EMOJI_SUCCESS_ID=123456789012345678.
    For animated emojis, also set EMOJI_SUCCESS_ANIMATED=true.
    The emoji name and ID must match an emoji owned by/available to the application.
    """
    normalized_key = re.sub(r"[^A-Z0-9]", "_", str(key).upper()).strip("_")
    fallback = DEFAULT_EMOJIS.get(str(key).lower(), "✨")
    name = os.getenv(f"EMOJI_{normalized_key}_NAME", "").strip()
    raw_id = os.getenv(f"EMOJI_{normalized_key}_ID", "").strip()
    animated = os.getenv(f"EMOJI_{normalized_key}_ANIMATED", "false").strip().lower() in {
        "1", "true", "yes", "y"
    }

    if not name or not raw_id or not raw_id.isdigit() or int(raw_id) <= 0:
        return fallback

    prefix = "a" if animated else ""
    return f"<{prefix}:{name}:{raw_id}>"


# Convenient registry for code that needs several emoji values at once.
EMOJIS = {key: emoji(key) for key in DEFAULT_EMOJIS}
