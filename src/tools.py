from pathlib import Path
from venv import logger

from smolagents import Tool


class LoadFileTool(Tool):
    name = "load_file_content"
    description = """
    Load a textual file and return its content as a string.
    """

    inputs = {
        "file_path": {
            "type": "string",
            "description": "The file path to read the content from.",
        }
    }

    output_type = "string"

    def forward(self, file_path: str) -> str:
        logger.info(f"Loading file content from: {file_path}")
        extension = Path(file_path).suffix
        if extension in [".json", ".txt"]:
            with open(file_path) as f:
                content = f.read()
            return content
        elif extension in [".csv"]:
            import pandas as pd

            df = pd.read_csv(file_path)
            return df.to_json()
        elif extension in [".xlsx"]:
            import pandas as pd

            df = pd.read_excel(file_path)
            return df.to_json()
        else:
            raise ValueError(f"Unsupported file type: {extension}")


class WebPageReaderTool(Tool):
    name = "webpage_reader"
    description = """
    Fetch the content of a webpage and return it as a string.
    """

    inputs = {
        "url": {
            "type": "string",
            "description": "The URL of the webpage to fetch.",
        }
    }

    output_type = "string"

    def forward(self, url: str) -> str:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch the webpage: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        return text


class TextFromImageTool(Tool):
    name = "text_from_image"
    description = """
    Extract text from an image using OCR (Optical Character Recognition).
    """

    inputs = {
        "image_path": {
            "type": "string",
            "description": "The file path to the image.",
        }
    }

    output_type = "string"

    def forward(self, image_path: str) -> str:
        logger.info(f"Extracting text from image: {image_path}")
        import pytesseract
        from PIL import Image

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text


class DescribeImageTool(Tool):
    name = "describe_image"
    description = """
    Describe the content of an image using a pre-trained model.
    """

    inputs = {
        "image_path": {
            "type": "string",
            "description": "The file path to the image.",
        }
    }

    output_type = "string"

    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, image_path: str) -> str:
        return self.model(image_path)
