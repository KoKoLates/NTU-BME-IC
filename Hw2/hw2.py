import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as fuzzy_ctrl
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def fun(x, y):
    simulation.input["temp"] = y
    simulation.input["soil"] = x
    simulation.compute()
    z = simulation.output["time"]
    return z


temp_MF = [[10, 10, 25, 35], [25, 35, 45], [35, 45, 55], [45, 55, 65], [55, 65, 85, 85]]
soil_MF = [[0, 0, 15, 35], [25, 35, 65, 75], [65, 85, 100, 100]]
time_MF = [[0, 0, 3, 6], [4, 6, 9, 11], [9, 12, 15, 15]]


temp_range = np.arange(10, 85, 1, np.float32)
soil_range = np.arange(0, 101, 1, np.float32)
time_range = np.arange(0, 16, 1, np.float32)
temp = fuzzy_ctrl.Antecedent(temp_range, "temp")
soil = fuzzy_ctrl.Antecedent(soil_range, "soil")
time = fuzzy_ctrl.Consequent(time_range, "time")

temp["cold"] = fuzzy.trapmf(temp_range, temp_MF[0])
temp["cool"] = fuzzy.trimf(temp_range, temp_MF[1])
temp["normal"] = fuzzy.trimf(temp_range, temp_MF[2])
temp["warm"] = fuzzy.trimf(temp_range, temp_MF[3])
temp["hot"] = fuzzy.trapmf(temp_range, temp_MF[4])

soil["dry"] = fuzzy.trapmf(soil_range, soil_MF[0])
soil["moist"] = fuzzy.trapmf(soil_range, soil_MF[1])
soil["wet"] = fuzzy.trapmf(soil_range, soil_MF[2])

time["short"] = fuzzy.trapmf(time_range, time_MF[0])
time["medium"] = fuzzy.trapmf(time_range, time_MF[1])
time["long"] = fuzzy.trapmf(time_range, time_MF[2])

rule_long = fuzzy_ctrl.Rule(
    (soil["dry"] & temp["hot"])
    | (soil["dry"] & temp["warm"])
    | (soil["dry"] & temp["normal"])
    | (soil["moist"] & temp["hot"]),
    time["long"], "long")

rule_medium = fuzzy_ctrl.Rule(
    (soil["dry"] & temp["warm"])
    | (soil["dry"] & temp["normal"])
    | (soil["dry"] & temp["cool"])
    | (soil["dry"] & temp["cold"])
    | (soil["moist"] & temp["hot"])
    | (soil["moist"] & temp["warm"])
    | (soil["moist"] & temp["normal"])
    | (soil["moist"] & temp["cool"])
    | (soil["wet"] & temp["hot"])
    | (soil["wet"] & temp["warm"]),
    time["medium"], "medium")

rule_short = fuzzy_ctrl.Rule(
    (soil["moist"] & temp["cold"])
    | (soil["wet"] & temp["normal"])
    | (soil["wet"] & temp["cool"])
    | (soil["wet"] & temp["cold"]),
    time["short"], "short")

time.defuzzify_method = "centroid"
system = fuzzy_ctrl.ControlSystem([rule_long, rule_medium, rule_short])
simulation = fuzzy_ctrl.ControlSystemSimulation(system)

# temp_input = int(input("Input the temperature(c): "))
# soil_input = int(input("Input the soil moisture(%): "))
# simulation.input["temp"] = temp_input
# simulation.input["soil"] = soil_input
# simulation.compute()
# output = simulation.output["time"]
# print(output)

fig, (temp_fig, soil_fig, time_fig) = plt.subplots(nrows=3, figsize=(6, 6))
temp_fig.plot(temp_range, fuzzy.trapmf(temp_range, temp_MF[0]), 'b', linewidth=1.5, label='cold')
temp_fig.plot(temp_range, fuzzy.trimf(temp_range, temp_MF[1]), 'g', linewidth=1.5, label='cool')
temp_fig.plot(temp_range, fuzzy.trimf(temp_range, temp_MF[2]), 'r', linewidth=1.5, label='normal')
temp_fig.plot(temp_range, fuzzy.trimf(temp_range, temp_MF[3]), 'y', linewidth=1.5, label='warm')
temp_fig.plot(temp_range, fuzzy.trapmf(temp_range, temp_MF[4]), 'k', linewidth=1.5, label='hot')
temp_fig.legend()

soil_fig.plot(soil_range, fuzzy.trapmf(soil_range, soil_MF[0]), 'b', linewidth=1.5, label='dry')
soil_fig.plot(soil_range, fuzzy.trapmf(soil_range, soil_MF[1]), 'g', linewidth=1.5, label='moist')
soil_fig.plot(soil_range, fuzzy.trapmf(soil_range, soil_MF[2]), 'r', linewidth=1.5, label='wet')
soil_fig.legend()

time_fig.plot(time_range, fuzzy.trapmf(time_range, time_MF[0]), 'b', linewidth=1.5, label='short')
time_fig.plot(time_range, fuzzy.trapmf(time_range, time_MF[1]), 'g', linewidth=1.5, label='medium')
time_fig.plot(time_range, fuzzy.trapmf(time_range, time_MF[2]), 'r', linewidth=1.5, label='long')
time_fig.legend()

for i in (temp_fig, soil_fig, time_fig):
    i.spines['top'].set_visible(False)
    i.spines['right'].set_visible(False)
    i.get_xaxis().tick_bottom()
    i.get_yaxis().tick_left()

fig_3D = plt.figure()
ax = Axes3D(fig_3D)
Y, X = np.meshgrid(temp_range, soil_range)
Z = fun(X, Y)
ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap=plt.cm.coolwarm)
ax.set_ylabel("air temperature", color='r')
ax.set_xlabel('soil moist', color='g')
ax.set_zlabel('watering time', color='b')

plt.tight_layout()
plt.show()
