import modal

app = modal.App("llama-vision-finetune")

image = modal.Image.debian_slim().pip_install(
    "torch",
    "transformers",
    "pandas",
    "numpy",
    "pillow",
    "accelerate"
)

volume = modal.Volume("chart-training-data")

@app.function(
    gpu="A100",
    image=image,
    timeout=3600,
    volumes={"/data": volume}
)
def train_model():
    import pandas as pd
    import torch
    from transformers import AutoModelForVision2Seq, AutoProcessor, TrainingArguments, Trainer
    
    model = AutoModelForVision2Seq.from_pretrained("llama-3.2-vision", trust_remote_code=True, device_map="auto")
    processor = AutoProcessor.from_pretrained("llama-3.2-vision")
    
    train_dataset = pd.read_csv("/data/training_results.csv")
    
    training_args = TrainingArguments(
        output_dir="/data/model_output",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_dir="/data/logs",
        logging_steps=10,
        save_strategy="epoch"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=lambda data: {
            "pixel_values": torch.stack([x["pixel_values"] for x in data]),
            "labels": torch.stack([x["labels"] for x in data])
        }
    )
    
    trainer.train()
    model.save_pretrained("/data/final_model")
    processor.save_pretrained("/data/final_model")
    return "Training completed successfully!"

if __name__ == "__main__":
    modal.run(train_model.remote())
