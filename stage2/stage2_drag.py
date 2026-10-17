import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# step 1
v0 = 50  # m/s
theta_deg = 45  # degrees
g = 9.81  # m/s^2
rho = 1.225  # kg/m^3
Cd = 0.47  # dimensionless
A = 0.038  # m^2
m = 0.43  # kg
dt = 0.01  # s

# step 2
theta_rad = np.deg2rad(theta_deg)  #rad

# step 3
x = 0  # m
y = 0  # m, starting height
t = 0  # s
vx = v0*np.cos(theta_rad)  # m/s
vy = v0*np.sin(theta_rad)  # m/s

# step 4
k = 0.5 * rho * Cd * A  # kg/m

# step 5
t_list = [0]  # s
x_list = [x]  # m
y_list = [y]  # m

# check
print(vx, vy, k)

# step 6
while y >= 0:
    # step 7
    v = np.sqrt(vx**2 + vy**2)  # m/s
    ax = -(k/m) * v * vx  # m/s^2
    ay = -g - (k/m) * v * vy  # m/s^2

    # step 8
    x_new = x + vx*dt
    y_new = y + vy*dt
    vx_new = vx + ax*dt
    vy_new = vy + ay*dt
    t_new = t + dt

    x = x_new
    y = y_new
    vx = vx_new
    vy = vy_new
    t = t_new

    # step 9
    x_list.append(x)
    y_list.append(y)
    t_list.append(t)

# step 10
x_a = x_list[-2]  # m
y_a = y_list[-2]  # m
t_a = t_list[-2]  # s
x_b = x_list[-1]  # m
y_b = y_list[-1]  # m

f = y_a / (y_a - y_b)  # fraction of the last step before the ground
R = x_a + f*(x_b - x_a)  # m
t_land = t_a + f*dt  # s
H = max(y_list)  # m

print(f"R = {R:.2f} m")
print(f"H = {H:.2f} m")
print(f"t = {t_land:.2f} s")

# step 11
plt.plot(x_list, y_list)
plt.xlabel("Distance x (m)")
plt.ylabel("Height y (m)")
plt.title("Football, 50 m/s at 45 degrees, with drag")
plt.savefig(Path(__file__).parent / "stage2_trajectory.png")
plt.show()
