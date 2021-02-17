import numpy as np, matplotlib.pyplot as plt
import urllib.request
link1 = 'https://dl.dropbox.com/s/q4bs7q0twqq5zi5/mnist_training.npy?dl=0'
link2 = 'https://dl.dropbox.com/s/yfc0i8masrxp6x7/mnist_valid.npy?dl=0'
link3 = 'https://dl.dropbox.com/s/l62r00kfjpsil74/mnist_test.npy?dl=0'
urllib.request.urlretrieve(link1,'mnist_training.npy')
urllib.request.urlretrieve(link2,'mnist_valid.npy')
urllib.request.urlretrieve(link3,'mnist_test.npy')
training = np.load('mnist_training.npy')
valid = np.load('mnist_valid.npy')
test = np.load('mnist_test.npy')

def ReLU(x):
  return( np.maximum(0,x))

def SOFTMAX(x):
  dummy = np.exp(x)
  return( dummy/np.sum(dummy, axis = 0))

def E(d,z):
  return(-np.sum(d*np.log(z) + (1.0-d)*np.log(1.0-z)))

def theta(x):
  return(np.heaviside(x,1.0))

N = np.shape(training)[0] # N = number of image data in training set
Nvalid = np.shape(valid)[0] # N = number of image data in validation set
Ntest = np.shape(test)[0] # N = number of image data in test set

Ni = 784 # number of nodes in input layer = number of pixels in one image data
No = 4 # number of nodes in output layer. 0, 1, 2, ..... 9 
Nh = 100 # number of nodes in hidden layer

alpha = 1.0 # learning rate
Nep = 20 # number of epochs

W = np.random.random( (Nh,Ni) )*0.01 # random weights
V = np.random.random( (No,Nh) )*0.01 # random weights
b = np.random.random( (Nh, 1) )*0.01
c = np.random.random( (No, 1) )*0.01

d = np.zeros( (No, N) )
d_valid = np.zeros( (No, Nvalid) )

label = training[:,0].astype('int')
for n in range(N):
  if (label[n] // 8):
    d[0, n] = 1
  if (label[n] % 8 // 4):
    d[1, n] = 1
  if (label[n] % 4 // 2):
    d[2, n] = 1
  if (label[n] % 2):
    d[3, n] = 1

label_valid = valid[:,0].astype('int')
for n in range(Nvalid):
  if (label_valid[n] // 8):
    d_valid[0, n] = 1
  if (label_valid[n] % 8 // 4):
    d_valid[1, n] = 1
  if (label_valid[n] % 4 // 2):
    d_valid[2, n] = 1
  if (label_valid[n] % 2):
    d_valid[3, n] = 1

x = (training[:,1:]/255.).T
x_valid = (valid[:,1:]/255.).T
x_test = (test[:,1:]/255.).T

alpha_N = alpha/N 

xarr = []
yarr1 = []
yarr2 = []

for ep in range(Nep):
  v = W@x + b
  y = ReLU(v)
  s = V@y + c
  z = SOFTMAX(s)

  delta = d - z
  eps = (V.T@delta)*theta(v)

  V += alpha_N*(delta@y.T)
  W += alpha_N*(eps@x.T)
  c += alpha_N*np.sum(delta,axis=1).reshape( (No, 1))
  b += alpha_N*np.sum(eps, axis = 1).reshape( (Nh, 1))

  if ( ep % 10 == 0):
    xarr.append(ep)
    yarr1.append(E(d,z)/N)

    v = W@x_valid + b
    y = ReLU(v)
    s = V@y + c
    z = SOFTMAX(s)

    yarr2.append(np.mean(np.argmax(z, axis = 0) == np.argmax(d_valid,axis =0)))
    print(xarr[-1], yarr2[-1])

plt.plot(xarr, yarr1)
plt.show()
plt.plot(xarr,yarr2)
plt.show()

v = W@x_test + b
y = ReLU(v)
s = V@y + c
z = SOFTMAX(s)

for n in range(5):
  image = x_test[:,n].reshape([28,28])/256.0
  plt.imshow(image)
  plt.show()
  print("This image looks like ",np.argmax(z[:,n]))
  if (z[0, n] > 0.5):
    print("1")
  if (z[1, n] > 0.5):
    print("1")
  if (z[2, n] > 0.5):
    print("1")
  if (z[3, n] > 0.5):
    print("1")