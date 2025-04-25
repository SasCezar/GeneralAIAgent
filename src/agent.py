from collections.abc import Callable
from pathlib import Path

from smolagents import CodeAgent


class GeneralAgent:
    def __init__(
        self, model: Callable, tools: list = None, additional_imports: list = None
    ):

        self.imports = [
            "pandas",
            "numpy",
            "datetime",
            "json",
            "re",
            "math",
            "os",
            "requests",
            "csv",
            "urllib",
            "bs4",
        ]
        if additional_imports:
            self.imports.extend(additional_imports)

        self.tools = tools if tools else []
        self.agent = CodeAgent(
            model=model,
            tools=self.tools,
            additional_authorized_imports=self.imports,
        )

    def __call__(self, question: str, file_path: str | Path | None) -> str:
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        prompt = self.format_prompt(question, file_path)
        answer = self.agent.run(prompt)
        return answer

    def format_prompt(self, question: str, file_path: str | Path | None) -> str:
        context = f"Question: {question}\n"
        if file_path:
            context += f"The question has and attached file located at: {file_path}\nIf the file is not needed, or an error araises, please ignore it and answer with the other info available.\n"

        full_prompt = f"""{context}
When answering, provide ONLY the precise answer requested.
Do not include explanations, steps, reasoning, or additional text.
Be direct and specific. GAIA benchmark requires exact matching answers.
For example, if asked "What is the capital of France?", respond simply with "Paris".
"""
        return full_prompt
