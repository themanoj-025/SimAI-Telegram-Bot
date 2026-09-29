import asyncio

import telegram.error
from telegram import Message, Update
from telegram.constants import ParseMode

from utils.logger import setup_logger

logger = setup_logger(__name__)


def _msg(update: Update) -> Message:
    """Return ``update.message`` — command/message handlers always carry one."""
    assert update.message is not None
    return update.message


# Hard cap for any single message that goes through send_split_message.
# Slightly below Telegram's 4096 limit, matching the existing convention.
MAX_MESSAGE_LENGTH = 4000
# Smallest chunk kept; anything shorter is treated as a hard failure.
MIN_CHUNK_LENGTH = 100

# Pending-per-chat cooldown so burst sends don't trigger Telegram flood errors.
_COOLDOWN_SECONDS = 3.0
_last_sent_at: dict[str, float] = {}


def _rate_limited(chat_id: str) -> bool:
    """Return True if the chat is still inside its cooldown window."""
    now = asyncio.get_event_loop().time()
    last = _last_sent_at.get(chat_id)
    if last is None or (now - last) >= _COOLDOWN_SECONDS:
        _last_sent_at[chat_id] = now
        return False
    return True


async def send_split_message(
    update: Update, text: str | None, parse_mode: str = ParseMode.MARKDOWN
) -> None:
    """
    Splits a long message into multiple parts if it exceeds Telegram's limit (4096 characters).
    Adds a hard max-length check and a warning log when content is silently cut.
    """
    if not text:
        return

    if len(text) > MAX_MESSAGE_LENGTH:
        logger.warning(
            "Content silently truncated: %d chars > hard max %d. "
            "Increase MAX_MESSAGE_LENGTH if longer reports are expected.",
            len(text),
            MAX_MESSAGE_LENGTH,
        )
        text = text[:MAX_MESSAGE_LENGTH]

    if len(text) <= MAX_MESSAGE_LENGTH:
        await _msg(update).reply_text(text, parse_mode=parse_mode)
        return

    # Split by double newline if possible to preserve structure
    parts = []
    current_part = ""

    sections = text.split("\n\n")

    for section in sections:
        if len(current_part) + len(section) + 2 <= MAX_MESSAGE_LENGTH:
            if current_part:
                current_part += "\n\n" + section
            else:
                current_part = section
        else:
            if current_part:
                parts.append(current_part)

            # If a single section is too long, split it by lines
            if len(section) > MAX_MESSAGE_LENGTH:
                lines = section.split("\n")
                temp_part = ""
                for line in lines:
                    if len(temp_part) + len(line) + 1 <= MAX_MESSAGE_LENGTH:
                        if temp_part:
                            temp_part += "\n" + line
                        else:
                            temp_part = line
                    else:
                        parts.append(temp_part)
                        temp_part = line
                current_part = temp_part
            else:
                current_part = section

    if current_part:
        parts.append(current_part)

    for i, part in enumerate(parts):
        if len(part) < MIN_CHUNK_LENGTH:
            logger.warning(
                "Dropping sub-chunk %d (%.0f chars): too small to be useful",
                i,
                len(part),
            )
            continue

        try:
            await _msg(update).reply_text(part, parse_mode=parse_mode)
            if i < len(parts) - 1:
                await asyncio.sleep(0.5)
        except (telegram.error.TelegramError, OSError) as e:
            logger.error(f"Error sending part {i}: {e}")
            # Fallback without markdown if it fails
            try:
                await _msg(update).reply_text(part)
            except (telegram.error.TelegramError, OSError) as e2:
                logger.error(f"Fallback also failed for part {i}: {e2}")


async def send_split_message_to_chat(
    chat_id: str, text: str | None, parse_mode: str = ParseMode.MARKDOWN
) -> None:
    """
    Chat-scoped split-and-send: applies the same hard max + warning, and
    honours a per-chat cooldown to protect against Telegram flood errors.
    """
    if not text:
        return

    if len(text) > MAX_MESSAGE_LENGTH:
        logger.warning(
            "Content silently truncated: %d chars > hard max %d. "
            "Increase MAX_MESSAGE_LENGTH if longer reports are expected.",
            len(text),
            MAX_MESSAGE_LENGTH,
        )
        text = text[:MAX_MESSAGE_LENGTH]

    if _rate_limited(chat_id):
        logger.debug("Skipping chat %s broadcast: cooldown active", chat_id)
        return

    if len(text) <= MAX_MESSAGE_LENGTH:
        await _send_message_to_chat(chat_id, text, parse_mode)
        return

    parts = []
    current_part = ""

    sections = text.split("\n\n")

    for section in sections:
        if len(current_part) + len(section) + 2 <= MAX_MESSAGE_LENGTH:
            if current_part:
                current_part += "\n\n" + section
            else:
                current_part = section
        else:
            if current_part:
                parts.append(current_part)

            if len(section) > MAX_MESSAGE_LENGTH:
                lines = section.split("\n")
                temp_part = ""
                for line in lines:
                    if len(temp_part) + len(line) + 1 <= MAX_MESSAGE_LENGTH:
                        if temp_part:
                            temp_part += "\n" + line
                        else:
                            temp_part = line
                    else:
                        parts.append(temp_part)
                        temp_part = line
                current_part = temp_part
            else:
                current_part = section

    if current_part:
        parts.append(current_part)

    for i, part in enumerate(parts):
        if len(part) < MIN_CHUNK_LENGTH:
            logger.warning(
                "Dropping sub-chunk %d (%.0f chars): too small to be useful", i, len(part)
            )
            continue

        try:
            await _send_message_to_chat(chat_id, part, parse_mode)
            if i < len(parts) - 1:
                await asyncio.sleep(0.5)
        except (telegram.error.TelegramError, OSError) as e:
            logger.error(f"Error sending part {i} to chat {chat_id}: {e}")
            try:
                await _send_message_to_chat(chat_id, part)
            except (telegram.error.TelegramError, OSError) as e2:
                logger.error(f"Fallback also failed for part {i}: {e2}")


async def _send_message_to_chat(
    chat_id: str, text: str, parse_mode: str = ParseMode.MARKDOWN
) -> None:
    """Send a single message to a chat id via the bot."""
    from telegram import Bot

    bot = Bot.get_current()
    if bot is None:
        logger.error("Cannot send to chat %s: no bot available", chat_id)
        return
    await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
