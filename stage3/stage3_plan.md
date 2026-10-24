# Stage 3: Euler vs RK4

## Inputs
- launch speed v0 = 50, meters per second
- angle of launch θ = 45, degrees
- acceleration due to gravity g = 9.81, meters per second squared
- starting height = 0 m
- assume the ball lands on level ground at 0 m
- air density rho = 1.225, kilograms per meter cubed
- drag coefficient Cd = 0 for the test case (dimensionless), which makes k = 0 so an exact answer exists. Cd = 0.47 for the football in stage 2
- frontal area A = 0.038, meters squared
- mass m = 0.43, kilograms
- list of step sizes dt, seconds: 0.1, 0.03, 0.01, 0.003, 0.001
- the two methods, one per run: Euler and RK4
- both methods get the same launch values, the same drag values and the same landing rule, so any difference in range comes from the method alone

## Outputs
- horizontal distance travelled before landing, R, meters, for each method at each dt
- exact range with no drag, R_exact = v0^2 * sin(2θ) / g, meters. It is used only to measure error and never inside the stepping
- error of each run, meters: error = abs(R - R_exact) where R_exact = 254.842 m
- table: one row per dt, columns: dt (s), Euler range (m), Euler error (m), RK4 range (m), RK4 error (m)
- plot: x-axis is dt in seconds, y-axis is error in meters, both axes on a log-log scale
- two lines on the plot, one for each method
- R is found by stepping until y is below 0 after a step. Take the last point above the ground, with position (x0, y0), velocity (vx0, vy0) and acceleration (ax0, ay0), all from the method's own state at that point. Over the remaining sliver of time tau, assume constant acceleration: `y0 + vy0*tau + 0.5*ay0*tau^2 = 0`. Solve for tau with the quadratic formula (`a = 0.5*ay0`, `b = vy0`, `c = y0`) and keep the smallest positive root. Then `R = x0 + vx0*tau + 0.5*ax0*tau^2`. Both methods use this same landing rule.

## Steps
1. Start with v0, θ, g, rho, Cd, A, m and the list of five dt values: 0.1, 0.03, 0.01, 0.003, 0.001.
2. Convert θ from degrees to radians once, before any loop.
3. Compute R_exact = v0^2 * sin(2θ) / g once, before any loop.
4. Create an empty results store, with one slot per (dt, method) pair, ten in total.
5. Loop over each dt in the list.
6. Inside that, loop over each method: Euler, then RK4.
7. For that dt and method, run one complete flight from launch to landing. dt stays fixed the whole way through:
   - Set the starting state [x, y, vx, vy] from v0 and θ.
   - Step forward until y goes below 0. Euler uses one slope per step. RK4 uses four slopes k1 to k4, each measured from the same starting state of that step, then steps with the weighted average (k1 + 2*k2 + 2*k3 + k4) / 6.
   - When y goes below 0, apply the quadratic landing rule from the last point above the ground to get R.
8. Store R in the results, labelled by its dt and method.
9. When both loops finish, compute error = abs(R - R_exact) for all ten stored ranges.
10. Print the table, one row per dt, with the five columns defined in Outputs.
11. Plot error against dt for both methods as two lines, with both axes on a log-log scale.

## Test case
- R_exact = 254.842 m, v0 = 50 m/s, 0 = 45 °, g = 9.81, Cd = 0
- Stepping check: run Euler with the old straight-line landing rule from stage 2. It must give 258.374 m at dt = 0.1, 255.195 m at dt = 0.01 and 254.877 m at dt = 0.001. If it does, the stepping loop is correct. Only then switch to the quadratic landing rule.
- Expected Euler result: error falls roughly in proportion to dt (slope 1 on the log-log plot). Each 10 times smaller dt gives about 10 times smaller error. At dt = 0.1 the error is about 3.5 m, and at dt = 0.001 about 0.035 m.
- Expected RK4 result: with Cd = 0 the true path is a parabola, which RK4 integrates exactly. The quadratic landing rule is also exact here. RK4's error should be at rounding level (about 1e-12 m or smaller) at every dt, with no meaningful slope.
- Pass condition: Euler slope within about 0.1 of 1, and RK4 error below 1e-9 m at all five dt values. If RK4 error is larger, the bug is in the RK4 step or the landing rule.
- Limit of this test: it proves both methods and the landing rule are coded correctly, but it cannot show RK4's fourth-order convergence. That comparison needs drag, where the path is curved, and is done in stage 3B against an RK4 reference at dt = 1e-5.