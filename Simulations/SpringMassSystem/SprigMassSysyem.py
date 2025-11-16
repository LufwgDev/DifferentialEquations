from vpython import *
import numpy as np

# ============================
# PARAMETERS (editable)
# ============================
m = 1.0       # mass
k = 4.0       # spring constant
b = 0.3       # damping coefficient (0 = no damping)
x0 = 1.0      # initial position
v0 = 0.0      # initial velocity

# External force F(t)
def F(t):
    # Example forcing term
    A = 1.0
    w = 1.5
    return A * np.cos(w * t)
    # return 0   # <- use this for no external force


# ============================
# SCENE SETUP
# ============================
scene = canvas(title="Sistema Masa-Resorte 3D",
               width=800, height=400,
               background=color.white)

# Fixed wall
wall = box(pos=vector(-2, 0, 0), size=vector(0.2, 1, 1), color=color.gray(0.5))

# Mass
mass = box(pos=vector(x0, 0, 0), size=vector(0.3, 0.3, 0.3), color=color.red)

# Spring (initial)
spring = helix(pos=wall.pos + vector(0.1,0,0),
               axis=mass.pos - (wall.pos + vector(0.1,0,0)),
               radius=0.15, coils=12, thickness=0.03,
               color=color.blue)

# Equilibrium marker
eq_marker = cylinder(pos=vector(0, -0.4, 0), axis=vector(0, 0.8, 0),
                     radius=0.02, color=color.green)


# ============================
# TIME + INITIAL CONDITIONS
# ============================
t = 0
dt = 0.001
x = x0
v = v0


# ============================
# SIMULATION LOOP
# ============================
while True:
    rate(1000)  # control animation speed

    # ODE: m x'' + b x' + k x = F(t)
    a = (F(t) - b*v - k*x) / m

    # Update velocity & position
    v += a * dt
    x += v * dt

    # Update mass position
    mass.pos = vector(x, 0, 0)

    # Update spring axis
    spring.axis = mass.pos - spring.pos

    t += dt
