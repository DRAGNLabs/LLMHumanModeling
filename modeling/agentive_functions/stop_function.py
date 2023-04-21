from math import exp as mathExp
from .llm_functions.perplexity import get_ppl

def sigmoid(x):
    """A sigmoid-esque function created through roughly gauging WolfRam Alpha visualizations"""
    return 1 / (
        1 + mathExp(
            -((x-5)/1.8)
            )
        )

def stop_or_continue(model, tokenizer = None, text: str = None, tokens = None, ideal_ppl: float = 25, device = None) -> float:
    """Calculate probability of stopping training on a given text; higher is more likely"""
    
    # Calculate the perplexity of the model on the given text
    model_ppl = get_ppl(model, tokenizer, text, device=device)

    # Find the absolute difference between the model's and the ideal perplexity
    diff = abs(model_ppl - ideal_ppl)

    # Apply the sigmoid function to the difference
    sigmoid_diff = sigmoid(diff)

    return sigmoid_diff
