import torch
from torch.utils.data import Dataset
from transformers import (
    PreTrainedModel,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)

class TextDataset(Dataset):
    def __init__(self, tokenizer: AutoTokenizer, text: str, block_size: int = 1024):
        self.tokenizer = tokenizer
        self.block_size = block_size

        self.examples = tokenizer(text, return_tensors='pt', padding=False)['input_ids']

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]

def train_model(
    model: PreTrainedModel,
    tokenizer: AutoTokenizer,
    text: str,
    training_args: TrainingArguments = None,
    block_size: int = 1024,
):
    training_args = TrainingArguments(
        "test-trainer",
    ),
    
    dataset = TextDataset(tokenizer, text, block_size)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False
    )

    trainer = Trainer(
        model=model,
        # args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    trainer.train()

    return model
