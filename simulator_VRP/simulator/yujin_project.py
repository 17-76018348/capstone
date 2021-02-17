import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
 
class NN:
    def __init__(self):
        self.W = np.random.uniform(low=-0.01, high=0.01, size=(784, 10))
        self.b = np.zeros(10)
        self.learningRate = 0.001
 
    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))
 
    def softmax(self, x):
        if x.ndim == 1:
            x = x.reshape([1, x.size])
        modifiedX = x -  np.max(x, 1).reshape([x.shape[0],1]);
        sigmoid = np.exp(modifiedX)
        return sigmoid/np.sum(sigmoid,axis=1).reshape([sigmoid.shape[0],1]);
 
    def getCrossEntropy(self, predictY, labelY):
        return np.mean(-np.sum(labelY * np.log(self.softmax(predictY)), axis=1))
 
    def feedForward(self, x):
        y = np.dot(x, self.W) + self.b
        softmaxY = self.softmax(y)
        return softmaxY
 
    def backpropagation(self, x, labelY, y):
        dW = x.T.dot(y - labelY)
        return dW
 
    def update(self, dW):
        self.W -= self.learningRate * dW
 
 
if __name__ == '__main__':
 
    mnist = input_data.read_data_sets('/tmp/tensorflow/mnist/input_data', one_hot=True)
 
    np.random.seed(777)
 
    NN = NN()
 
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        y = NN.feedForward(batch_xs)
        dW = NN.backpropagation(batch_xs, batch_ys, y)
        NN.update(dW)
 
 
    y = NN.feedForward(mnist.test.images)
    correct_prediction = np.equal(np.argmax(y, 1), np.argmax(mnist.test.labels, 1))
    accuracy = np.mean(correct_prediction)
    print(accuracy)