import openai
import os
import time
from typing import Dict, Any, Optional
from src.llm.prompt_builder import PromptBuilder
from src.config import config

class OpenAIClient:
    """
    Handles OpenAI/LM Studio API interaction for performance analysis and reflection questions.
    Supports local LM Studio endpoint via config (set OPENAI_API_BASE and model as needed).
    """
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, rate_limit: int = 60, api_base: Optional[str] = None):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "http://192.168.2.3:1234/v1")
        self.rate_limit = rate_limit  # requests per minute
        self.last_request_time = 0
        openai.api_key = self.api_key or "sk-local"  # LM Studio ignores key but openai-python requires a value
        openai.api_base = self.api_base

    def _rate_limit(self):
        now = time.time()
        elapsed = now - self.last_request_time
        min_interval = 60 / self.rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()

    def generate_performance_analysis(self, metrics: Dict[str, Any]) -> str:
        prompt = PromptBuilder.build_performance_prompt(metrics)
        return self._call_openai(prompt)

    def generate_reflection_questions(self, metrics: Dict[str, Any]) -> str:
        prompt = PromptBuilder.build_reflection_prompt(metrics)
        return self._call_openai(prompt)

    def _call_openai(self, prompt: str) -> str:
        self._rate_limit()
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            return f"OpenAI/LM Studio API error: {e}" 