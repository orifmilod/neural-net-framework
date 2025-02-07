import random
from gigatorch.tensor import Tensor


class Neuron:
    def __init__(self, number_of_input, nonlin=True) -> None:
        self.weights = [Tensor(random.uniform(-1, 1)) for _ in range(number_of_input)]
        self.bias = Tensor(random.uniform(-1, 1))
        self.nonlin = nonlin

    def __call__(self, x: Tensor) -> Tensor:
        total = sum((wi * xi for wi, xi in list(zip(self.weights, x))), Tensor(0)) + self.bias
        return total.tanh()

    def __repr__(self):
        return f"Weights:\n{self.weights} \nBias: \n{self.bias}\n"


class Layer:
    def __init__(self, number_of_inputs, number_of_neurons) -> None:
        self.number_of_inputs = number_of_inputs
        self.number_of_neurons = number_of_neurons

        self.neurons = [Neuron(number_of_inputs) for _ in range(number_of_neurons)]

    def __call__(self, x: Tensor) -> Tensor:
        return Tensor([neuron(x) for neuron in self.neurons])

    def __repr__(self):
        result = ""

        neuron_index = 0
        for neuron in self.neurons:
            neuron_index += 1
            result += f"Neuron {neuron_index}:\n{repr(neuron)}"
        return result


class MLP:
    """Multi Layered Perceptron"""

    def __init__(self, number_of_inputs, nuerons_per_layers, loss_fn, prob_fn) -> None:
        layers = [number_of_inputs] + nuerons_per_layers
        self.layers = [Layer(layers[i], layers[i + 1]) for i in range(len(nuerons_per_layers))]
        self.loss_fn = loss_fn
        self.prob_fn = prob_fn

    def __call__(self, x: Tensor) -> Tensor:
        for layer in self.layers:
            x = layer(x)
        return Tensor(x)

    def calc_loss(self, ys, y_pred):
        # Convertin y_pred to probabilities
        return sum(self.loss_fn(ys, y_pred), Tensor(0))

    def __repr__(self):
        result = ""

        for i in range(len(self.layers)):
            layer = self.layers[i]
            result += f"Layer {i + 1} with {len(layer.neurons)} neurons accepting {layer.number_of_inputs} inputs\n"
            result += repr(layer)
            result += "###########\n"

        return result
