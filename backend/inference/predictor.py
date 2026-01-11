import torch
import json
import os
from model.bilstm_model import BiLSTM_POS
from inference.preprocess import TextPreprocessor

class POSPredictor:
    def __init__(self, model_path, char_map, pos_map):
        # Set device (Detect GPU, otherwise CPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # 1. Load POS Mappings
        with open(pos_map, 'r', encoding='utf-8') as f:
            raw_pos = json.load(f)
            # Ensure keys are integers for easy lookup
            self.idx2pos = {int(v): k for k, v in raw_pos.items()}
        
        # 2. Initialize Preprocessor
        self.preprocessor = TextPreprocessor(char_map)
        
        # 3. Load Model
        self.model = BiLSTM_POS()
        # Note: Ensure your bilstm_model.py uses init instead of init
        
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        else:
            print(f"Warning: Model file {model_path} not found!")
            
        self.model.to(self.device)
        self.model.eval()

    def predict(self, raw_text: str):
        if not raw_text.strip():
            return []

        # Preprocess and get the cleaned text (no spaces)
        input_tensor, clean_text = self.preprocessor.prepare_input(raw_text)
        input_tensor = input_tensor.to(self.device)
        
        with torch.no_grad():
            seg_out, pos_out = self.model(input_tensor)

        # Remove batch dimension and move to CPU for processing
        seg_preds = seg_out.argmax(-1)[0].cpu().tolist()
        pos_preds = pos_out.argmax(-1)[0].cpu().tolist()

        return self._build_results(clean_text, seg_preds, pos_preds)

    def _build_results(self, text, seg, pos):
        results = []
        current_word = ""
        current_pos = None

        for i, ch in enumerate(text):
            # i can't exceed the predicted sequence length
            if i >= len(seg):
                break

            # Based on your logic: 0 is the 'Begin' of a new word
            if seg[i] == 0:
                if current_word:
                    results.append({"word": current_word, "tag": current_pos})
                
                current_word = ch
                current_pos = self.idx2pos.get(pos[i], "UNKNOWN")
            else:
                current_word += ch

        # Add the final word
        if current_word:
            results.append({"word": current_word, "tag": current_pos})

        return results