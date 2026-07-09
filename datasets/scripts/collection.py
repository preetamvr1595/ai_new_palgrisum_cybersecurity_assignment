import pandas as pd
import logging

logger = logging.getLogger(__name__)

def mock_download_human_dataset(source_name: str, num_samples: int = 1000) -> pd.DataFrame:
    """
    Mocks downloading a human dataset from sources like CommonCrawl or Academic papers.
    """
    logger.info(f"Downloading {num_samples} samples from {source_name}...")
    # Mock data
    data = [{"text": f"This is a human written sample {i}.", "source": source_name} for i in range(num_samples)]
    return pd.DataFrame(data)

def mock_generate_ai_dataset(model_name: str, prompts: list, num_samples: int = 1000) -> pd.DataFrame:
    """
    Mocks generating an AI dataset by hitting an LLM API.
    """
    logger.info(f"Generating {num_samples} AI samples using {model_name}...")
    data = [{"text": f"This is an AI generated response {i}.", "source": model_name, "prompt": prompts[i % len(prompts)]} for i in range(num_samples)]
    return pd.DataFrame(data)
