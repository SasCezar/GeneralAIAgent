import os

import gradio as gr
import pandas as pd
from hydra import compose, initialize
from hydra.utils import instantiate
from loguru import logger
from omegaconf import OmegaConf
from tqdm import tqdm

from agent import GeneralAgent
from src.hf_gaia_api import (
    HFGAIAApiClient,
)
from src.utils import save_temp_file, setup_telemetry

setup_telemetry()


def run_and_submit_all(profile: gr.OAuthProfile | None):
    """
    Fetches all questions, runs the BasicAgent on them, submits all answers,
    and displays the results.
    """
    with initialize(version_base="1.3", config_path="config"):
        cfg = compose(config_name="config")
        logger.info(OmegaConf.to_yaml(cfg, resolve=True))

    tools = instantiate(cfg.tools)
    tools = [tools[k] for k in tools]

    llm = instantiate(cfg.llm)
    logger.info(f"LLM: {llm}")
    logger.info(f"Tools: {tools}")

    if profile:
        username = f"{profile.username}"
        logger.info(f"User logged in: {username}")
    else:
        logger.info("User not logged in.")
        return "Please Login to Hugging Face with the button.", None

    # 1. Initialize components
    try:
        agent = GeneralAgent(tools=tools, model=llm)
        logger.info(f"Agent initialized: {agent}")
        api = HFGAIAApiClient()
    except Exception as e:
        logger.info(f"Error initializing agent or API client: {e}")
        return f"Error initializing agent or API client: {e}", None

    space_id = os.getenv("SPACE_ID")
    agent_code = (
        f"https://huggingface.co/spaces/{space_id}/tree/main" if space_id else "unknown"
    )

    # 2. Fetch questions
    try:
        questions_data = api.get_questions()
        if not questions_data:
            return "Fetched questions list is empty or invalid.", None
        logger.info(f"Fetched {len(questions_data)} questions.")
    except Exception as e:
        return f"Error fetching questions: {e}", None

    # 3. Run agent on each question
    results_log = []
    answers_payload = []

    for item in tqdm(questions_data):
        task_id = item.get("task_id")
        question_text = item.get("question")
        if not task_id or question_text is None:
            continue
        try:
            file_path = None
            try:

                file_content = api.get_file(task_id)
                logger.info(f"Found file for task {task_id}")
                file_path = save_temp_file(file_content, task_id)
            except Exception as file_e:
                logger.info(f"No file found for task {task_id} or error: {file_e}")

            submitted_answer = agent(question_text, file_path)
            answers_payload.append(
                {"task_id": task_id, "submitted_answer": submitted_answer}
            )
            results_log.append(
                {
                    "Task ID": task_id,
                    "Question": question_text,
                    "Submitted Answer": submitted_answer,
                }
            )
        except Exception as e:
            results_log.append(
                {
                    "Task ID": task_id,
                    "Question": question_text,
                    "Submitted Answer": f"AGENT ERROR: {e}",
                }
            )

    if not answers_payload:
        return "Agent did not produce any answers to submit.", pd.DataFrame(results_log)

    # 4. Submit answers
    try:
        result_data = api.submit_answers(username, agent_code, answers_payload)
        final_status = (
            f"Submission Successful!\n"
            f"User: {result_data.get('username')}\n"
            f"Overall Score: {result_data.get('score', 'N/A')}% "
            f"({result_data.get('correct_count', '?')}/{result_data.get('total_attempted', '?')} correct)\n"
            f"Message: {result_data.get('message', 'No message received.')}"
        )
        return final_status, pd.DataFrame(results_log)
    except Exception as e:
        return f"Submission failed: {e}", pd.DataFrame(results_log)


# --- Build Gradio Interface ---
with gr.Blocks() as demo:
    gr.Markdown("# Basic Agent Evaluation Runner")
    gr.Markdown(
        """
        **Instructions:**

        1. Clone this space and define your custom agent logic and tools.
        2. Log in to your Hugging Face account below.
        3. Click 'Run Evaluation & Submit All Answers' to evaluate and score your agent.

        ---
        **Note:** Submissions can take time depending on how long your agent takes to answer.
        """
    )

    gr.LoginButton()

    run_button = gr.Button("Run Evaluation & Submit All Answers")
    status_output = gr.Textbox(
        label="Run Status / Submission Result", lines=5, interactive=False
    )
    results_table = gr.DataFrame(label="Questions and Agent Answers", wrap=True)

    run_button.click(fn=run_and_submit_all, outputs=[status_output, results_table])

# --- Startup Info ---
if __name__ == "__main__":
    logger.info("\n" + "-" * 30 + " App Starting " + "-" * 30)

    space_host = os.getenv("SPACE_HOST")
    space_id = os.getenv("SPACE_ID")

    if space_host:
        logger.info(f"✅ SPACE_HOST: {space_host}")
        logger.info(f"   Runtime URL: https://{space_host}.hf.space")
    else:
        logger.info("ℹ️  SPACE_HOST not set (likely running locally).")

    if space_id:
        logger.info(f"✅ SPACE_ID: {space_id}")
        logger.info(f"   Repo: https://huggingface.co/spaces/{space_id}")
    else:
        logger.info("ℹ️  SPACE_ID not set (repo link not available).")

    logger.info("-" * (60 + len(" App Starting ")) + "\n")
    logger.info("Launching Gradio Interface...")
    demo.launch(debug=True, share=False)
