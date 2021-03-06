# -*- coding: utf-8 -*-
"""NeuralNetFromScratch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LNfXSlN5gthWYMTB30Ru1Nf24kZ_tHUA
"""

import torch
import torch.nn as nn

X = torch.tensor(([2,9],[1,5],[3,6]),dtype=torch.float) # 3x2 tensor
y = torch.tensor(([92],[100],[89]),dtype=torch.float) # 3X1 tensor
xPredicted = torch.tensor(([4,8]),dtype=torch.float) # 2X1 tensor

print(X.size())
print(y.size())

#Scale units
X_max, _ = torch.max(X,0) # dummy variable to capture and drop indices (we only need max value)
xPredicted_max, _ = torch.max(xPredicted,0)
#Dividing tensors
X = torch.div(X, X_max)
xPredicted = torch.div(xPredicted,xPredicted_max)
y = y /100 # max test score is 100

class Neural_Network(nn.Module):
  def __init__(self,):
    super(Neural_Network,self).__init__()
    #Parametres
    #TODO: parameters can be parameterized instead of declaring them here
    self.inputSize = 2
    self.outputSize = 1
    self.hiddenSize = 3
    self.intermediate = 3

    #weights
    self.W1 = torch.randn(self.inputSize, self.hiddenSize) # 2X3 tensor
    self.WI = torch.randn(self.hiddenSize,self.intermediate) # 3x3 tensor 
    self.W2 = torch.randn(self.intermediate,self.outputSize) # 3x1 tensor

  
  def forward(self, X):
    self.z = torch.matmul(X,self.W1) #3x3
    self.z2 = self.sigmoid(self.z) # activation function
    self.ZI = torch.matmul(self.z2,self.WI)
    self.zi1 = self.sigmoid(self.ZI)
    self.z3 = torch.matmul(self.zi1, self.W2)
    o = self.sigmoid(self.z3) # final activation
    return o
  
  def sigmoid(self,s):
    return 1 / (1+torch.exp(-s))

  def sigmoidPrime(self,s):
    #derivative of sigmoid
    return s * (1 - s)

  def backward(self, X, y, o):
    self.o_error = y - 0 #error in output
    self.o_delta = self.o_error * self.sigmoidPrime(o) # derivative of sigmoid to error
    self.ZI_error = torch.matmul(self.o_delta,torch.t(self.W2))
    self.ZI_delta = self.ZI_error * self.sigmoidPrime(self.ZI) # derivative of inter hidden layer
    self.z2_error = torch.matmul(self.ZI_delta,torch.t(self.WI)) # error of 1 hidden layer
    self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2) # derivative of 1 hidden layer
    self.W1 += torch.matmul(torch.t(X), self.z2_delta) 
    self.WI += torch.matmul(torch.t(self.z2),self.ZI_delta)
    self.W2 += torch.matmul(torch.t(self.zi1), self.o_delta)

  def train(self, X,y):
    #forward + backward pass for training
    o = self.forward(X)
    self.backward(X,y,o)

  def saveWeights(self,model):
    #we will use the pytorch internal storage function
    torch.save(model, 'NN')
    # you can reload model with all the weights and so forth with:
    # torch.load('NN')

  def predict(self):
    print('Predicted data based on trained weights :')
    print('Input (scaled): \n' + str(xPredicted))
    print('Output: \n'+ str(self.forward(xPredicted)))

#Training process
NN = Neural_Network()
for i in range(1000):
  print('#'+str(i)+" Loss: " + str(torch.mean((y-NN(X))**2).detach().item()))
  NN.train(X,y)
NN.saveWeights(NN)
NN.predict()