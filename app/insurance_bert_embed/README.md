---
license: apache-2.0  
inference: false  
---
# industry-bert-insurance-v0.1

<!-- Provide a quick summary of what the model is/does. -->

industry-bert-insurance-v0.1 is part of a series of industry-fine-tuned sentence_transformer embedding models.   

### Model Description

<!-- Provide a longer summary of what this model is. -->

industry-bert-insurance-v0.1 is a domain fine-tuned BERT-based 768-parameter Sentence Transformer model, intended to as a "drop-in" 
substitute for embeddings in the insurance industry domain.   This model was trained on a wide range of publicly available documents on the insurance industry.

- **Developed by:** llmware
- **Model type:** BERT-based Industry domain fine-tuned Sentence Transformer architecture
- **Language(s) (NLP):** English
- **License:** Apache 2.0
- **Finetuned from model [optional]:** BERT-based model, fine-tuning methodology described below.

## Model Use

from transformers import AutoTokenizer, AutoModel  

tokenizer = AutoTokenizer.from_pretrained("llmware/industry-bert-insurance-v0.1")  

model = AutoModel.from_pretrained("llmware/industry-bert-insurance-v0.1")  



## Bias, Risks, and Limitations

This is a semantic embedding model, fine-tuned on public domain documents about the insurance industry.   Results may vary if used outside of this
domain, and like any embedding model, there is always the potential for anomalies in the vector embedding space.   No specific safeguards have
put in place for safety or mitigate potential bias in the dataset.

### Training Procedure 

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

This model was fine-tuned using a custom self-supervised procedure and custom dataset that combined contrastive techniques 
with stochastic injections of distortions in the samples.  The methodology was derived, adapted and inspired primarily from 
three research papers cited below:  TSDAE (Reimers), DeClutr (Giorgi), and Contrastive Tension (Carlsson).


## Citation [optional]

Custom self-supervised training protocol used to train the model, which was derived and inspired by the following papers:

@article{wang-2021-TSDAE,
    title = "TSDAE: Using Transformer-based Sequential Denoising Auto-Encoderfor Unsupervised Sentence Embedding Learning",
    author = "Wang, Kexin and Reimers, Nils and  Gurevych, Iryna", 
    journal= "arXiv preprint arXiv:2104.06979",
    month = "4",
    year = "2021",
    url = "https://arxiv.org/abs/2104.06979",
}

@inproceedings{giorgi-etal-2021-declutr,
    title        = {{D}e{CLUTR}: Deep Contrastive Learning for Unsupervised Textual Representations},
    author       = {Giorgi, John  and Nitski, Osvald  and Wang, Bo  and Bader, Gary},
    year         = 2021,
    month        = aug,
    booktitle    = {Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)},
    publisher    = {Association for Computational Linguistics},
    address      = {Online},
    pages        = {879--895},
    doi          = {10.18653/v1/2021.acl-long.72},
    url          = {https://aclanthology.org/2021.acl-long.72}
}

@article{Carlsson-2021-CT,
      title =  {Semantic Re-tuning with Contrastive Tension},
      author=  {Fredrik Carlsson, Amaru Cuba Gyllensten, Evangelia Gogoulou, Erik Ylipää Hellqvist, Magnus Sahlgren},
        year=  {2021},
        month= {"January"}
    Published: 12 Jan 2021, Last Modified: 05 May 2023
}

<!-- If there is a paper or blog post introducing the model, the APA and Bibtex information for that should go in this section. -->


## Model Card Contact

Darren Oberst @ llmware


