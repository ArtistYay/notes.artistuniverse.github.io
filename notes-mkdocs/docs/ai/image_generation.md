---
tags:
  - Generative AI
---

## How do diffusion models make images?

Image generation works totally differently from text generation. Most image models are diffusion models.

During training, the model takes a clean image and adds random static (Gaussian noise) step by step until the picture is unrecognizable. It learns how to undo each of those steps.

When you generate an image, it starts from pure noise and removes it a little at a time, using your prompt to steer what shows up. You're basically watching it pull a picture out of static.

Most modern models, like Stable Diffusion, don't do this on every pixel. They work on a compressed version of the image (latent space), which is a lot cheaper, and then decode it back into a full image at the end.

## Why does this matter for security?

Deepfakes. The same tech makes it cheap to fake a face or a voice, and attackers are already using it for social engineering. In 2024 an employee at the engineering firm Arup was tricked into sending about $25 million after a video call where the "CFO" and other coworkers were all deepfakes. Out-of-band verification (calling back on a known number) matters more than ever.
