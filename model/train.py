from transformers import AutoModelForVision2Seq, AutoProcessor
import torch
from torch.utils.data import DataLoader
from data.dataset import ChartDataset
from config.config import ModelConfig

def train():
    config = ModelConfig()
    
    # Use the correct model identifier
    model = AutoModelForVision2Seq.from_pretrained("meta-llama/Llama-2-7b-chat-hf", 
                                                  token="your_huggingface_token")
    processor = AutoProcessor.from_pretrained("meta-llama/Llama-2-7b-chat-hf",
                                            token="your_huggingface_token")

    device = torch.device("cpu")
    model.to(device)
    
    # Rest of the training code remains the same

    # Prepare dataset
    dataset = ChartDataset("data/training_data.csv")
    train_loader = DataLoader(
        dataset, 
        batch_size=config.batch_size, 
        shuffle=True
    )
    
    # Training loop
    model.train()
    optimizer = torch.optim.AdamW(
        model.parameters(), 
        lr=config.learning_rate
    )
    
    for epoch in range(config.num_epochs):
        for batch in train_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            
            print(f"Epoch: {epoch}, Loss: {loss.item():.4f}")
            
    # Save model
    model.save_pretrained(config.output_dir)
    processor.save_pretrained(config.output_dir)

if __name__ == "__main__":
    train()
