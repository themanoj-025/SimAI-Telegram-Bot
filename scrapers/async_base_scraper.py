import warnings

import httpx

from config.config import Config
from utils.logger import setup_logger

warnings.filterwarnings(
    "ignore",
    message=r"urllib3 .* doesn't match a supported version!",
)

logger = setup_logger(__name__)


class AsyncBaseScraper:
    def __init__(self) -> None:
        self.config = Config()
        self.headers = {"User-Agent": "AI Daily Bot/1.0"}

    async def fetch_url(self, url: str, timeout: int | None = None) -> str | None:
        """Fetch a URL asynchronously and return the response body as text."""
        request_timeout = timeout or self.config.REQUEST_TIMEOUT

        async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
            try:
                response = await client.get(url, timeout=request_timeout)
                response.raise_for_status()
                return response.text
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                logger.error(f"Error fetching {url}: {e}")
                return None
