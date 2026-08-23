import asyncio

from telegram import Update
from telegram.constants import ParseMode

from utils.logger import setup_logger

logger = setup_logger(__name__)


async def send_split_message(update: Update, text: str, parse_mode: str = ParseMode.MARKDOWN) -> None:
    """
    Splits a long message into multiple parts if it exceeds Telegram's limit (4096 characters).
    """
    if not text:
        return

    MAX_LENGTH = 4000  # Slightly less than 4096 to be safe

    if len(text) <= MAX_LENGTH:
        await update.message.reply_text(text, parse_mode=parse_mode)
        return

    # Split by double newline if possible to preserve structure
    parts = []
    current_part = ""

    # Split by sections (usually separated by double newlines or headers)
    sections = text.split("\n\n")

    for section in sections:
        if len(current_part) + len(section) + 2 <= MAX_LENGTH:
            if current_part:
                current_part += "\n\n" + section
            else:
                current_part = section
        else:
            if current_part:
                parts.append(current_part)

            # If a single section is too long, split it by lines
            if len(section) > MAX_LENGTH:
                lines = section.split("\n")
                temp_part = ""
                for line in lines:
                    if len(temp_part) + len(line) + 1 <= MAX_LENGTH:
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
        try:
            # Re-apply Markdown to each part (might need care if a tag is split)
            # Simple approach: ensure each part is valid markdown
            await update.message.reply_text(part, parse_mode=parse_mode)
            # Small delay to prevent rate limit issues
            if i < len(parts) - 1:
                await asyncio.sleep(0.5)
        except (telegram.error.TelegramError, OSError) as e:
            logger.error(f"Error sending part {i}: {e}")
            # Fallback without markdown if it fails
            await update.message.reply_text(part)
