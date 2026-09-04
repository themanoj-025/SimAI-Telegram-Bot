import asyncio

import pytest

from services.report_generator import ReportGenerator

pytestmark = pytest.mark.integration


async def test_all_categories() -> None:
    generator = ReportGenerator()
    categories = [
        "tools",
        "jobs",
        "startups",
        "models",
        "trending",
        "learn",
        "news",
        "papers",
        "blogs",
        "india",
        "youtube",
        "twitter",
    ]

    try:
        for category in categories:
            print(f"Testing category: {category}...")
            try:
                report = await generator.generate_report(category, force_refresh=True)
                if "No updates available" in report or "Invalid category" in report:
                    print(f"  [-] {category}: returned an empty report")
                else:
                    print(f"  [+] {category}: working")
            except (RuntimeError, OSError, ValueError) as e:
                print(f"  [!] {category}: exception - {e}")
    finally:
        await generator.cleanup()


if __name__ == "__main__":
    asyncio.run(test_all_categories())
