import numpy as np
import matplotlib.pyplot as plt

# step 1
v0 = 30  # m/s
theta_deg = 60  # degrees
g = 9.81  # m/s^2

# step 2
theta_rad = np.deg2rad(theta_deg)

# step 3
vx = v0*np.cos(theta_rad)
vy = v0*np.sin(theta_rad)

# step 4
t_top = vy/g

# step 5
t = 2*t_top

# step 6
H = vy*t_top + 0.5*(-g)*t_top**2

# step 7
R = vx*t

# step 8
times = np.linspace(0, t, 10000)
x = vx*times
y = vy*times + 0.5*(-g)*times**2

# step 9
print(f"R = {R:.2f} m")
print(f"H = {H:.2f} m")
print(f"t = {t:.2f} s")
print(y[0])
print(y[-1])
plt.plot(x, y)
plt.xlabel("Distance x (m)")
plt.ylabel("Height y (m)")
plt.savefig("stage1_trajectory.png")
plt.show()
