import torch
from torch.utils.data import Dataset
import pandas as pd
from PIL import Image
import os

class ChartDataset(Dataset):
    def __init__(self, data_dir, annotations_file, processor=None):
        self.data_dir = data_dir
        self.annotations = pd.read_csv(annotations_file)
        self.processor = processor

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        img_path = os.path.join(self.data_dir, self.annotations.iloc[idx]['image_file'])
        image = Image.open(img_path).convert('RGB')
        label = self.annotations.iloc[idx]['pattern']

        if self.processor:
            inputs = self.processor(images=image, return_tensors="pt")
            return {
                "pixel_values": inputs.pixel_values.squeeze(),
                "labels": torch.tensor(self.patterns.index(label))
            }
        return image, label
