import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as fuzzy_ctrl
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from mpl_toolkits.mplot3d import Axes3D

error_function = [[-35, -35, -30, -25],
                  [-28, -23, -18],
                  [-22, -17, -12],
                  [-16, -11, -6],
                  [-10, -5, 0, 0]]

humid_function = [[20, 20, 25, 40],
                  [25, 40, 55],
                  [40, 55, 70],
                  [55, 70, 85],
                  [70, 85, 90, 90]]

time_function = [[0, 0, 1, 3],
                 [2, 4, 6, 8],
                 [7, 9, 10, 10]]

error_range = np.arange(-35, 1, 1, np.float32)
humid_range = np.arange(20, 91, 1, np.float32)
time_range = np.arange(0, 11, 1, np.float32)
error = fuzzy_ctrl.Antecedent(error_range, "error")
humid = fuzzy_ctrl.Antecedent(humid_range, "humid")
time = fuzzy_ctrl.Consequent(time_range, "time")

error["huge"] = fuzzy.trapmf(error_range, error_function[0])
error["large"] = fuzzy.trimf(error_range, error_function[1])
error["high"] = fuzzy.trimf(error_range, error_function[2])
error["low"] = fuzzy.trimf(error_range, error_function[3])
error["few"] = fuzzy.trapmf(error_range, error_function[4])

humid["arid"] = fuzzy.trapmf(humid_range, humid_function[0])
humid["dry"] = fuzzy.trimf(humid_range, humid_function[1])
humid["normal"] = fuzzy.trimf(humid_range, humid_function[2])
humid["moist"] = fuzzy.trimf(humid_range, humid_function[3])
humid["wet"] = fuzzy.trapmf(humid_range, humid_function[4])

time["short"] = fuzzy.trapmf(time_range, time_function[0])
time["medium"] = fuzzy.trapmf(time_range, time_function[1])
time["long"] = fuzzy.trapmf(time_range, time_function[2])

rule_short = fuzzy_ctrl.Rule((humid["arid"] & error["few"]) |
                             (humid["arid"] & error["low"]) |
                             (humid["arid"] & error["high"]) |
                             (humid["arid"] & error["large"]) |
                             (humid["dry"] & error["few"]) |
                             (humid["dry"] & error["low"]) |
                             (humid["normal"] & error["few"]) |
                             (humid["moist"] & error["few"]), time["short"], "short")

rule_medium = fuzzy_ctrl.Rule((humid["arid"] & error["large"]) |
                              (humid["arid"] & error["huge"]) |
                              (humid["dry"] & error["high"]) |
                              (humid["dry"] & error["large"]) |
                              (humid["dry"] & error["huge"]) |
                              (humid["normal"] & error["low"]) |
                              (humid["normal"] & error["high"]) |
                              (humid["normal"] & error["large"]) |
                              (humid["moist"] & error["few"]) |
                              (humid["moist"] & error["low"]) |
                              (humid["moist"] & error["high"]) |
                              (humid["wet"] & error["few"]) |
                              (humid["wet"] & error["low"]), time["medium"], "medium")


rule_long = fuzzy_ctrl.Rule((humid["dry"] & error["huge"]) |
                            (humid["normal"] & error["huge"]) |
                            (humid["moist"] & error["large"]) |
                            (humid["moist"] & error["huge"]) |
                            (humid["wet"] & error["low"]) |
                            (humid["wet"] & error["high"]) |
                            (humid["wet"] & error["large"]) |
                            (humid["wet"] & error["huge"]), time["long"], "long")

time.defuzzify_method = "centroid"
system = fuzzy_ctrl.ControlSystem([rule_long, rule_medium, rule_short])
simulation = fuzzy_ctrl.ControlSystemSimulation(system)

data = [[], []]
humidity = 90
temperature = 40
sample_time = 1
expect_temp = int(input("Expect temp: "))
t = int()
while error != 0 or humidity != 0:
    error = expect_temp - temperature
    simulation.input['error'] = error
    simulation.input['humid'] = humidity
    simulation.compute()
    output = simulation.output['time']
    t += 1
    print(error, humidity, output)
    data[1].append(output)
    data[0].append(t)
    if temperature > expect_temp: temperature += (-1 * sample_time)
    if humidity > 0: humidity += (-1 * sample_time)
#
# model = make_interp_spline(data[0], data[1])
# xs = np.linspace(1, t, 500)
# ys = model(xs)
# plt.plot(xs, ys, color='darkslategrey')
# plt.xlabel('Operating Time')
# plt.ylabel('Expect Running Time')
# plt.text(50, 5, 'Initial humidity:90\nInitial temperature:40\nExpect temperature:5\n')
# plt.show()

def fun(x, y):
    simulation.input["error"] = x
    simulation.input["humid"] = y
    simulation.compute()
    z = simulation.output["time"]
    return z


fig, (error_fig, humid_fig, time_fig) = plt.subplots(nrows=3, figsize=(6, 6))
error_fig.plot(error_range, fuzzy.trapmf(error_range, error_function[0]), 'b', linewidth=1.5, label='huge')
error_fig.plot(error_range, fuzzy.trimf(error_range, error_function[1]), 'g', linewidth=1.5, label='large')
error_fig.plot(error_range, fuzzy.trimf(error_range, error_function[2]), 'r', linewidth=1.5, label='high')
error_fig.plot(error_range, fuzzy.trimf(error_range, error_function[3]), 'y', linewidth=1.5, label='low')
error_fig.plot(error_range, fuzzy.trapmf(error_range, error_function[4]), 'k', linewidth=1.5, label='few')
error_fig.legend()

humid_fig.plot(humid_range, fuzzy.trapmf(humid_range, humid_function[0]), 'b', linewidth=1.5, label='arid')
humid_fig.plot(humid_range, fuzzy.trimf(humid_range, humid_function[1]), 'g', linewidth=1.5, label='dry')
humid_fig.plot(humid_range, fuzzy.trimf(humid_range, humid_function[2]), 'r', linewidth=1.5, label='normal')
humid_fig.plot(humid_range, fuzzy.trimf(humid_range, humid_function[3]), 'y', linewidth=1.5, label='moist')
humid_fig.plot(humid_range, fuzzy.trapmf(humid_range, humid_function[4]), 'k', linewidth=1.5, label='wet')
humid_fig.legend()

time_fig.plot(time_range, fuzzy.trapmf(time_range, time_function[0]), 'b', linewidth=1.5, label='short')
time_fig.plot(time_range, fuzzy.trapmf(time_range, time_function[1]), 'g', linewidth=1.5, label='medium')
time_fig.plot(time_range, fuzzy.trapmf(time_range, time_function[2]), 'r', linewidth=1.5, label='long')
time_fig.legend()

for i in (error_fig, humid_fig, time_fig):
    i.spines['top'].set_visible(False)
    i.spines['right'].set_visible(False)
    i.get_xaxis().tick_bottom()
    i.get_yaxis().tick_left()

fig_3D = plt.figure()
ax = Axes3D(fig_3D)
X, Y = np.meshgrid(error_range, humid_range)
Z = fun(X, Y)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm)
ax.set_xlabel("temperature error", color='g')
ax.set_ylabel("moisture", color='r')
ax.set_zlabel("time", color='b')

plt.tight_layout()
plt.show()

