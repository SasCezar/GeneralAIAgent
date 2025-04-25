from typing import Any

import requests


class HFGAIAApiClient:
    def __init__(self, api_url="https://agents-course-unit4-scoring.hf.space"):
        self.api_url = api_url
        self.questions_url = f"{api_url}/questions"
        self.submit_url = f"{api_url}/submit"
        self.files_url = f"{api_url}/files"

    def get_questions(self) -> list[dict[str, Any]]:
        """
        Get all questions from HF evaluation endpoint.
        """
        response = requests.get(self.questions_url)
        response.raise_for_status()
        return response.json()

    def get_random_question(self) -> dict[str, Any]:
        """
        Get a random question from HF evaluation endpoint.
        """
        response = requests.get(f"{self.api_url}/random-question")
        response.raise_for_status()
        return response.json()

    def get_file(self, task_id: str) -> bytes:
        """
        Download a file from HF evaluation endpoint
        The task_id is the unique identifier for the file.
        """
        response = requests.get(f"{self.files_url}/{task_id}")
        response.raise_for_status()
        return response.content

    def submit_answers(
        self, username: str, agent_code: str, answers: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Submit answers to HF evaluation endpoint. The endpoint returns a JSON object
        containing the evaluation results.
        """
        data = {"username": username, "agent_code": agent_code, "answers": answers}
        response = requests.post(self.submit_url, json=data)
        response.raise_for_status()
        return response.json()
