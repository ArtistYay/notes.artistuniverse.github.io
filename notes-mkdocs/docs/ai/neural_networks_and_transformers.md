---
tags:
  - Generative AI
---

## What is a neural network?

A neural network is a bunch of connected nodes (neurons) stacked in layers. Data goes in one side, gets passed through the layers, and a prediction comes out the other side.

## How does a neural network learn?

Two things get adjusted while it learns: weights and biases.

Weights are like volume knobs on every connection between neurons. Turn one up and that connection matters more, turn it down and it matters less. Biases are extra numbers added at each neuron that shift the output, kind of like a starting baseline.

Learning happens in a loop:

1. Forward pass: the input runs through the network and it makes a prediction.
2. Loss: the prediction gets compared to the right answer. How far off it was is the loss (error).
3. Backpropagation: the network works backward through the layers to figure out how much each weight contributed to that error.
4. Gradient descent: every weight and bias gets nudged a tiny bit in whatever direction lowers the error.

That loop runs over and over on a huge amount of training data. Today's LLMs have billions of these weights, which is why you'll see them called "parameters" (like a 70B model = 70 billion parameters).

## What is a transformer and why did 2017 change everything?

Before 2017, language models mostly used recurrent neural networks (RNNs and LSTMs). They read a sentence one word at a time, in order. That's slow because you can't run it in parallel, and by the end of a long paragraph the model has kind of forgotten how it started.

In 2017 Google researchers published "Attention Is All You Need," which introduced the transformer. The main trick is self-attention: every token looks at every other token in the input at the same time and figures out which ones matter to it.

That's how a model knows "bank" means something different in "river bank" vs "bank account." And since it all happens at once instead of word by word, it runs really well on GPUs, which is a big reason models were able to get so large.

The original transformer had two halves. The encoder reads and understands the input, and the decoder generates the output. Most models today only use one half:

- Encoder-only, like BERT. Good at understanding tasks like classification and search.
- Decoder-only, like GPT, Claude, and Llama. Good at generating text, which is what every chatbot does.

[Documentation | arXiv](https://arxiv.org/abs/1706.03762) - The original "Attention Is All You Need" paper.
