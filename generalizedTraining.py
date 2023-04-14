import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, Trainer, TrainingArguments
from datasets import load_dataset
import evaluate, numpy as np
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer and model...")
checkpoint = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
print("Moving model to GPU...")
model = model.to(device)

print("Loading dataset...")
load_dataset_args = ("glue", "mrpc")
raw_datasets = load_dataset(*load_dataset_args)
print("Tokenizing dataset...")
tokenized_datasets = raw_datasets.map(lambda examples: tokenizer(examples["sentence1"], examples["sentence2"], truncation=True), batched=True)
# print("Moving dataset to GPU...")
# tokenized_datasets = tokenized_datasets.to(device)

data_collater = DataCollatorWithPadding(tokenizer)

def compute_metrics(eval_pred):
    metric = evaluate.load("glue", "mrpc")
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments('test-trainer', evaluation_strategy='epoch')

print("Creating trainer...")
trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collater,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

print("Starting training")

trainer.train()

model_tokenizer_save_path = "pretrained/" + checkpoint + "/" + '__'.join(load_dataset_args)
print(f"Saving model to {model_tokenizer_save_path}/")
model.save_pretrained(model_tokenizer_save_path + "/model")
tokenizer.save_pretrained(model_tokenizer_save_path + "/tokenizer")
