import torch
from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image

class ChartAnalyzer:
    def __init__(self, model_path):
        self.model = AutoModelForVision2Seq.from_pretrained(model_path)
        self.processor = AutoProcessor.from_pretrained(model_path)
        self.model.eval()
    
    def analyze_chart(self, image_path):
        image = Image.open(image_path).convert('RGB')
        inputs = self.processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs)
            predictions = self.processor.batch_decode(outputs, skip_special_tokens=True)
            
        return predictions[0]
