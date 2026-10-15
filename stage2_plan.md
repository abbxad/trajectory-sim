# Stage 2: projectile with drag

## Inputs
- launch speed v0, meters per second
- angle of launch θ, degrees
- acceleration due to gravity g = 9.81, meters per second squared
- the object is a football
- air density rho = 1.225, kilograms per meter cubed
- drag coefficient Cd = 0.47, dimensionless (smooth sphere)
- frontal area A = 0.038, meters squared (radius 0.11m)
- mass m = 0.43, kilograms
- step size dt, seconds
- starting height = 0 m
- assume the ball lands on level ground at 0 m
- air resistance acts against the motion, so vx changes during the flight

## Outputs
- horizontal distance travelled before landing R, meters
- highest point above the ground H, meters
- time taken to reach the ground after launch t, seconds
- trajectory plot, x-axis: x, meters, y-axis: y, meters
- R is the x at the landing moment, found by estimating between the last point above the ground and the first point below it
- H is the largest y in the stored list
- t is the time at that same landing moment, found the same way

## Steps
1. start with v0, θ, g, rho, Cd, A, m and dt
2. convert θ from degrees to radians
3. set the starting state: x = 0 m, y = 0 m (the starting height), horizontal speed `vx = v0 * cos(θ)`, vertical speed `vy = v0 * sin(θ)`, both in meters per second
4. combine the drag inputs into one number, `k = 0.5 * rho * Cd * A`, in kilograms per meter. It stays the same for the whole flight
5. make lists for time, x and y, and store the starting values (time = 0 s)
6. repeat steps 7 to 9 until y is below 0 after a step, which means the ball has gone through the ground
7. find the rates from the current state. Speed `v = sqrt(vx^2 + vy^2)` in meters per second, then `ax = -(k/m) * v * vx` and `ay = -g - (k/m) * v * vy`, both in meters per second squared
8. take one step of length dt, working every new value out from the same old state: `x_new = x + dt*vx`, `y_new = y + dt*vy`, `vx_new = vx + dt*ax`, `vy_new = vy + dt*ay`, and time goes up by dt. Then replace all four values together
9. store the new time, x and y in the lists
10. after the loop, find the landing moment between the last point above the ground (x_a, y_a, time t_a) and the first point below it (x_b, y_b). The fraction of the way down to y = 0 is `f = y_a / (y_a - y_b)`. Then `R = x_a + f*(x_b - x_a)` and `t = t_a + f*dt`. H is the largest y in the list
11. plot y against x using the lists

## Test case
- v0 = 50 m/s, angle θ = 45°, g = 9.81 m/s², dt = 0.01 s, starting height = 0 m
- turn drag off by setting Cd = 0, k = 0, ax = 0, ay = -g
- exact answer with no drag: `vx = 50 * cos(45°) = 35.355 m/s`, `vy = 50 * sin(45°) = 35.355 m/s`, `t = 2*vy / g = 7.208 s`, `H = vy^2 / (2*g) = 63.71 m`, `R = vx * t = 254.842 m`
- the simulation should give R close to 255.195 m, using Euler with dt = 0.01s
- the two do not match exactly because Euler uses vertical speed at the start of each step for the whole step, even though the ball is slowing down during it. Every step puts the ball slightly too high, so it lands slightly too far
- pass: R within 0.5 m of 254.842 m. If it is out by metres, check the angle conversion and the landing estimate first
- halving dt should roughly halve the error, since Euler is first order. For dt = 0.1, 0.01 and 0.001 the ranges should be about 258.374, 255.195 and 254.877