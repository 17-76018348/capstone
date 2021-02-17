import numpy as np 

def sigmoid(x):
    return 1/(1+np.exp(-x))

x = np.array([[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]])
y = np.array([1,0,0,1,0,1,1,0])
theta3 = 1
theta2 = 1
theta1 = 1

theta0 = 1

lr = 0.1
for i in range(10000):
    error_sum = 0
    for j in range(8):
        output = sigmoid(np.sum(theta3 * )+b)
        error = y[j][0] - output 
        w = w + x[j] * lr * error 
        b = b + lr * error 
        error_sum += error 
    if i % 1000 == 999:
        print(i, error_sum)

