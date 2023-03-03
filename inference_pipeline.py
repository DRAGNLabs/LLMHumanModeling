from lib2to3.pgen2 import token
import random
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import torch.nn.functional as F
import sys, argparse

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

parser = argparse.ArgumentParser(
    prog="clm inference pipeline cli tool",
    description="A foo that bars",
    epilog="Amd that's how you'd foo a bar",
)

parser.add_argument("checkpoint", default="pretrained/lds_hymnal_dgpt2/", nargs="?")
parser.add_argument("num_return_sequences", type=int, default=5, nargs="?")
parser.add_argument("max_sequence_length", type=int, default=211, nargs="?")
parser.add_argument("text", default="""""", nargs="?")
parser.add_argument("--many", "-m", action="extend", nargs="+")

cliArgs = parser.parse_args()
print(cliArgs)

model = AutoModelForCausalLM.from_pretrained(cliArgs.checkpoint)
tokenizer = AutoTokenizer.from_pretrained(cliArgs.checkpoint)

thing = tokenizer(cliArgs.text)
print(thing)

generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=device)

results = generator(cliArgs.text if cliArgs.many == None else cliArgs.many, max_length=cliArgs.max_sequence_length, num_return_sequences=cliArgs.num_return_sequences, pad_token_id=50256)

for result in results:
    if cliArgs.many == None:
        print("\n\n" + result['generated_text'])
    else:
        for res in result:
            print("\n" + res["generated_text"])
        print("\n")

# generator = pipeline('fill-mask', model=model, tokenizer=tokenizer, device=device)

# results = generator(cliArgs.text if cliArgs.many == None else cliArgs.many)

# print(results)

# def main():
#     tokenized_input = tokenizer([cliArgs.text] if cliArgs.many == None else cliArgs.many, return_tensors="pt")
#     print("".join(tokenizer.batch_decode(tokenized_input["input_ids"])))
#     tokenized_input = {
#         "input_ids": torch.tensor([[*tokenized_input.input_ids[0]]]),
#         "attention_mask": torch.tensor([[*tokenized_input.attention_mask[0]]])
#     }
    
#     print(tokenized_input)

#     while len(tokenized_input["input_ids"][0]) <= 200:
#         raw_results = None

#         with torch.no_grad():
#             raw_results = model(**tokenized_input)

#         logits = raw_results.logits
        
#         force_continue_tokens = (198, 50256)
        
#         # label_encoding = random.choice(torch.topk(logits[0][-1], 10).indices)
#         cdf = 0
#         topk = torch.topk(logits[0][-1].softmax(0), 200, sorted=True)
#         #label_encoding = random.choice(list(topk.indices[0:next(i for i, prob in enumerate(topk.values) if (cdf > .5 or i == len(topk.values) - 1, cdf := cdf + prob)[0])]))
        
        
#         print(label_encoding, logits[0][-1])
#         print(tokenized_input)
#         tokenized_input = {
#             "input_ids": torch.tensor([[*tokenized_input["input_ids"][0], label_encoding]]),
#             "attention_mask": torch.tensor([[*tokenized_input["attention_mask"][0], 1]])
#         }
        
#         print("".join(tokenizer.batch_decode(tokenized_input["input_ids"])))

#     # results = [tokenizer.batch_decode(logit) for logit in label_encodings]
#     results = ["".join(tokenizer.batch_decode(tokenized_input["input_ids"]))]

#     for result in results:
#         if cliArgs.many == None:
#             print("\n\n" + result)
#         else:
#             for res in result:
#                 print("\n" + res)
#             print("\n")

# main()