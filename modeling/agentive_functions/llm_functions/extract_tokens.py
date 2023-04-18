from transformers import AutoTokenizer

def extract_n_tokens(text: str, n: int, tokenizer: AutoTokenizer) -> tuple[list[int], str, str]:
    # Tokenize the text
    encoded_text = tokenizer(text, add_special_tokens=False).input_ids

    # Extract the first n tokens
    n_tokens = encoded_text[:n]
    n_tokens = tokenizer(tokenizer.decode(n_tokens))
    
    print(n_tokens)

    # Decode the tokens back to text
    extracted_text = tokenizer.decode(n_tokens.input_ids)

    # Truncate the original text
    truncated_text = text[len(extracted_text):]

    # Return the extracted tokens and truncated text
    return tuple([n_tokens, extracted_text, truncated_text])