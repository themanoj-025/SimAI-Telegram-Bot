import asyncio

from services.summarizer import Summarizer


async def test_summarizer() -> None:
    print("\nTesting Summarizer...")
    summarizer = Summarizer()
    articles = [
        {
            "title": "OpenAI announces a new multimodal update",
            "link": "https://example.com/openai",
        },
        {
            "title": "Google DeepMind releases a new robotics model",
            "link": "https://example.com/deepmind",
        },
    ]
    summary = await summarizer.summarize_articles(articles)
    print(f"Summary:\n{summary}")


if __name__ == "__main__":
    asyncio.run(test_summarizer())
