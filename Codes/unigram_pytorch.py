"""Pytorch."""
import nltk
import numpy as np
from numpy.typing import NDArray
import torch
from typing import List, Optional
from torch import nn
import matplotlib.pyplot as plt

FloatArray = NDArray[np.float64]


def onehot(vocabulary: List[Optional[str]], token: Optional[str]) -> FloatArray:
    """Generate the one-hot encoding for the provided token in the provided vocabulary."""
    embedding = np.zeros((len(vocabulary), 1))
    try:
        idx = vocabulary.index(token)
    except ValueError:
        idx = len(vocabulary) - 1
    embedding[idx, 0] = 1
    return embedding


def logit(x: FloatArray) -> FloatArray:
    """Compute logit (inverse sigmoid)."""
    return np.log(x) - np.log(1 - x)


def normalize(x: torch.Tensor) -> torch.Tensor:
    """Normalize vector so that it sums to 1."""
    return x / torch.sum(x)


def loss_fn(p: float) -> float:
    """Compute loss to maximize probability."""
    return -p


class Unigram(nn.Module):
    def __init__(self, V: int):
        super().__init__()

        # construct initial s - corresponds to uniform p
        s0 = logit(np.ones((V, 1)) / V)
        self.s = nn.Parameter(torch.tensor(s0.astype("float32")))

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        # convert s to proper distribution p
        p = normalize(torch.sigmoid(self.s))

        # compute log probability of input
        return torch.sum(input, 1, keepdim=True).T @ torch.log(p)


def gradient_descent_example():
    """Demonstrate gradient descent."""
    # generate vocabulary
    vocabulary = [chr(i + ord("a")) for i in range(26)] + [" ", None]

    # generate training document
    text = nltk.corpus.gutenberg.raw("austen-sense.txt").lower()

    # tokenize - split the document into a list of little strings
    tokens = [char for char in text]

    # generate one-hot encodings - a V-by-T array
    encodings = np.hstack([onehot(vocabulary, token) for token in tokens])

    # convert training data to PyTorch tensor
    x = torch.tensor(encodings.astype("float32"))

    # define model
    model = Unigram(len(vocabulary))
    # print(type(encodings))
    # print(encodings)
    print(encodings.shape)
    temp_array = np.sum(encodings, 1, keepdims=True)
    temp = 0
    probabilities = np.array([])
    for i in range(temp_array.size):
        temp += temp_array[i] / encodings.shape[1]
        print(
            i,
            temp_array[i],
            temp_array[i] / encodings.shape[1],
            np.log(temp_array[i] / encodings.shape[1]),
        )
        probabilities = np.append(probabilities, temp_array[i] / encodings.shape[1])
    print(encodings.shape[0])
    print(encodings.shape[1])
    print(temp)
    print(probabilities)
    log_probabilities = np.log(probabilities)
    print(log_probabilities)
    known_min_probability = probabilities.T @ log_probabilities
    print(known_min_probability)
    # print(np.log(known_min_probability))
    # print(np.log(known_min_probability) - np.log(1 - known_min_probability))
    print((logit(loss_fn(-known_min_probability))))
    # set number of iterations and learning rate
    num_iterations = 1000  # SET THIS
    learning_rate = 0.01  # SET THIS

    # initialize lists to store loss and iteration values
    losses = []
    iterations = []
    # train model
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    for _ in range(num_iterations):
        p_pred = model(x)
        loss = -p_pred
        loss.backward(retain_graph=True)
        optimizer.step()
        optimizer.zero_grad()
        # append loss and iteration values to lists
        losses.append(loss.item())
        # print(loss.item())
        iterations.append(_)

    # print(min_loss)
    # print(min_loss_item)
    # display results
    # plot loss as a function of iterations
    print(losses)
    plt.plot(iterations, losses)
    plt.axhline(y=known_min_probability, color="r", linestyle="--")
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.show()
    # print(model.s)
    # print(len(model.s))
    # print(model.s[0])
    # print(model.s[0].item())
    model_parameters = np.array([])
    for i in range(len(model.s)):
        # print(model.s[i].item())
        model_parameters = np.append(model_parameters, model.s[i].item())
    model_parameters
    model_parameters_sigmoid_normalized = normalize(model.s)
    # print(model_parameters_sigmoid_normalized)
    for i in range(len(model_parameters_sigmoid_normalized)):
        print(
            np.log(model_parameters_sigmoid_normalized[i].item()),
            # np.log(-model_parameters_sigmoid_normalized[i].item()),
            np.log(model_parameters_sigmoid[i].item()),
            # np.log(-model_parameters_sigmoid[i].item()),
            logit(model_parameters_sigmoid_normalized[i].item()),
            # logit(-model_parameters_sigmoid_normalized[i].item()),
            logit(model_parameters_sigmoid[i].item()),
            logit(-model_parameters_sigmoid[i].item()),
        )


if __name__ == "__main__":
    gradient_descent_example()
