# Fuzzy Control, Back Propagation Neural Network

## Problem 1
Due to the input of the controller are the humidity and temperature difference, and the temperature is lying between 5 and 40 Celsius, ones could assume the error of temperature is between -35 to 0. In other words, as the desire temperature is 40 and the actual room temperature is 5 degree now, the error has negative maximum as -35. Besides, the error could not be positive because as the actual temperature higher than desire, ac could not give any help for adjusting temperature.

### Membership function / Surface Plot
![image](./Figures/1-1.png) ![image](./Figures/1-2.png) <br>
From the surface plot, as the humidity get higher and temperature is heater than expect, the air conditioner will operate longer. In the other hand, ones the environment is dry and the temperature is cooler than expect, the expect running time become lower.

### Test Table
| error  |   humidity |  Time | 
| -------| ---------- | ------|
|  -35   | 90         |  9.066| 
|  -30   |  85        | 8.851 |
|  -28   |  80        |  8.690|
| -24    | 75         | 6.196 |
| -15    |70          | 5.166 |
| -7     |60          | 3.468 |
| 0      |0           | 0.533 | 


### Result
![image](./Figures/1-3.png) <br>
In above figures, I just give some assumption for the system and observe the situation. First, I just set the initial temperature and humidity to 40℃ and 90 %, and I hope the temperature could become 5℃. I also assume the change rates of temperature and humidity of the air conditioner is 0.5 degree per minute, both. And as the system compute, we could find out the needed running time starts to drop down. Ones the error and humidity are lower enough, the gradient of change rate gradually become gentle and converge into a little number, but not, zero, shutdown.

---
## Problem 2
