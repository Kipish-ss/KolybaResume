import torch
from torch.utils.data import DataLoader
from torch.nn import Module
from torch.optim import Optimizer
from typing import Callable
from torchmetrics import Metric
from transformers import get_linear_schedule_with_warmup
from tqdm import tqdm


class ClassificationTrainer:
    def __init__(
            self,
            train_dataloader: DataLoader,
            val_dataloader: DataLoader,
            model: Module,
            optimizer: Optimizer,
            loss_function: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
            metric: Metric,
            epochs: int,
            device: torch.device):
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.model = model
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.metric = metric
        self.epochs = epochs

        self.device = device
        self.model.to(self.device)
        self.metric.to(self.device)

        num_training_steps = self.epochs * len(self.train_dataloader)
        self.scheduler = get_linear_schedule_with_warmup(self.optimizer, num_warmup_steps=0,
                                                         num_training_steps=num_training_steps)
        self.history = {'train_loss': [], 'val_loss': [], 'train_metric': [], 'val_metric': []}

    def _train_step(self) -> tuple[float, float]:
        self.model.train()
        loss = 0

        for batch in tqdm(self.train_dataloader, desc="Training", leave=False):
            token_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)

            self.optimizer.zero_grad()
            batch_loss, logits = self.model(input_ids=token_ids, attention_mask=attention_mask, labels=labels,
                                            return_dict=False)

            loss += batch_loss.item()
            batch_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            self.scheduler.step()

            preds = torch.argmax(logits, dim=1)
            self.metric.update(preds, labels)

        avg_loss = loss / len(self.train_dataloader)
        metric_result = self.metric.compute()

        return avg_loss, metric_result.item()

    def _val_step(self) -> tuple[float, float]:
        self.model.eval()
        loss = 0

        with torch.no_grad():
            for batch in tqdm(self.val_dataloader, desc="Validating", leave=False):
                token_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)

                batch_loss, logits = self.model(input_ids=token_ids, attention_mask=attention_mask, labels=labels,
                                                return_dict=False)

                loss += batch_loss.item()

                preds = torch.argmax(logits, dim=1)
                self.metric.update(preds, labels)

        avg_loss = loss / len(self.val_dataloader)
        metric_result = self.metric.compute()

        return avg_loss, metric_result.item()

    def fine_tune(self) -> None:
        for epoch in range(1, self.epochs + 1):
            self.metric.reset()
            train_loss, train_metric = self._train_step()

            self.metric.reset()
            val_loss, val_metric = self._val_step()

            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['train_metric'].append(train_metric)
            self.history['val_metric'].append(val_metric)

            print(f'Epoch {epoch}/{self.epochs}')
            print(f'  Train Loss: {train_loss:.4f}, Train Metric: {train_metric:.4f}')
            print(f'  Val Loss: {val_loss:.4f}, Val Metric: {val_metric:.4f}')
