## Week 1: Introduction to LLMs and the generative AI project lifecycle
### Generative configuration:
* * greedy vs random sampling
* * top K: select an output from the top-k results after applying random-weighted strategy using the probabilities
* * top p: select an output using the random-weighted strategy with the top-ranked consecutive results by probability and with a cumulative probability <=p, [0,1]
* * Temperature: Cooler temperature (<1) strongly peaked probability distribution; Higher temperature (> 1) Broader, flatter probability distribution
### Generative AI project lifecylcle
* Scope: Define the use case
* Select: Choose an existing model or pretrain your own
* Adapt and align model: Prompt engineering, Fine-tuning, Align with human feedback => Evaluate
* Application integration: Optimize and deploy model for inference, Augment model and build LLM-powered applications
## Week 2: LLM pre-training and scaling laws
* Pre-training large language models:
* Encoder only models (Autoencoding models): Good use cases: Sentiment analysis, Named entity recognition, Word classification
* * Example models: BERT, ROBERTA
* Encoder Decoder models (Sequence-tosequence models): Good use cases: Translation, Text summarization, Question answering
* * Example models: T5, BART
* Decoder only models (Autoregressive models): Good use cases: Text generation, Other emergent behavior -> depends on model size
* * Example models: GPT, BLOOM