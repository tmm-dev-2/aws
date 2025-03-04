from dataclasses import dataclass

@dataclass
class ModelConfig:
    base_model: str = "llama-2-7b"
    output_dir: str = "trained_model"
    max_length: int = 1024
    image_size: int = 224
    batch_size: int = 8
    learning_rate: float = 2e-5
    num_epochs: int = 3
    patterns = ["bullish_engulfing", "bearish_engulfing", "doji", "hammer"]
