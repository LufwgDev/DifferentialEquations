#enable long paths in Windows

#Method 1: Using Group Policy Editor
#Press Win + R on your keyboard, type gpedit.msc, and press Enter to open the Local Group Policy Editor.
#Navigate to Computer Configuration > Administrative Templates > System > Filesystem.
#Double-click on Enable Win32 long paths.
#Select Enabled, click Apply, and then click OK.
#Restart your computer to apply the changes. 

#pip install vpython
import vpython
from vpython import *
import numpy as np

# Escena
scene.title = "Tanque de mezclas: concentración y nivel"
scene.width = 900
scene.height = 600
scene.background = color.gray(0.2)
scene.center = vector(0, 2, 0)

# Parámetros físicos
tank_height = 4.0      # m
tank_radius = 1.5      # m
A = np.pi * tank_radius**2  # área transversal (m²)
V = A * tank_height     # volumen total del tanque (m³)

# Condiciones iniciales y caudales
Qin = 0.025    # m³/s (entrada)
Qout = 0.015   # m³/s (salida)
Cin = 8.0      # g/L (alta concentración de entrada)
C0 = 0.0       # g/L (inicialmente pura)
water_height0 = 0.5  # m
dt = 0.1
t = 0

running = False  # Control de ejecución

# Crear tanque
tank = cylinder(pos=vector(0, 0, 0), axis=vector(0, tank_height, 0),
                radius=tank_radius, opacity=0.15, color=color.white)

# Crear líquido
water = cylinder(pos=vector(0, 0, 0), axis=vector(0, water_height0, 0),
                 radius=tank_radius*0.99, color=color.cyan, opacity=0.8)

# Entradas y salidas
inlet = cylinder(pos=vector(-2, tank_height*0.9, 0),
                 axis=vector(0.6, 0, 0), radius=0.05, color=color.blue)
outlet = cylinder(pos=vector(1.5, 0, 0),
                  axis=vector(0.6, 0, 0), radius=0.05, color=color.red)

# Crear gota animada
drop = sphere(pos=inlet.pos + vector(0.6, 0, 0),
              radius=0.06, color=color.blue, make_trail=True, retain=10)

# Texto informativo
info = label(pos=vector(0, tank_height + 0.7, 0),
             text="", height=16, box=False, color=color.white)

# Conversión de concentración a color
def concentration_to_color(C, Cmax=10):
    """Color entre azul (0 g/L) y rojo (Cmax g/L)"""
    ratio = min(max(C / Cmax, 0), 1)
    return vector(ratio, 0.4 + 0.4*(1 - ratio), 1 - ratio)

# Funciones de control
def start_sim():
    global running
    running = True

def pause_sim():
    global running
    running = False

def reset_sim():
    global C, water_height, t, running
    running = False
    C = C0
    water_height = water_height0
    t = 0
    water.axis = vector(0, water_height, 0)
    water.color = concentration_to_color(C)
    info.text = f"Reiniciado.\nC={C:.2f} g/L\nNivel={water_height:.2f} m"

# Actualización de parámetros desde la interfaz
def update_parameters():
    global Qin, Qout, Cin, C0, water_height0, dt
    global tank_height, tank_radius, A, V, running

    if running:
        return  # No permitir edición en ejecución

    Qin = float(qin_input.text)
    Qout = float(qout_input.text)
    Cin = float(cin_input.text)
    C0 = float(c0_input.text)
    water_height0 = float(h0_input.text)
    dt = float(dt_input.text)
    tank_height = float(height_input.text)
    tank_radius = float(radius_input.text)
    
    # Recalcular área y volumen
    A = np.pi * tank_radius**2
    V = A * tank_height

    # Actualizar geometría del tanque
    tank.axis = vector(0, tank_height, 0)
    tank.radius = tank_radius
    water.radius = tank_radius * 0.99

    reset_sim()

# Interfaz gráfica dentro de VPython
wtext(text="\n--- Parámetros del tanque ---\n")

qin_input = winput(text=str(Qin), bind=lambda _: update_parameters())
wtext(text="  Qin (m³/s)\n")

qout_input = winput(text=str(Qout), bind=lambda _: update_parameters())
wtext(text="  Qout (m³/s)\n")

cin_input = winput(text=str(Cin), bind=lambda _: update_parameters())
wtext(text="  Cin (g/L)\n")

c0_input = winput(text=str(C0), bind=lambda _: update_parameters())
wtext(text="  C inicial (g/L)\n")

h0_input = winput(text=str(water_height0), bind=lambda _: update_parameters())
wtext(text="  Nivel inicial (m)\n")

dt_input = winput(text=str(dt), bind=lambda _: update_parameters())
wtext(text="  dt (s)\n")

height_input = winput(text=str(tank_height), bind=lambda _: update_parameters())
wtext(text="  Altura del tanque (m)\n")

radius_input = winput(text=str(tank_radius), bind=lambda _: update_parameters())
wtext(text="  Radio del tanque (m)\n")

button(text="Start", bind=lambda _: start_sim())
button(text="Pause", bind=lambda _: pause_sim())
button(text="Reset", bind=lambda _: reset_sim())

# Variables internas de la simulación
C = C0
water_height = water_height0
t = 0

# Simulación principal
while True:
    rate(60)

    if running:

        # EDO de concentración
        dCdt = (Qin*Cin - Qout*C) / V
        C += dCdt * dt

        # EDO de nivel (balance de volumen)
        dHdt = (Qin - Qout) / A
        water_height += dHdt * dt
        t += dt

        # Condiciones de parada
        if water_height <= 0:
            water_height = 0
            running = False

        if water_height >= tank_height:
            water_height = tank_height
            running = False

        # Actualiza color del líquido según concentración
        water.color = concentration_to_color(C)

        # Actualiza nivel del agua
        water.axis = vector(0, water_height, 0)

        # Movimiento de la gota
        drop.pos.x += 0.08
        if drop.pos.x > inlet.pos.x + 0.6:
            drop.pos = inlet.pos + vector(0, 0, 0)
            drop.clear_trail()

        # Texto informativo
        info.text = (f"t = {t:.1f} s\n"
                    f"Nivel: {water_height:.2f} m\n"
                    f"C(t): {C:.2f} g/L")
