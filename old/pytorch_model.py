from __future__ import print_function
from sklearn.preprocessing import normalize

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.metrics import mean_absolute_error



class Net(nn.Module):
   def __init__(self):
       super(Net, self).__init__()
       self.layer1 = torch.nn.Linear(10, 50)
       self.layer2 = torch.nn.Linear(50, 1)
       #self.layer = torch.nn.Linear(10, 1)

   def forward(self, x):
       x = F.sigmoid(self.layer1(x))
       x = self.layer2(x)
       return x

net = Net()
print(net)

def normalize_exmaples(np_array):
    np_normed = np_array / np_array.max(axis = 0)
    return np_normed

def get_mean_absolute_error(y_list, y_hat_list):
    return mean_absolute_error(y_list, y_hat_list)



def main():
    x_np = np.loadtxt("model_data/train.csv", delimiter=",")
    x_np = normalize_exmaples(x_np)
    y_np = np.loadtxt("model_data/target_train.csv", delimiter=",")


    # Define Optimizer and Loss Function
    optimizer = torch.optim.Adam(net.parameters(), lr=0.05)
    loss_func = torch.nn.MSELoss()
    for i in range(100):
        x_np, y_np = shuffle(x_np, y_np)
        x = torch.from_numpy(x_np).float()
        y = torch.from_numpy(y_np).float()

        results = []
        for example, target in zip(x, y):
            input = Variable(example)
            output = Variable(target)
            prediction = net(input)
            results.append((output, prediction.item()))
            loss = loss_func(prediction, output)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    for real, pred in results:
        print("True value: {}, Predicted value: {}".format(real, pred))

    reals = [real for real, pred in results]
    preds = [pred for real, pred in results]
    print("MSE: {}".format(get_mean_absolute_error(reals, preds)))
        # if i % 1 == 0:
            #     # plot and show learning process
            #     plt.cla()
            #     plt.scatter(x.data.numpy(), y.data.numpy())
            #     plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=2)
            #     plt.text(0.5, 0, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size': 10, 'color': 'red'})
            #     plt.pause(0.1)

if __name__ == "__main__":
    main()