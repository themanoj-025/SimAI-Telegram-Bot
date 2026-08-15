"""Static fallback content used when live sources are unavailable."""


FALLBACK_CONTENT: dict[str, list[dict[str, str]]] = {
    "news": [
        {
            "title": "OpenAI newsroom and product updates",
            "link": "https://openai.com/news/",
            "source": "OpenAI",
            "published": "",
        },
        {
            "title": "Google DeepMind research highlights",
            "link": "https://deepmind.google/discover/blog/",
            "source": "Google DeepMind",
            "published": "",
        },
        {
            "title": "Anthropic company announcements and research notes",
            "link": "https://www.anthropic.com/news",
            "source": "Anthropic",
            "published": "",
        },
        {
            "title": "NVIDIA AI platform and model ecosystem updates",
            "link": "https://blogs.nvidia.com/blog/category/ai/",
            "source": "NVIDIA",
            "published": "",
        },
        {
            "title": "Hugging Face community and open model news",
            "link": "https://huggingface.co/blog",
            "source": "Hugging Face",
            "published": "",
        },
    ],
    "arxiv": [
        {
            "title": "arXiv AI feed for new artificial intelligence papers",
            "link": "https://arxiv.org/list/cs.AI/recent",
            "source": "arXiv",
            "published": "",
        },
        {
            "title": "arXiv machine learning feed for current research",
            "link": "https://arxiv.org/list/cs.LG/recent",
            "source": "arXiv",
            "published": "",
        },
        {
            "title": "arXiv natural language processing feed",
            "link": "https://arxiv.org/list/cs.CL/recent",
            "source": "arXiv",
            "published": "",
        },
        {
            "title": "arXiv computer vision feed",
            "link": "https://arxiv.org/list/cs.CV/recent",
            "source": "arXiv",
            "published": "",
        },
        {
            "title": "Papers With Code trending research",
            "link": "https://paperswithcode.com/trending",
            "source": "Papers With Code",
            "published": "",
        },
    ],
    "blogs": [
        {
            "title": "OpenAI blog",
            "link": "https://openai.com/blog",
            "source": "OpenAI",
            "published": "",
        },
        {
            "title": "NVIDIA technical blog",
            "link": "https://developer.nvidia.com/blog/",
            "source": "NVIDIA",
            "published": "",
        },
        {
            "title": "Hugging Face blog",
            "link": "https://huggingface.co/blog",
            "source": "Hugging Face",
            "published": "",
        },
        {
            "title": "Google DeepMind blog",
            "link": "https://deepmind.google/discover/blog/",
            "source": "Google DeepMind",
            "published": "",
        },
        {
            "title": "Anthropic news and product updates",
            "link": "https://www.anthropic.com/news",
            "source": "Anthropic",
            "published": "",
        },
    ],
    "tools": [
        {
            "title": "Futurepedia directory of AI tools",
            "link": "https://www.futurepedia.io/",
            "source": "Futurepedia",
            "published": "",
        },
        {
            "title": "Hugging Face Spaces for live AI apps",
            "link": "https://huggingface.co/spaces",
            "source": "Hugging Face",
            "published": "",
        },
        {
            "title": "Product Hunt AI collection",
            "link": "https://www.producthunt.com/topics/artificial-intelligence",
            "source": "Product Hunt",
            "published": "",
        },
        {
            "title": "GitHub topic page for AI projects",
            "link": "https://github.com/topics/artificial-intelligence",
            "source": "GitHub",
            "published": "",
        },
        {
            "title": "OpenAI API platform for building AI products",
            "link": "https://platform.openai.com/",
            "source": "OpenAI",
            "published": "",
        },
    ],
    "jobs": [
        {
            "title": "AI Jobs curated board",
            "link": "https://ai-jobs.net/",
            "source": "AI Jobs",
            "published": "",
        },
        {
            "title": "Remote OK AI roles",
            "link": "https://remoteok.com/remote-ai-jobs",
            "source": "Remote OK",
            "published": "",
        },
        {
            "title": "We Work Remotely AI category",
            "link": "https://weworkremotely.com/remote-jobs/search?term=ai",
            "source": "We Work Remotely",
            "published": "",
        },
        {
            "title": "Hugging Face careers",
            "link": "https://huggingface.co/jobs",
            "source": "Hugging Face",
            "published": "",
        },
        {
            "title": "Anthropic careers",
            "link": "https://www.anthropic.com/careers",
            "source": "Anthropic",
            "published": "",
        },
    ],
    "startups": [
        {
            "title": "TechCrunch AI startup coverage",
            "link": "https://techcrunch.com/category/artificial-intelligence/",
            "source": "TechCrunch",
            "published": "",
        },
        {
            "title": "Crunchbase AI startup lists",
            "link": "https://www.crunchbase.com/lists/artificial-intelligence-companies",
            "source": "Crunchbase",
            "published": "",
        },
        {
            "title": "Y Combinator companies tagged with AI",
            "link": "https://www.ycombinator.com/companies?tags=AI",
            "source": "Y Combinator",
            "published": "",
        },
        {
            "title": "Inc42 startup coverage for AI in India",
            "link": "https://inc42.com/tag/artificial-intelligence/",
            "source": "Inc42",
            "published": "",
        },
        {
            "title": "YourStory startup and funding coverage",
            "link": "https://yourstory.com/tag/artificial-intelligence",
            "source": "YourStory",
            "published": "",
        },
    ],
    "models": [
        {
            "title": "OpenAI model release notes",
            "link": "https://platform.openai.com/docs/models",
            "source": "OpenAI",
            "published": "",
        },
        {
            "title": "Google Gemini model overview",
            "link": "https://deepmind.google/technologies/gemini/",
            "source": "Google DeepMind",
            "published": "",
        },
        {
            "title": "Anthropic Claude model family",
            "link": "https://www.anthropic.com/claude",
            "source": "Anthropic",
            "published": "",
        },
        {
            "title": "Meta Llama open model page",
            "link": "https://www.llama.com/",
            "source": "Meta",
            "published": "",
        },
        {
            "title": "Hugging Face trending models",
            "link": "https://huggingface.co/models?sort=trending",
            "source": "Hugging Face",
            "published": "",
        },
    ],
    "trending": [
        {
            "title": "r/MachineLearning discussions",
            "link": "https://www.reddit.com/r/MachineLearning/",
            "source": "Reddit",
            "published": "",
        },
        {
            "title": "r/LocalLLaMA community trends",
            "link": "https://www.reddit.com/r/LocalLLaMA/",
            "source": "Reddit",
            "published": "",
        },
        {
            "title": "r/OpenAI community conversations",
            "link": "https://www.reddit.com/r/OpenAI/",
            "source": "Reddit",
            "published": "",
        },
        {
            "title": "GitHub trending AI repositories",
            "link": "https://github.com/trending?since=weekly",
            "source": "GitHub",
            "published": "",
        },
        {
            "title": "Hugging Face trending spaces",
            "link": "https://huggingface.co/spaces?sort=trending",
            "source": "Hugging Face",
            "published": "",
        },
    ],
    "learn": [
        {
            "title": "DeepLearning.AI learning resources",
            "link": "https://www.deeplearning.ai/",
            "source": "DeepLearning.AI",
            "published": "",
        },
        {
            "title": "Hugging Face learn portal",
            "link": "https://huggingface.co/learn",
            "source": "Hugging Face",
            "published": "",
        },
        {
            "title": "Kaggle learn courses",
            "link": "https://www.kaggle.com/learn",
            "source": "Kaggle",
            "published": "",
        },
        {
            "title": "Fast.ai practical deep learning",
            "link": "https://course.fast.ai/",
            "source": "fast.ai",
            "published": "",
        },
        {
            "title": "Microsoft AI learning hub",
            "link": "https://learn.microsoft.com/training/browse/?products=azure-openai",
            "source": "Microsoft Learn",
            "published": "",
        },
    ],
    "indian_ai": [
        {
            "title": "IndiaAI portal news and initiatives",
            "link": "https://indiaai.gov.in/",
            "source": "IndiaAI",
            "published": "",
        },
        {
            "title": "Analytics India Magazine AI coverage",
            "link": "https://analyticsindiamag.com/",
            "source": "Analytics India Magazine",
            "published": "",
        },
        {
            "title": "Inc42 artificial intelligence coverage",
            "link": "https://inc42.com/tag/artificial-intelligence/",
            "source": "Inc42",
            "published": "",
        },
        {
            "title": "YourStory AI startup coverage",
            "link": "https://yourstory.com/tag/artificial-intelligence",
            "source": "YourStory",
            "published": "",
        },
        {
            "title": "The Economic Times AI section",
            "link": "https://ai.economictimes.com/news",
            "source": "Economic Times",
            "published": "",
        },
    ],
    "github": [
        {
            "title": "microsoft/autogen Multi-agent framework for AI applications",
            "link": "https://github.com/microsoft/autogen",
            "source": "GitHub Trending",
            "published": "",
        },
        {
            "title": "langchain-ai/langchain Framework for LLM application orchestration",
            "link": "https://github.com/langchain-ai/langchain",
            "source": "GitHub Trending",
            "published": "",
        },
        {
            "title": "huggingface/transformers State of the art ML for PyTorch and TensorFlow",
            "link": "https://github.com/huggingface/transformers",
            "source": "GitHub Trending",
            "published": "",
        },
        {
            "title": "vllm-project/vllm High-throughput serving for large language models",
            "link": "https://github.com/vllm-project/vllm",
            "source": "GitHub Trending",
            "published": "",
        },
        {
            "title": "ollama/ollama Local model serving made simple",
            "link": "https://github.com/ollama/ollama",
            "source": "GitHub Trending",
            "published": "",
        },
    ],
}


def get_fallback_articles(category: str, limit: int = 5) -> list[dict[str, str]]:
    return FALLBACK_CONTENT.get(category, [])[:limit]
