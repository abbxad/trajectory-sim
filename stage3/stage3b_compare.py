import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# step 1
v0 = 50  # m/s
theta_deg = 45  # degrees
g = 9.81  # m/s^2
rho = 1.225  # kg/m^3
Cd = 0.47  # dimensionless, the football, drag on
A = 0.038  # m^2
m = 0.43  # kg
dt_list = [0.1, 0.03, 0.01, 0.003, 0.001]  # s
method_list = ["Euler", "RK4"]
dt_ref = 0.00001  # s, reference run
landing_rule = "quadratic"  # "linear" is the stage 2 rule, used only for the stepping check

# step 2
theta_rad = np.deg2rad(theta_deg)  # rad
k = 0.5 * rho * Cd * A  # kg/m


def accel(vx, vy):
    # acceleration from gravity and drag, used by both methods
    v = np.sqrt(vx**2 + vy**2)  # m/s
    ax = -(k/m) * v * vx  # m/s^2
    ay = -g - (k/m) * v * vy  # m/s^2
    return ax, ay


def flight(dt, method):
    # one complete flight from launch to landing, returns the range R in m
    x = 0  # m
    y = 0  # m
    vx = v0*np.cos(theta_rad)  # m/s
    vy = v0*np.sin(theta_rad)  # m/s

    while True:
        ax, ay = accel(vx, vy)  # m/s^2

        if method == "Euler":
            x_new = x + vx*dt
            y_new = y + vy*dt
            vx_new = vx + ax*dt
            vy_new = vy + ay*dt
        else:
            # four slopes, each measured from the same starting state
            k1x, k1y = vx, vy
            k1vx, k1vy = ax, ay

            k2x, k2y = vx + k1vx*dt/2, vy + k1vy*dt/2
            k2vx, k2vy = accel(k2x, k2y)

            k3x, k3y = vx + k2vx*dt/2, vy + k2vy*dt/2
            k3vx, k3vy = accel(k3x, k3y)

            k4x, k4y = vx + k3vx*dt, vy + k3vy*dt
            k4vx, k4vy = accel(k4x, k4y)

            x_new = x + dt*(k1x + 2*k2x + 2*k3x + k4x)/6
            y_new = y + dt*(k1y + 2*k2y + 2*k3y + k4y)/6
            vx_new = vx + dt*(k1vx + 2*k2vx + 2*k3vx + k4vx)/6
            vy_new = vy + dt*(k1vy + 2*k2vy + 2*k3vy + k4vy)/6

        # stop when the step goes below the ground
        if y_new < 0:
            break

        x = x_new
        y = y_new
        vx = vx_new
        vy = vy_new

    # landing
    # x, y, vx, vy are now the last point above the ground
    if landing_rule == "quadratic":
        # constant acceleration over the remaining sliver of time tau
        a_q = 0.5 * ay  # m/s^2
        b_q = vy  # m/s
        c_q = y  # m
        disc = b_q**2 - 4*a_q*c_q  # m^2/s^2
        tau_1 = (-b_q + np.sqrt(disc)) / (2*a_q)  # s
        tau_2 = (-b_q - np.sqrt(disc)) / (2*a_q)  # s
        tau = min(t for t in (tau_1, tau_2) if t >= 0)  # s
        R = x + vx*tau + 0.5*ax*tau**2  # m
    else:
        f = y / (y - y_new)  # fraction of the last step before the ground
        R = x + f*(x_new - x)  # m
    return R


# step 3
R_ref = flight(dt_ref, "RK4")  # m

# step 4
R_euler = []  # m
R_rk4 = []  # m

# step 5
for dt in dt_list:
    # step 6
    for method in method_list:
        # step 7
        R = flight(dt, method)  # m

        # step 8
        if method == "Euler":
            R_euler.append(R)
        else:
            R_rk4.append(R)

# step 9
error_euler = [abs(R - R_ref) for R in R_euler]  # m
error_rk4 = [abs(R - R_ref) for R in R_rk4]  # m

# check
R_check = flight(2*dt_ref, "RK4")  # m, a second reference at twice the step
print(f"R_ref = {R_ref:.3f} m")
print(f"reference check, dt = {2*dt_ref}: difference = {abs(R_check - R_ref):.1e} m")

# step 10
print("dt (s) | Euler R (m) | Euler error (m) | RK4 R (m) | RK4 error (m)")
for i in range(len(dt_list)):
    print(f"{dt_list[i]} | {R_euler[i]:.3f} | {error_euler[i]:.3e} | {R_rk4[i]:.3f} | {error_rk4[i]:.3e}")

# step 11
slope_euler = np.polyfit(np.log(dt_list), np.log(error_euler), 1)[0]
slope_rk4 = np.polyfit(np.log(dt_list), np.log(error_rk4), 1)[0]
print(f"Euler slope = {slope_euler:.2f}")
print(f"RK4 slope = {slope_rk4:.2f}")

# step 12
plt.loglog(dt_list, error_euler, "o-", label="Euler")
plt.loglog(dt_list, error_rk4, "s-", label="RK4")
plt.xlabel("Step size dt (s)")
plt.ylabel("Range error (m)")
plt.title("Euler vs RK4, 50 m/s at 45 degrees, with drag")
plt.legend()
plt.savefig(Path(__file__).parent / "stage3b_error.png")
plt.show()
