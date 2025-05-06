import torch
from torch.utils.data import Dataset
from transformers import PreTrainedTokenizer


class ResumeDataset(Dataset):
    def __init__(
            self,
            resumes: list[str],
            labels: list[int],
            tokenizer: PreTrainedTokenizer,
            max_length: int = 512
    ):
        self.resumes = resumes
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        text = self.resumes[idx]
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            return_tensors='pt',
            max_length=self.max_length,
            padding='max_length',
            truncation=True
        )

        input_ids = encoding['input_ids'].squeeze(0)
        attention_mask = encoding['attention_mask'].squeeze(0)
        labels_tensor = torch.tensor(label, dtype=torch.long)

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels_tensor
        }

    def __len__(self) -> int:
        return len(self.resumes)
