# Stage 3B: Euler vs RK4 with drag

## Inputs
- launch speed v0 = 50, meters per second
- angle of launch θ = 45, degrees
- acceleration due to gravity g = 9.81, meters per second squared
- starting height = 0 m
- assume the ball lands on level ground at 0 m
- air density rho = 1.225, kilograms per meter cubed
- drag coefficient Cd = 0.47 for the football (dimensionless). This is the only change from stage 3A, where Cd = 0
- frontal area A = 0.038, meters squared
- mass m = 0.43, kilograms
- list of step sizes dt, seconds: 0.1, 0.03, 0.01, 0.003, 0.001
- the two methods, one per run: Euler and RK4
- reference run: RK4 at dt = 0.00001 s, run once, with the same launch values, drag values and landing rule. It is not in the dt list. It is 100 times finer than the finest step being tested, so every run in the table has a real error. A run used as its own reference would have an error of zero, which a log axis cannot draw
- both methods get the same launch values, the same drag values and the same landing rule, so any difference in range comes from the method alone

## Outputs
- the reference range R_ref, meters. It is used only to measure error and never inside the stepping
- horizontal distance travelled before landing, R, meters, for each method at each dt
- error of each run, meters: error = abs(R - R_ref)
- table: one row per dt, columns: dt (s), Euler range (m), Euler error (m), RK4 range (m), RK4 error (m). R_ref is printed once above the table
- plot: x-axis is dt in seconds, y-axis is error in meters, both axes on a log-log scale
- two lines on the plot, one for each method. The reference run is not plotted, because its error against itself is zero
- R is found the same way as stage 3A: step until y is below 0, then apply the quadratic landing rule from the last point above the ground. With drag the acceleration is not exactly constant over that last sliver, so this rule is no longer exact

## Steps
1. Start with v0, θ, g, rho, Cd = 0.47, A, m, the five dt values and the reference step 0.00001.
2. Convert θ from degrees to radians once, before any loop. Compute k = 0.5 * rho * Cd * A once.
3. Run the reference: one complete RK4 flight at dt = 0.00001 and store its range as R_ref.
4. Create an empty results store, one slot per (dt, method) pair, ten in total.
5. Loop over each dt in the list.
6. Inside that, loop over each method: Euler, then RK4.
7. For that dt and method, run one complete flight from launch to landing, with dt fixed throughout. This is the same stepping and landing code as stage 3A. Drag is now on, so the acceleration depends on the speed at every step.
8. Store R, labelled by its dt and method.
9. When both loops finish, compute error = abs(R - R_ref) for all ten ranges.
10. Print R_ref, then the table.
11. Fit a straight line to log(error) against log(dt) for each method and print both slopes.
12. Plot error against dt for both methods as two lines, log-log, and save the plot.

## Test case
- Stepping check: run Euler at dt = 0.01 with the old straight-line landing rule from stage 2. It must give 54.90 m, the R printed by stage2_drag.py. If it does, the drag and the stepping are correct. Only then switch to the quadratic landing rule.
- Reference check: RK4 at dt = 0.00002 must agree with R_ref to within about 1e-9 m. If it does, the reference can be trusted. R_ref should come out at 54.985 m.
- Expected Euler result: error falls roughly in proportion to dt, slope 1 on the log-log plot. About 0.96 m at dt = 0.1 and about 0.008 m at dt = 0.001.
- Expected RK4 result: error far below Euler's at every dt and falling much faster. About 2e-4 m at dt = 0.1 and about 5e-11 m at dt = 0.001. The fitted slope is about 3, and the points scatter, so the slope between neighbouring points ranges from about 2.5 to 4.6.
- Pass condition: Euler slope within about 0.1 of 1. RK4 slope between 2.5 and 4.5. RK4 error below Euler error at every dt.
- Limit of this test: RK4's step is fourth order, but the fitted slope comes out nearer 3. The likely cause is the landing rule, which treats the acceleration as constant over the last sliver of time. That was not tested. This test shows RK4 is far more accurate than Euler with drag. It does not separate the stepping error from the landing error.
