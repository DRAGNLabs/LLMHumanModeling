from transformers import AutoTokenizer

def extract_n_tokens(text: str, n: int, tokenizer: AutoTokenizer) -> tuple(list(int), str, str):
    # Tokenize the text
    encoded_text = tokenizer.encode(text, add_special_tokens=False)

    # Extract the first n tokens
    n_tokens = encoded_text[:n]

    # Decode the tokens back to text
    extracted_text = tokenizer.decode(n_tokens)

    # Truncate the original text
    truncated_text = text[len(extracted_text):]
    
    input_text = tokenizer.decode(n_tokens)

    # Return the extracted tokens and truncated text
    return n_tokens, input_text, truncated_text