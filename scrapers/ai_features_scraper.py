"""
Curated data helpers for:
  /compare
  /roadmap
  /leaderboard
"""

import re

from utils.logger import setup_logger

logger = setup_logger(__name__)

MODEL_DATA = {
    "gpt-4o": {
        "full_name": "GPT-4o",
        "provider": "OpenAI",
        "context": "128k",
        "coding": "Excellent",
        "reasoning": "Excellent",
        "speed": "Fast",
        "cost": "High",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://openai.com/",
    },
    "gpt-4.5": {
        "full_name": "GPT-4.5",
        "provider": "OpenAI",
        "context": "128k",
        "coding": "Excellent",
        "reasoning": "Excellent",
        "speed": "Moderate",
        "cost": "Very High",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://openai.com/",
    },
    "claude": {
        "full_name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "context": "200k",
        "coding": "Excellent",
        "reasoning": "Excellent",
        "speed": "Fast",
        "cost": "High",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://www.anthropic.com/claude",
    },
    "claude 3.5": {
        "full_name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "context": "200k",
        "coding": "Excellent",
        "reasoning": "Excellent",
        "speed": "Fast",
        "cost": "High",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://www.anthropic.com/claude",
    },
    "gemini": {
        "full_name": "Gemini 1.5 Pro",
        "provider": "Google DeepMind",
        "context": "1M",
        "coding": "Strong",
        "reasoning": "Excellent",
        "speed": "Fast",
        "cost": "Medium",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://deepmind.google/technologies/gemini/",
    },
    "gemini 2.0": {
        "full_name": "Gemini 2.0 Flash",
        "provider": "Google DeepMind",
        "context": "1M",
        "coding": "Excellent",
        "reasoning": "Excellent",
        "speed": "Very Fast",
        "cost": "Low",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://deepmind.google/technologies/gemini/",
    },
    "llama": {
        "full_name": "Llama 3.3 70B",
        "provider": "Meta",
        "context": "128k",
        "coding": "Strong",
        "reasoning": "Strong",
        "speed": "Fast",
        "cost": "Self-hosted",
        "multimodal": "No",
        "open_source": "Yes",
        "link": "https://www.llama.com/",
    },
    "deepseek": {
        "full_name": "DeepSeek R1",
        "provider": "DeepSeek",
        "context": "64k",
        "coding": "Excellent",
        "reasoning": "Excellent",
        "speed": "Moderate",
        "cost": "Low",
        "multimodal": "No",
        "open_source": "Yes",
        "link": "https://www.deepseek.com/",
    },
    "mistral": {
        "full_name": "Mistral Large 2",
        "provider": "Mistral",
        "context": "128k",
        "coding": "Strong",
        "reasoning": "Strong",
        "speed": "Very Fast",
        "cost": "Medium",
        "multimodal": "No",
        "open_source": "Yes",
        "link": "https://mistral.ai/",
    },
    "qwen": {
        "full_name": "Qwen 2.5 72B",
        "provider": "Alibaba",
        "context": "128k",
        "coding": "Strong",
        "reasoning": "Strong",
        "speed": "Fast",
        "cost": "Self-hosted",
        "multimodal": "No",
        "open_source": "Yes",
        "link": "https://qwenlm.github.io/",
    },
    "grok": {
        "full_name": "Grok 3",
        "provider": "xAI",
        "context": "128k",
        "coding": "Strong",
        "reasoning": "Excellent",
        "speed": "Fast",
        "cost": "High",
        "multimodal": "Yes",
        "open_source": "No",
        "link": "https://x.ai/",
    },
}

MODEL_ALIASES = {
    "gpt4": "gpt-4o",
    "gpt 4": "gpt-4o",
    "chatgpt": "gpt-4o",
    "openai": "gpt-4o",
    "claude3": "claude",
    "anthropic": "claude",
    "gemini1.5": "gemini",
    "google": "gemini",
    "meta": "llama",
    "llama3": "llama",
    "deepseek-r1": "deepseek",
    "r1": "deepseek",
}

STATIC_LEADERBOARD = [
    {
        "rank": 1,
        "model": "GPT-4.5",
        "provider": "OpenAI",
        "arena_score": 1415,
        "coding": "Excellent",
        "reasoning": "Excellent",
    },
    {
        "rank": 2,
        "model": "Gemini 2.0 Flash",
        "provider": "Google",
        "arena_score": 1390,
        "coding": "Excellent",
        "reasoning": "Excellent",
    },
    {
        "rank": 3,
        "model": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "arena_score": 1380,
        "coding": "Excellent",
        "reasoning": "Excellent",
    },
    {
        "rank": 4,
        "model": "DeepSeek R1",
        "provider": "DeepSeek",
        "arena_score": 1365,
        "coding": "Excellent",
        "reasoning": "Excellent",
    },
    {
        "rank": 5,
        "model": "GPT-4o",
        "provider": "OpenAI",
        "arena_score": 1360,
        "coding": "Strong",
        "reasoning": "Excellent",
    },
    {
        "rank": 6,
        "model": "Grok 3",
        "provider": "xAI",
        "arena_score": 1350,
        "coding": "Strong",
        "reasoning": "Excellent",
    },
    {
        "rank": 7,
        "model": "Llama 3.3 70B",
        "provider": "Meta",
        "arena_score": 1320,
        "coding": "Strong",
        "reasoning": "Strong",
    },
    {
        "rank": 8,
        "model": "Qwen 2.5 72B",
        "provider": "Alibaba",
        "arena_score": 1310,
        "coding": "Strong",
        "reasoning": "Strong",
    },
    {
        "rank": 9,
        "model": "Mistral Large 2",
        "provider": "Mistral",
        "arena_score": 1290,
        "coding": "Good",
        "reasoning": "Strong",
    },
    {
        "rank": 10,
        "model": "Gemini 1.5 Pro",
        "provider": "Google",
        "arena_score": 1275,
        "coding": "Strong",
        "reasoning": "Strong",
    },
]

ROADMAPS = {
    "ai engineer": [
        (
            "1",
            "Python fundamentals",
            "Learn Python, NumPy, Pandas, and core software design.",
        ),
        (
            "2",
            "Math and statistics",
            "Cover linear algebra, probability, and statistics.",
        ),
        (
            "3",
            "Machine learning",
            "Practice supervised and unsupervised learning with scikit-learn.",
        ),
        (
            "4",
            "Deep learning",
            "Build with PyTorch or TensorFlow and understand transformers.",
        ),
        ("5", "NLP and LLMs", "Study prompting, embeddings, RAG, and evaluation."),
        (
            "6",
            "MLOps and deployment",
            "Use Docker, APIs, logging, and cloud deployment patterns.",
        ),
        (
            "7",
            "Portfolio projects",
            "Ship end-to-end AI apps and document what you built.",
        ),
    ],
    "machine learning": [
        (
            "1",
            "Python and data science",
            "Focus on Python, data cleaning, and exploratory analysis.",
        ),
        (
            "2",
            "Statistics and probability",
            "Build intuition for inference, distributions, and experiments.",
        ),
        (
            "3",
            "Classical ML",
            "Learn regression, classification, trees, and model evaluation.",
        ),
        (
            "4",
            "Unsupervised learning",
            "Work on clustering, dimensionality reduction, and anomaly detection.",
        ),
        (
            "5",
            "Deep learning",
            "Add neural networks, sequence models, and transformers.",
        ),
        ("6", "Evaluation", "Study metrics, validation, and error analysis."),
        (
            "7",
            "Projects",
            "Publish multiple real ML projects with notebooks and deployment demos.",
        ),
    ],
    "llm engineer": [
        (
            "1",
            "LLM fundamentals",
            "Understand transformers, tokenization, and context windows.",
        ),
        (
            "2",
            "Prompt engineering",
            "Practice structured prompts, tool use, and iteration.",
        ),
        (
            "3",
            "RAG systems",
            "Learn embeddings, vector databases, chunking, and retrieval.",
        ),
        ("4", "Fine-tuning", "Study SFT, LoRA, adapters, and evaluation loops."),
        ("5", "LLM evaluation", "Measure quality, latency, hallucination, and cost."),
        (
            "6",
            "Production systems",
            "Build APIs, streaming responses, observability, and guardrails.",
        ),
        (
            "7",
            "Agents and multimodal",
            "Explore workflows with tools, planning, and vision models.",
        ),
    ],
    "data scientist": [
        ("1", "Python and SQL", "Learn Python, SQL, and dataframe workflows."),
        (
            "2",
            "EDA and visualization",
            "Use charts and dashboards to inspect patterns.",
        ),
        ("3", "Statistics", "Cover testing, regression, and experiment design."),
        ("4", "Machine learning", "Train and evaluate practical models."),
        ("5", "Feature engineering", "Build useful inputs and reusable pipelines."),
        ("6", "Communication", "Translate results into business recommendations."),
        ("7", "Portfolio", "Publish strong case studies with code and visuals."),
    ],
    "default": [
        (
            "1",
            "Python basics",
            "Start with Python and general programming fundamentals.",
        ),
        ("2", "Machine learning", "Learn common ML methods and evaluation."),
        (
            "3",
            "Deep learning",
            "Move into neural networks and transformer-based models.",
        ),
        (
            "4",
            "LLM applications",
            "Build prompt-based and retrieval-based applications.",
        ),
        ("5", "Projects", "Create and ship projects that prove your skills."),
    ],
}


class AICompareScraper:
    def compare(self, models_input: str) -> str:
        parts = re.split(r"\s+vs\.?\s+|\s+and\s+|,\s*", models_input, flags=re.IGNORECASE)
        parts = [part.strip().lower() for part in parts if part.strip()]

        resolved = []
        for name in parts:
            key = self._resolve_model(name)
            if key and key not in [item[0] for item in resolved]:
                resolved.append((key, MODEL_DATA[key]))

        if not resolved:
            known = ", ".join(sorted({data["full_name"] for data in MODEL_DATA.values()}))
            return (
                f"No recognized models found in: *{models_input}*\n\n"
                f"Supported models:\n{known}\n\n"
                "Example: `/compare GPT-4o vs Claude vs Gemini`"
            )

        if len(resolved) == 1:
            return self._single_model_card(resolved[0][1])

        return self._comparison_table(resolved)

    def _resolve_model(self, name: str) -> str | None:
        normalized = name.lower().strip()
        if normalized in MODEL_DATA:
            return normalized
        if normalized in MODEL_ALIASES:
            return MODEL_ALIASES[normalized]
        for key in MODEL_DATA:
            if normalized in key or key in normalized:
                return key
        return None

    def _single_model_card(self, model: dict) -> str:
        return (
            f"*{model['full_name']}* - {model['provider']}\n\n"
            f"Context window: `{model['context']}`\n"
            f"Coding: {model['coding']}\n"
            f"Reasoning: {model['reasoning']}\n"
            f"Speed: `{model['speed']}`\n"
            f"Cost: `{model['cost']}`\n"
            f"Multimodal: {model['multimodal']}\n"
            f"Open source: {model['open_source']}\n"
            f"Reference: {model['link']}"
        )

    def _comparison_table(self, resolved: list) -> str:
        lines = ["*AI Model Comparison*", "", "Source: curated reference data", ""]
        features = [
            ("Provider", "provider"),
            ("Context", "context"),
            ("Coding", "coding"),
            ("Reasoning", "reasoning"),
            ("Speed", "speed"),
            ("Cost", "cost"),
            ("Multimodal", "multimodal"),
            ("Open source", "open_source"),
        ]

        for label, key in features:
            lines.append(f"*{label}*")
            for _, data in resolved:
                lines.append(f"- {data['full_name']}: {data[key]}")
            lines.append("")

        lines.append("Reference: https://artificialanalysis.ai")
        return "\n".join(lines).strip()


class AIRoadmapScraper:
    def get_roadmap(self, role_input: str) -> str:
        role = role_input.strip().lower()
        steps = self._find_roadmap(role)
        title = role_input.strip().title() if role_input.strip() else "AI Engineer"

        lines = [
            f"*AI Learning Roadmap: {title}*",
            "",
            "Reference set: roadmap.sh, DeepLearning.AI, Hugging Face",
            "",
        ]

        for step_number, step_title, details in steps:
            lines.append(f"{step_number}. *{step_title}*")
            lines.append(f"   {details}")
            lines.append("")

        lines.append("Full roadmap: https://roadmap.sh/ai-engineer")
        lines.append("Practice hub: https://www.kaggle.com/learn")
        return "\n".join(lines).strip()

    def _find_roadmap(self, role: str) -> list:
        normalized_role = role.strip().lower()
        if normalized_role in ROADMAPS:
            return ROADMAPS[normalized_role]

        best_key = None
        best_score = 0
        role_words = set(normalized_role.split())

        for key in ROADMAPS:
            if key == "default":
                continue

            key_words = set(key.split())
            if key in normalized_role or normalized_role in key:
                score = len(key_words) + 10
            else:
                score = len(role_words & key_words)

            if score > best_score:
                best_key = key
                best_score = score

        if best_key:
            return ROADMAPS[best_key]
        return ROADMAPS["default"]


class AILeaderboardScraper:
    async def get_leaderboard(self, filter_input: str = "") -> str:
        term = filter_input.strip().lower()
        data = STATIC_LEADERBOARD

        if term:
            filtered = [
                entry
                for entry in STATIC_LEADERBOARD
                if term in entry["model"].lower() or term in entry["provider"].lower()
            ]
            if filtered:
                data = filtered
            else:
                logger.info(
                    f"No leaderboard matches for filter '{filter_input}', returning the full curated list."
                )

        lines = [
            "*AI Model Leaderboard*",
            "Source: curated reference snapshot",
            "",
        ]

        for entry in data[:10]:
            lines.append(
                f"{entry['rank']}. *{entry['model']}* - _{entry['provider']}_\n"
                f"   Arena score: `{entry['arena_score']}` | Coding: {entry['coding']} | Reasoning: {entry['reasoning']}"
            )
            lines.append("")

        lines.append("Reference: https://lmarena.ai")
        lines.append("Analysis: https://artificialanalysis.ai/leaderboards")
        return "\n".join(lines).strip()
