import torch
import json
import os

class TextPreprocessor:
    def __init__(self, char2idx_path):
        # Load the character mapping
        if not os.path.exists(char2idx_path):
            raise FileNotFoundError(f"Mapping file not found at {char2idx_path}")
            
        with open(char2idx_path, 'r', encoding='utf-8') as f:
            self.char2idx = json.load(f)
        
    def prepare_input(self, text: str, max_len: int = 150):
        # 1. Clean text to match training (remove spaces)
        clean_text = text.replace(" ", "").strip()
        
        # 2. Convert to indices (use 0 for padding/unknown)
        indices = [self.char2idx.get(char, 0) for char in clean_text]
        
        # 3. Padding/Truncating
        if len(indices) > max_len:
            indices = indices[:max_len]
        else:
            indices = indices + [0] * (max_len - len(indices))
            
        return torch.LongTensor(indices).unsqueeze(0), clean_text