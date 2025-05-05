from torch.optim import AdamW
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from ml_backend.models import ClassificationTrainer, ResumeDataset
from sklearn.preprocessing import LabelEncoder
from torchmetrics import F1Score
from sklearn.model_selection import train_test_split
import pandas as pd
import torch
from joblib import dump
from collections import Counter
import numpy as np

file_path = "/content/drive/MyDrive/preprocessed_resumes.parquet"

EPOCHS = 4
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MODEL_NAME = 'bert-base-uncased'
MAX_LENGTH = 512
VAL_SIZE = 0.1
RANDOM_STATE = 42


def load_data(file_path: str) -> tuple[list[str], list[int], LabelEncoder]:
    df = pd.read_parquet(file_path)
    resumes = df['Resume'].tolist()

    encoder = LabelEncoder()
    labels = encoder.fit_transform(df['Category']).tolist()

    return resumes, labels, encoder


resumes, labels, encoder = load_data(file_path)

train_resumes, val_resumes, train_labels, val_labels = train_test_split(
    resumes, labels, test_size=VAL_SIZE, stratify=labels, random_state=42)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_dataset = ResumeDataset(train_resumes, train_labels, tokenizer, max_length=MAX_LENGTH)
val_dataset = ResumeDataset(val_resumes, val_labels, tokenizer, max_length=MAX_LENGTH)
train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=True)

num_classes = len(encoder.classes_)
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=num_classes)

optimizer = AdamW(model.parameters())
label_counts = Counter(train_labels)
counts = np.array([label_counts[i] for i in range(num_classes)], dtype=np.float32)
weights = 1.0 / counts
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
weights = torch.tensor(weights / weights.sum(), dtype=torch.float32).to(device)
loss_function = torch.nn.CrossEntropyLoss(weight=weights)
metric = F1Score(task='multiclass', num_classes=num_classes, average='macro')

trainer = ClassificationTrainer(
    train_dataloader=train_dataloader,
    val_dataloader=val_dataloader,
    model=model,
    optimizer=optimizer,
    loss_function=loss_function,
    metric=metric,
    epochs=EPOCHS,
    device=device
)

trainer.fine_tune()

model.save_pretrained("/content/drive/MyDrive/fine_tuned_bert")
tokenizer.save_pretrained("/content/drive/MyDrive/fine_tuned_bert")
dump(encoder, "/content/drive/MyDrive/label_encoder.joblib")
