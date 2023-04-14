import torch
from transformers import (
    Trainer,
    TrainingArguments,
    AutoTokenizer,
    PreTrainedModel,
    TextDataset,
    DataCollatorForLanguageModeling,
)

def train_transformer_model(
    model: PreTrainedModel,
    text: str,
    training_args: TrainingArguments = TrainingArguments(
        "test-trainer",
    ),
    block_size: int = 1024,
):
    # # Save the input text to a file
    # with open("input_text.txt", "w") as f:
    #     f.write(text)

    # Load the tokenizer using the model's name
    tokenizer = AutoTokenizer.from_pretrained(model.name_or_path)

    # Create a dataset from the input text
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path="input_text.txt",
        block_size=block_size,
    )

    # Create a data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.15
    )

    # Create the trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    # Train the model
    trainer.train()

    # Save the trained model
    model.save_pretrained("trained_model")

# Example usage:
# from transformers import AutoModelForMaskedLM

# model = AutoModelForMaskedLM.from_pretrained("distilbert-base-uncased")
# text = "This is a sample text for training the model."

# train_transformer_model(model, text)
