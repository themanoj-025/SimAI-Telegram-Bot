import asyncio
import warnings

from config.config import Config
from utils.logger import setup_logger

warnings.filterwarnings(
    "ignore",
    message=r"urllib3 .* doesn't match a supported version!",
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    import google.generativeai as genai

logger = setup_logger(__name__)


class Summarizer:
    def __init__(self):
        self.config = Config()
        self.gemini_key = self.config.GEMINI_API_KEY

        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
            logger.info("Gemini AI summarizer initialized.")
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not found. Falling back to simple summaries.")

    async def summarize_articles(self, articles):
        if not articles:
            return "No articles are available to summarize right now."

        if not self.model:
            logger.warning("Gemini model unavailable; using simple summary fallback.")
            return self.get_simple_summary(articles)

        try:
            content = "\n".join(f"- {a['title']}: {a['link']}" for a in articles)
            prompt = (
                "Summarize the following AI news articles into a concise daily "
                "briefing (max 300 words). Focus on the most important "
                "breakthroughs and trends. Use bullet points for readability:\n\n"
                f"{content}"
            )

            response = await asyncio.wait_for(
                self.model.generate_content_async(prompt),
                timeout=8,
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating summary: {type(e).__name__}: {e}")
            return self.get_simple_summary(articles)

    def get_simple_summary(self, articles):
        """Fallback: just list titles if LLM is unavailable."""
        summary = "*Today's Top AI Stories:*\n\n"
        for i, article in enumerate(articles[:10], 1):
            summary += f"{i}. {article['title']}\n"
        return summary
