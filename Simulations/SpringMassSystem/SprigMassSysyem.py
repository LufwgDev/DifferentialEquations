#enable long paths in Windows

#Method 1: Using Group Policy Editor
#Press Win + R on your keyboard, type gpedit.msc, and press Enter to open the Local Group Policy Editor.
#Navigate to Computer Configuration > Administrative Templates > System > Filesystem.
#Double-click on Enable Win32 long paths.
#Select Enabled, click Apply, and then click OK.
#Restart your computer to apply the changes. 

#pip install vpython
from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Sistema Masa-Resorte-Amortiguador",
               width=1200, height=700, background=color.white)

# lista para llevar los objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del Sistema ---\n")

# Sliders con valores dinámicos
# --- Masa ---
texto_m = wtext(text="Masa (m): 1.00 kg\n")
def actualizar_m(s):
    texto_m.text = f"Masa (m): {s.value:.2f} kg\n"
slider_m = slider(min=0.1, max=5.0, value=1.0, step=0.1, bind=actualizar_m)

# --- Constante del resorte ---
texto_k = wtext(text="\nConstante del resorte (k): 4.00 N/m\n")
def actualizar_k(s):
    texto_k.text = f"\nConstante del resorte (k): {s.value:.2f} N/m\n"
slider_k = slider(min=0.5, max=20.0, value=4.0, step=0.5, bind=actualizar_k)

# --- Coeficiente de amortiguamiento ---
texto_b = wtext(text="\nCoeficiente de amortiguamiento (b): 0.30\n")
def actualizar_b(s):
    texto_b.text = f"\nCoeficiente de amortiguamiento (b): {s.value:.2f}\n"
slider_b = slider(min=0.0, max=2.0, value=0.3, step=0.05, bind=actualizar_b)

# --- Posición inicial ---
texto_x0 = wtext(text="\nPosición inicial (x₀): 1.00 m\n")
def actualizar_x0(s):
    texto_x0.text = f"\nPosición inicial (x₀): {s.value:.2f} m\n"
slider_x0 = slider(min=-2.0, max=2.0, value=1.0, step=0.1, bind=actualizar_x0)

# --- Velocidad inicial ---
texto_v0 = wtext(text="\nVelocidad inicial (v₀): 0.00 m/s\n")
def actualizar_v0(s):
    texto_v0.text = f"\nVelocidad inicial (v₀): {s.value:.2f} m/s\n"
slider_v0 = slider(min=-5.0, max=5.0, value=0.0, step=0.1, bind=actualizar_v0)

# --- Amplitud de fuerza externa ---
texto_A = wtext(text="\nAmplitud fuerza externa (A): 1.00\n")
def actualizar_A(s):
    texto_A.text = f"\nAmplitud fuerza externa (A): {s.value:.2f}\n"
slider_A = slider(min=0.0, max=3.0, value=1.0, step=0.1, bind=actualizar_A)

# --- Frecuencia de fuerza externa ---
texto_w = wtext(text="\nFrecuencia fuerza externa (ω): 1.50 rad/s\n")
def actualizar_w(s):
    texto_w.text = f"\nFrecuencia fuerza externa (ω): {s.value:.2f} rad/s\n"
slider_w = slider(min=0.0, max=5.0, value=1.5, step=0.1, bind=actualizar_w)

wtext(text="\n")

# Mostrar ecuación diferencial
ecuacion_text = wtext(text="\nEcuación: m·x'' + b·x' + k·x = A·cos(ω·t)\n")

# Salidas numéricas
salida_info = wtext(text="\nTiempo actual: 0.00 s\n")

# -------------------------------------------------
# FUNCIONES DE SIMULACIÓN
# -------------------------------------------------

# Limpiar objetos anteriores
def hide_previous_objects():
    global created_objects
    for obj in created_objects:
        try:
            obj.visible = False
        except:
            pass
    created_objects = []

# Simulación
def simular(ev):
    global created_objects

    # Leer parámetros desde sliders
    m = float(slider_m.value)
    k = float(slider_k.value)
    b = float(slider_b.value)
    x0 = float(slider_x0.value)
    v0 = float(slider_v0.value)
    A = float(slider_A.value)
    w = float(slider_w.value)

    # Ocultar objetos previos
    hide_previous_objects()

    # Función de fuerza externa
    def F(t):
        return A * np.cos(w * t)

    # ============================
    # CONFIGURACIÓN DE ESCENA
    # ============================
    
    # Fixed wall
    wall = box(pos=vector(-3, 0, 0), size=vector(0.2, 1, 1), color=color.gray(0.5))
    
    # Mass
    mass = box(pos=vector(x0, 0, 0), size=vector(0.4, 0.4, 0.4), 
               color=color.red, make_trail=True, trail_type="points", 
               trail_radius=0.02, interval=10, retain=200)
    
    # Spring (initial)
    spring = helix(pos=wall.pos + vector(0.1, 0, 0),
                   axis=mass.pos - (wall.pos + vector(0.1, 0, 0)),
                   radius=0.15, coils=12, thickness=0.03,
                   color=color.blue)
    
    # Equilibrium marker
    eq_marker = cylinder(pos=vector(0, -0.5, 0), axis=vector(0, 1.0, 0),
                         radius=0.02, color=color.green)
    
    # Labels informativos
    label_pos = label(text=f"Posición: {x0:.2f} m", pos=vector(0, 1.5, 0), 
                      box=False, height=16)
    label_vel = label(text=f"Velocidad: {v0:.2f} m/s", pos=vector(0, 1.2, 0), 
                      box=False, height=16)
    
    created_objects.extend([wall, mass, spring, eq_marker, label_pos, label_vel])

    # ============================
    # VARIABLES DE SIMULACIÓN
    # ============================
    t = 0
    dt = 0.01
    x = x0
    v = v0

    # ============================
    # BUCLE DE SIMULACIÓN
    # ============================
    running = True
    
    def stop_simulation(ev):
        nonlocal running
        running = False
    
    # Botón para detener
    boton_detener = button(text="Detener simulación", bind=stop_simulation)
    created_objects.append(boton_detener)
    
    while running:
        rate(200)  # control animation speed

        # ODE: m x'' + b x' + k x = F(t)
        a = (F(t) - b*v - k*x) / m

        # Update velocity & position
        v += a * dt
        x += v * dt

        # Update mass position
        mass.pos = vector(x, 0, 0)

        # Update spring axis
        spring.axis = mass.pos - spring.pos

        # Update labels
        label_pos.text = f"Posición: {x:.2f} m"
        label_vel.text = f"Velocidad: {v:.2f} m/s"
        
        # Update time display
        salida_info.text = f"\nTiempo actual: {t:.2f} s\n"

        t += dt

    # Limpiar botón de detener
    boton_detener.delete()

# Botón para iniciar simulación
boton_iniciar = button(text="Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")