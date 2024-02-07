# Code and Data Repository for 'Large-Scale Text Analysis Using Generative Language Models: A Case Study in Discovering Public Value Expressions in AI Patents'  
## In [Quantitative Science Studies (QSS)](https://direct.mit.edu/qss/article/doi/10.1162/qss_a_00285/119275)

## by [Sergio Pelaez*](https://www.linkedin.com/in/sergio-pel%C3%A1ez-sierra-148690147/), [Gaurav Verma*](https://gaurav22verma.github.io/), [Barbara Ribeiro](https://www.linkedin.com/in/drbarbararibeiro), [Philip Shapira<sup>1</sup>](https://iac.gatech.edu/people/person/pshapira)
### * = Co-First authors; <sup>1</sup> Corresponding author: pshapira@manchester.ac.uk

We provide the code used to make API calls to GPT-4 for obtaining labels and rationales for 10,000 sentences sampled from the patent documents. The code contains the instructions as well as the examples supplied to GPT-4 as part of the prompt.

# Code using GPT-4 for labeling and obtaining rationales for 10,000 sentences
Check the file `gpt-4_script.py` that loads the `10k_sentences_to_annotate.csv` file and calls GPT-4 to obtain their labels and rationales. The file contains the instruction provided to GPT-4 (line 27-31) and the final 14 examples along with their rationales (lines 33-73). The API calls to GPT-4 are made sentence by sentence, and the generated labels and rationales are parsed and stored in a python pickle file for later use and analysis. We use `python3` for all our scripts.

# Data: 10k sentences, their generated labels, and rationales

**10k sentences**: The ~10,000 sentences that were labeled using GPT-4 are availabe in `10k_sentences_to_annotated.csv` under the `./data` subdirectory. The sampling strategy for obtaining these 10k sentences is discusses in the preprint. 

**Labels and rationales**: We have stored the labels and rationales generated by GPT-4 for these sentences in a python3 pickle file `10k_responses_gpt4.pkl` under the `./data` subdirectory. For ease of viewing and interacting with the data, we have also reformmated the pickle file into an Excel spreadsheet, which is available as `10k_responses_gpt4.xlsx` under the `./data` subdirectory. Alternatively, you can use the script called `read_responses.py` to directly read the labels and ratinales from the pickle file. The script stores the responses in form of a dictionary of dictionaries, with the sentences (`str`) as the key and `rationale` and `label` as the the subkeys. 

# Citation
If you use the code and data in this repository, please cite the following QSS paper:

Sergio Pelaez, Gaurav Verma, Barbara Ribeiro, Philip Shapira; Large-scale text analysis using generative language models: A case study in discovering public value expressions in AI patents. Quantitative Science Studies 2024; doi: https://doi.org/10.1162/qss_a_00285

**Bibtex**

```
@article{generative_language_models_for_public_values,
    author = {Pelaez, Sergio and Verma, Gaurav and Ribeiro, Barbara and Shapira, Philip},
    title = "{Large-scale text analysis using generative language models: A case study in discovering public value expressions in AI patents}",
    journal = {Quantitative Science Studies},
    pages = {1-26},
    year = {2024},
    month = {02},
    issn = {2641-3337},
    doi = {10.1162/qss_a_00285},
    url = {https://doi.org/10.1162/qss\_a\_00285},
    eprint = {https://direct.mit.edu/qss/article-pdf/doi/10.1162/qss\_a\_00285/2325312/qss\_a\_00285.pdf},
}
```
