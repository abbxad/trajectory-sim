# Projectile trajectory simulation

## Problem

This project simulates a ball launched at a given speed and angle. It finds how far the ball travels, how high it gets and how long it stays in the air.

Stage 1 ignores air resistance and uses exact formulas. Stage 2 adds air resistance. That has no simple formula, so the program moves the ball forward in small time steps (Euler's method) and checks the result against the exact answer from stage 1.

## Stage 1: no air resistance

### Problem

This program simulates a ball launched at a given speed and angle. It finds how far the ball travels, how high it gets and how long it stays in the air. It assumes no air resistance and flat ground, so the ball lands at the height it started from.

The test case is a launch at 30 m/s at 60 degrees, with g = 9.81 m/s².

### Method

**Inputs and outputs.** The program takes a launch speed `v0`, a launch angle `theta` and gravity `g`. It outputs the range R (total horizontal distance), the maximum height H and the time of flight `t`. It also plots the path of the ball.

**Time of flight.** The program finds the time to reach the top, `t_top`, from the vertical speed and gravity. The flat-ground assumption makes the path symmetrical, so the time rising equals the time falling. The total flight time is `t = 2 * t_top`.

**Drawing the curve.** `np.linspace(0, t, 10000)` makes 10000 equally spaced times from launch to landing. For each time, the code calculates how far across the ball is (`x = vx * time`) and how high it is (`y = vy * time + 0.5 * (-g) * time**2`). Plotting each `y` against its `x` joins the 10000 positions into the curve.

**Check.** The ball starts and lands at ground level. `y[0]` is the height at launch and `y[-1]` is the height at time `t`. Both printing 0.0 confirms the flight time is correct.

### Result

For the test case:

| Quantity | Program | Exact |
|---|---|---|
| Range R | 79.45 m | 79.45 m |
| Maximum height H | 34.40 m | 34.40 m |
| Time of flight t | 5.30 s | 5.30 s |

### Plot

![Trajectory of the ball, 30 m/s at 60 degrees](stage1/stage1_trajectory.png)

## Stage 2: with air resistance

### Problem

The program now includes air resistance. The test object is a football with air density rho = 1.225 kg/m³, drag coefficient Cd = 0.47, frontal area A = 0.038 m² and mass m = 0.43 kg. The launch is 50 m/s at 45 degrees with g = 9.81 m/s², and the time step is dt = 0.01 s.

### Method

**Inputs and outputs.** The inputs are the launch speed `v0`, the angle `theta`, gravity `g`, the drag values `rho`, `Cd`, `A` and `m`, and the step size `dt`. The outputs are the range R, the maximum height H, the time of flight `t` and a plot of the path.

**Drag.** Air pushes against the motion, and harder the faster the ball moves. The drag force is `k * v^2`, where `k = 0.5 * rho * Cd * A` and `v` is the speed. Split into horizontal and vertical parts and divided by the mass, this gives `ax = -(k/m) * v * vx` and `ay = -g - (k/m) * v * vy`. The speed changes every instant, so the drag changes every instant, and no single formula gives the path.

**Stepping forward.** The program tracks four numbers: `x`, `y`, `vx` and `vy`. At each step it works out `ax` and `ay` from the current values. Each value then becomes its old value plus `dt` times its rate of change, for example `x_new = x + vx*dt` and `vx_new = vx + ax*dt`. All four new values are worked out from the same old values before any are replaced. Each point is stored in a list, and the loop repeats until `y` is below 0.

**Landing.** The loop stops just after the ball passes through the ground, so the last point is below `y = 0`. The program draws a straight line between the last two points and finds where it crosses the ground. The fraction of the way along is `f = y_a / (y_a - y_b)`, where a is the last point above the ground and b is the first point below it. Then `R = x_a + f * (x_b - x_a)` and `t = t_a + f * dt`. H is the largest `y` in the list.

### Result

**Check with drag switched off.** With `Cd = 0` and the 50 m/s, 45 degree launch, the exact range is 254.842 m. Euler's method gets closer as the step size shrinks.

| dt (s) | Euler range (m) | Error (m) |
|---|---|---|
| 0.1 | 258.374 | 3.532 |
| 0.01 | 255.195 | 0.353 |
| 0.001 | 254.877 | 0.035 |

Each tenfold drop in `dt` cuts the error about tenfold. Euler's method is first order. It overshoots because it uses the vertical speed at the start of each step for the whole step, while the ball is slowing down during it.

**With drag switched on.** For the football:

| Quantity | No drag (exact) | With drag |
|---|---|---|
| Range R | 254.84 m | 54.90 m |
| Maximum height H | 63.71 m | 22.69 m |
| Time of flight t | 7.21 s | 4.23 s |

Drag shortens the range to about a fifth. The path is no longer symmetrical. The ball rises gently and falls steeply, and the peak is past the halfway point of the flight.

### Plot

![Trajectory of a football, 50 m/s at 45 degrees, with air resistance](stage2/stage2_trajectory.png)

## Stage 3: Euler against RK4

### Problem

Stage 2 used Euler's method. This stage compares it with a more accurate method, RK4 (fourth-order Runge-Kutta). The launch is 50 m/s at 45 degrees with g = 9.81 m/s². Both methods run at five time steps, dt = 0.1, 0.03, 0.01, 0.003 and 0.001 s, and each range is compared with a trusted answer. Stage 3A has no air resistance. Stage 3B uses the football from stage 2 (rho = 1.225 kg/m³, Cd = 0.47, A = 0.038 m², m = 0.43 kg).

### Method

**Euler.** Each step uses one reading of the speed and acceleration, taken at the start of the step, and assumes they stay the same for the whole step.

**RK4.** Each step takes four readings: at the start, twice in the middle and at the end. Each reading uses the one before it to decide where to look. The step then uses an average of the four, where the two middle readings count double.

**Landing.** The loop stops at the first step below the ground. From the last point above the ground, the program assumes constant acceleration over the remaining sliver of time and solves a quadratic for it. Both methods use the same rule.

**Error.** Error is `abs(R - answer)`. In 3A the answer is the exact range, 254.842 m. With drag there is no formula, so in 3B the answer is an RK4 run at dt = 0.00001 s, which gives R = 54.985 m. A second run at dt = 0.00002 s differs from it by 3e-12 m. The reference is 100 times finer than the smallest step tested, so no run is marked against itself.

### Result

**3A, no air resistance.** The exact range is 254.842 m.

| dt (s) | Euler error (m) | RK4 error (m) |
|---|---|---|
| 0.1 | 3.532 | about 2e-13 |
| 0.01 | 0.353 | about 2e-12 |
| 0.001 | 0.035 | about 5e-11 |

Euler's error falls in proportion to dt (slope 1.00). With no drag the path is a parabola, which RK4 follows exactly, so its error is only the computer's rounding. It rises slightly as dt shrinks because smaller steps mean more steps.

**3B, with air resistance.** The reference range is 54.985 m.

| dt (s) | Euler error (m) | RK4 error (m) |
|---|---|---|
| 0.1 | 0.957 | 1.6e-4 |
| 0.03 | 0.262 | 1.0e-6 |
| 0.01 | 0.085 | 1.6e-8 |
| 0.003 | 0.025 | 4.1e-9 |
| 0.001 | 0.008 | 4.6e-11 |

The fitted slope is 1.03 for Euler and 3.09 for RK4. RK4 is about 6,000 times more accurate than Euler at dt = 0.1 and gains about a thousand times in accuracy for each tenfold drop in dt. RK4's step is fourth order, but the fitted slope is nearer 3. The likely cause is the landing rule, which treats the acceleration as constant over the last sliver of time. That has not been tested.

### Plots

Stage 3A, no air resistance:

![Euler vs RK4 error, no drag](stage3/stage3_error.png)

Stage 3B, with air resistance:

![Euler vs RK4 error, with drag](stage3/stage3b_error.png)
