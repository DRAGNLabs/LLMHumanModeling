import torch
from tqdm import tqdm

# from transformers import GPT2LMHeadModel, GPT2TokenizerFast
# model_id = "gpt2-large"
# model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
# tokenizer = GPT2TokenizerFast.from_pretrained(model_id)

# from datasets import load_dataset

# test = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
# encodings = tokenizer("\n\n".join(test["text"]), return_tensors="pt")

def get_ppl(model, tokenizer = None, text = None, tokens = None, device = torch.device("cuda" if torch.cuda.is_available() else "cpu")) -> float:
    encodings = tokens if tokens else tokenizer(text, return_tensors="pt")
    
    max_length = model.config.n_positions
    stride = 50
    # print(encodings)
    seq_len = encodings.input_ids.size(1)

    nlls = []
    prev_end_loc = 0
    for begin_loc in tqdm(range(0, seq_len, stride)):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc  # may be different from stride on last loop
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)

            # loss is calculated using CrossEntropyLoss which averages over input tokens.
            # Multiply it with trg_len to get the summation instead of average.
            # We will take average over all the tokens to get the true average
            # in the last step of this example.
            neg_log_likelihood = outputs.loss * trg_len

        nlls.append(neg_log_likelihood)

        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    return ppl.item()

# # Units test
# from transformers import AutoTokenizer
# from transformers import AutoModelForCausalLM

# model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)
# tokenizer = AutoTokenizer.from_pretrained("gpt2")

# tests = ["Hello, my dog is cute", "The quick brown fox jumps over the lazy dog."]

# for test in tests:
#     print(f"Test: {test}")
#     print(f"PPL: {get_ppl(model, tokenizer = tokenizer, text = test)}")