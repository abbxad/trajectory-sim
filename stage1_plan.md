# Stage 1: projectile without drag

## Inputs
- launch speed v0, meters per second
- angle of launch θ, degrees
- acceleration due to gravity g = 9.81, meters per second squared
- assume the ball starts at ground level, height 0 m
- no air resistance, so horizontal speed stays constant throughout motion
- the ball lands on level ground at height 0 m

## Outputs
- horizontal distance travelled before landing R, meters
- highest point above the ground H, meters
- time taken to reach the ground after launch t, seconds
- trajectory plot, x-axis: x, meters, y-axis: y, meters
- R is the x value when ball returns to y = 0
- H is the y value at the maximum turning point

## Steps
1. start with v0, θ, g
2. convert θ from degrees to radians
3. split v0 into horizontal component `vx = v0 * cos(θ)`, vertical component `vy = v0 * sin(θ)`, both in meters per second
4. time to the top t_top, seconds is determined using v = u + a*t with `u = vy`, `v = 0`, `a = -g`, so `t_top = vy / g`
5. total time t, seconds the fall takes as long as the rise so `t = 2*vy / g`
6. maximum height H, meters is determined by `s = u*t + 0.5*a*t^2` with `s = H`, `u = vy`, `t = t_top`, `a = -g` so `H = vy*t_top + 0.5*(-g)*t_top^2`
7. range R, meters is determined by v = s / t with `v = vx`, `s = R`, `t = t` so `R = vx*t`
8. times: 10000 equally spaced values from 0 to t, including both ends. For each time T: `x = vx * T`, `y = vy*T + 0.5*(-g)*T^2`
9. print H, R both in meters, t in seconds, plot of the whole flight, height against distance

## Test case
- v0 = 30 m/s, θ = 60°, g = 9.81 m/s²
- vx = 15 m/s, vy = 25.98 m/s
- t_top = 2.65 s, t = 5.30 s
- H = 34.40 m, R = 79.45 m
- plot: starts at (0.00,0.00), peaks at (39.73, 34.40), ends at (79.45, 0.00)
