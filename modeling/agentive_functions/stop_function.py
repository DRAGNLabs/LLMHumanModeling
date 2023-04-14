import torch
from llm_functions.perplexity import get_ppl

def sigmoid(x):
    return 1 / (
        1 + torch.exp(
            -((x-5)/1.8)
            )
        )

def stop_training(model, tokenizer = None, text: str = None, tokens = None, ideal_ppl: float = 25) -> float:
    # Calculate the perplexity of the model on the given text
    model_ppl = get_ppl(model, tokens=tokens)

    # Find the absolute difference between the model's and the ideal perplexity
    diff = abs(model_ppl - ideal_ppl)

    # Apply the sigmoid function to the difference
    sigmoid_diff = sigmoid(diff)

    return sigmoid_diff
