# Fuzzy Control of Watering System
Define your own membership functions and rules and design the program of gardener watering. Observe its performance surface and make appropriate adjustments on membership functions and rules.
1. Outputs make sense
2. Rules identify desired behavior 
3. Labels have correct shape and overlap by exhaustively various input combinations : 
   * At extreme ends of universe of discourse
   * At extreme ends of the individual M.F.’ domain
   * Corresponding to the overlap of M.F.
   * With some degree of truth in as many antecedents as possible

---

### Membership function / Surface Plot
![image](./Figures/v3-1.png)![image](./Figures/v3-2.png)
![image](./Figures/Final-1.png)![image](./Figures/Final-2.png)

### Rule Table
|        |   cold |  cool | normal |  warm  |   hot  |
| -------| ------ | ------|------- | -------|--------|
|  Dry   | meduim | meduim|  long  |  long  |  long  |
|  Moist |  short | meduim| meduim | medium |  long  |
|  Wet   |  short | short | short  | meduim | meduim |

In the final version, I just re-modifying the membership function and rule. First, I increasing the overlapping to that the output has more balancing values, and make they in balancing and a little be symmetry that could make the hierarchy clearly. In the rule, I re-constrain the boundary condition, just make it more complex and restrict, so that few differences could lead a huge impact around it.

### Test Table
|  Time  |   2.33 |  2.54 |   7.5  |  2.33  |   7.65 | 9.94 | 7.5 | 9.95 | 12.6 |
| -------| ------ | ------|------- | -------|--------|------|-----|------|------|
|  Temp  |   100  | 50    |  0     |  100   |  50    | 0    | 100 | 50   | 0    |
|  Moist |  10    | 10    | 10     | 45     |  45    |  45  | 80  | 80   | 80   |

The moisture is between 0 and 100 in %, and temperature is between 10 and 80 Celsius, watering time then between 0 and 15 minutes. And the above table gives some various values for testing the simulation system.
