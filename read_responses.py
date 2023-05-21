import pickle as pkl
import pandas as pd

# open a pikcle file and read the responses that were appended to it until there are no more responses to read
def read_responses(file_name):
    responses = []
    with open(file_name, 'rb') as f:
        while True:
            try:
                responses.append(pkl.load(f))
            except EOFError:
                break
    return responses

responses = read_responses('data/10k_responses_gpt4.pkl')

# dictionary with sent as the key and rationale and label as the values
sent_rationale_label = {}
for response in responses:
    if response[0] not in sent_rationale_label:
        sent = response[0]
        sent_rationale_label[sent] = {}
        sent_rationale_label[sent]['rationale'] = response[1]
        sent_rationale_label[sent]['label'] = response[2]
print("number of entries in the dictionary: ", len(sent_rationale_label))