import torch
import torch.nn as nn
import torch.nn.functional as fun
import torch.utils.data as Data
import matplotlib.pyplot as plt


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        # self.layers = nn.Sequential(
        #     nn.Linear(3, 100),
        #     nn.ReLU(),
        #     nn.Linear(100, 100),
        #     nn.ReLU(),
        #     nn.Linear(100, 3)
        # )
        self.hidden1 = nn.Linear(3, 100)
        self.hidden2 = nn.Linear(100, 100)
        self.output = nn.Linear(100, 3)

    def forward(self, x):
        # return self.layers(x).squeeze()
        x = fun.relu(self.hidden1(x))
        x = fun.relu(self.hidden2(x))
        x = self.output(x)
        return x


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
    point = forward_kinematic(joints)
    return point, joints


loss_function = nn.L1Loss()
model = torch.load('model.pt')
points, joint = generate_data(1000)
test = Data.TensorDataset(points, joint)

test_loss = []
o, t = [], []
for (x, target) in test:
    output = model(x)
    loss = loss_function(output, target)
    test_loss.append(loss.item())
    o.append(torch.mean(output).item())
    t.append(torch.mean(target).item())

plt.plot(sorted(test_loss, reverse=True), marker='o', linestyle='--', color='lightskyblue',
         label='loss')
plt.legend()
plt.title("Test Loss")
plt.xlabel("Data(sorted)")
plt.ylabel("Loss")
plt.show()

# plt.title('Output-Target(test)')
# plt.xlabel('Target')
# plt.ylabel('Output')
# plt.plot([-1.5, 0.5], [-1.5, 0.5], label='y=t', color='orangered')
# plt.scatter(t, o, marker='o', c='white', edgecolors='black', label='test')
# plt.legend()
# plt.show()


