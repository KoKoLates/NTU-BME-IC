import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torch.nn.functional as fun
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
from torch.optim.lr_scheduler import MultiStepLR


def forward_kinematic(joints):
    q1 = joints[:, 0:1]
    q2 = joints[:, 1:2]
    q3 = joints[:, 2:3]
    a1, a2, a3, a4 = 0, 135, 147, 61
    c1 = torch.cos(q1)
    c2 = torch.cos(q2)
    c23 = torch.cos(q2 + q3)
    s1 = torch.sin(q1)
    s2 = torch.sin(q2)
    s23 = torch.sin(q2 + q3)

    dx = c1 * (a3 * c23 + a2 * c2 + a4)
    dy = s1 * (a3 * c23 + a2 * c2 + a4)
    dz = -a2 * s2 - a3 * s23
    point = torch.hstack([dx, dy, dz])
    return point


def generate_data(train_num):
    joint1 = (-torch.pi/2) + torch.pi * torch.rand(train_num, 1)
    joint2 = (-85 * torch.pi/180) + (85 * torch.pi/180) * torch.rand(train_num, 1)
    joint3 = (-105 * torch.pi/180) + (105 * torch.pi/180) * torch.rand(train_num, 1)
    joints = torch.hstack((joint1, joint2, joint3))
    points = forward_kinematic(joints)
    return points, joints


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(3, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 3)
        )
        # self.hidden1 = nn.Linear(3, 100)
        # self.hidden2 = nn.Linear(100, 100)
        # self.output = nn.Linear(100, 3)

    def forward(self, x):
        return self.layers(x).squeeze()
        # x = fun.relu(self.hidden1(x))
        # x = fun.relu(self.hidden2(x))
        # x = self.output(x)
        # return x


def main():
    # writer = SummaryWriter("./logs/202204070110")
    data_number = 500000
    train_size, valid_size, test_size = int(data_number*0.7), int(data_number*0.2), int(data_number*0.1)
    x_train, y_train = generate_data(data_number)
    train, valid, test = data.random_split(data.TensorDataset(x_train, y_train),
                                           [train_size, valid_size, test_size])
    train_loader = data.DataLoader(train, batch_size=700, shuffle=True, num_workers=4)
    valid_loader = data.DataLoader(valid, batch_size=200, shuffle=True, num_workers=4)

    model = Model()
    loss_function = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    train_loss, valid_loss = [], []
    for epoch in range(100):
        for (x, target) in train_loader:
            optimizer.zero_grad()
            output = model(x)
            loss = loss_function(output, target)
            loss.backward()
            optimizer.step()
            train_loss.append(loss.item())

        model.eval()
        # writer.add_scalar('Train Loss', train_loss[epoch], epoch)

        for (x, target) in valid_loader:
            output = model(x)
            loss = loss_function(output, target)
            valid_loss.append(loss.item())

        # writer.add_scalar('Valid Loss', valid_loss[epoch], epoch)
        print("Epoch:{} Training Loss:{} valid Loss:{}".format
              (epoch, np.mean(train_loss), np.mean(valid_loss)))
    # torch.save(model, 'model.pt')

    test_loss = []
    for (x, target) in test:
        output = model(x)
        loss = loss_function(output, target)
        test_loss.append(loss.item())


if __name__ == '__main__':
    main()
