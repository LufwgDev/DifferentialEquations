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
scene.title = "Tanque de mezcla: concentración y nivel"
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
C = 0.0        # g/L (inicialmente pura)
water_height = 0.5  # m
dt = 0.1
t = 0

# Crear tanque
tank = cylinder(pos=vector(0, 0, 0), axis=vector(0, tank_height, 0),
                radius=tank_radius, opacity=0.15, color=color.white)

# Crear líquido
water = cylinder(pos=vector(0, 0, 0), axis=vector(0, water_height, 0),
                 radius=tank_radius*0.99, color=color.cyan, opacity=0.8)

# Entradas y salidas
inlet = cylinder(pos=vector(-2, tank_height*0.9, 0),
                 axis=vector(0.6, 0, 0), radius=0.05, color=color.blue)
outlet = cylinder(pos=vector(1.5, 0, 0),
                  axis=vector(0.6, 0, 0), radius=0.05, color=color.red)

drop = sphere(pos=inlet.pos + vector(0.6, 0, 0),
              radius=0.06, color=color.blue, make_trail=True, retain=10)

# Texto informativo
info = label(pos=vector(0, tank_height + 0.7, 0),
             text="", height=16, box=False, color=color.white)

# Conversión de concentración a color
def concentration_to_color(C, Cmax=10):
    """Color entre azul (0 g/L) y rojo (Cmax g/L)."""
    ratio = min(max(C / Cmax, 0), 1)
    return vector(ratio, 0.4 + 0.4*(1 - ratio), 1 - ratio)

# Simulación
while True:
    rate(60)

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
        info.text = f"Tanque vacío. Simulación detenida.\nTiempo: {t:.1f}s"
        break
    if water_height >= tank_height:
        water_height = tank_height
        info.text = f"Tanque lleno. Simulación detenida.\nTiempo: {t:.1f}s"
        break

    # Actualiza color del líquido
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


