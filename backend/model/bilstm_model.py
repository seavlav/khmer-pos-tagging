import torch
import torch.nn as nn

class BiLSTM_POS(nn.Module):
    def init(self):
        super().init()
        self.embedding = nn.Embedding(91, 128, padding_idx=0)
        self.lstm = nn.LSTM(128, 256, batch_first=True, bidirectional=True)
        self.seg_fc = nn.Linear(512, 2)
        self.pos_fc = nn.Linear(512, 13)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        return self.seg_fc(x), self.pos_fc(x)