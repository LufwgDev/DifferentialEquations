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
scene = canvas(title="Tanque de mezcla: concentración y nivel",
               width=1000, height=700, background=color.gray(0.2))
scene.center = vector(0, 2, 0)

# lista para llevar los objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del Tanque de Mezcla ---\n")

# Sliders con valores dinámicos
# --- Caudal de entrada ---
texto_Qin = wtext(text="Caudal de entrada (Qin): 0.025 m³/s\n")
def actualizar_Qin(s):
    texto_Qin.text = f"Caudal de entrada (Qin): {s.value:.3f} m³/s\n"
slider_Qin = slider(min=0.005, max=0.1, value=0.025, step=0.005, bind=actualizar_Qin)

# --- Caudal de salida ---
texto_Qout = wtext(text="\nCaudal de salida (Qout): 0.015 m³/s\n")
def actualizar_Qout(s):
    texto_Qout.text = f"\nCaudal de salida (Qout): {s.value:.3f} m³/s\n"
slider_Qout = slider(min=0.005, max=0.1, value=0.015, step=0.005, bind=actualizar_Qout)

# --- Concentración de entrada ---
texto_Cin = wtext(text="\nConcentración de entrada (Cin): 8.00 g/L\n")
def actualizar_Cin(s):
    texto_Cin.text = f"\nConcentración de entrada (Cin): {s.value:.2f} g/L\n"
slider_Cin = slider(min=0.0, max=20.0, value=8.0, step=0.5, bind=actualizar_Cin)

# --- Altura inicial del agua ---
texto_h0 = wtext(text="\nAltura inicial del agua: 0.50 m\n")
def actualizar_h0(s):
    texto_h0.text = f"\nAltura inicial del agua: {s.value:.2f} m\n"
slider_h0 = slider(min=0.1, max=3.5, value=0.5, step=0.1, bind=actualizar_h0)

# --- Radio del tanque ---
texto_radio = wtext(text="\nRadio del tanque: 1.50 m\n")
def actualizar_radio(s):
    texto_radio.text = f"\nRadio del tanque: {s.value:.2f} m\n"
slider_radio = slider(min=0.5, max=3.0, value=1.5, step=0.1, bind=actualizar_radio)

wtext(text="\n")

# Mostrar ecuaciones diferenciales
ecuacion_text = wtext(text="\nEcuaciones:\n  dC/dt = (Qin·Cin - Qout·C) / V\n  dH/dt = (Qin - Qout) / A\n")

# Salidas numéricas
salida_info = wtext(text="\nTiempo: 0.0 s | Nivel: 0.0 m | Concentración: 0.0 g/L\n")

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

# Conversión de concentración a color
def concentration_to_color(C, Cmax=20):
    """Color entre azul (0 g/L) y rojo (Cmax g/L)."""
    ratio = min(max(C / Cmax, 0), 1)
    return vector(ratio, 0.4 + 0.4*(1 - ratio), 1 - ratio)

# Simulación
def simular(ev):
    global created_objects

    # Leer parámetros desde sliders
    Qin = float(slider_Qin.value)
    Qout = float(slider_Qout.value)
    Cin = float(slider_Cin.value)
    water_height0 = float(slider_h0.value)
    tank_radius = float(slider_radio.value)
    
    # Parámetros calculados
    tank_height = 4.0      # m
    A = np.pi * tank_radius**2  # área transversal (m²)
    V = A * tank_height     # volumen total del tanque (m³)

    # Ocultar objetos previos
    hide_previous_objects()

    # ============================
    # CONFIGURACIÓN DE ESCENA
    # ============================
    
    # Crear tanque
    tank = cylinder(pos=vector(0, 0, 0), axis=vector(0, tank_height, 0),
                    radius=tank_radius, opacity=0.15, color=color.white)
    
    # Crear líquido
    water = cylinder(pos=vector(0, 0, 0), axis=vector(0, water_height0, 0),
                     radius=tank_radius*0.99, color=color.cyan, opacity=0.8)
    
    # Entradas y salidas
    inlet = cylinder(pos=vector(-tank_radius-0.5, tank_height*0.9, 0),
                     axis=vector(0.6, 0, 0), radius=0.05, color=color.blue)
    outlet = cylinder(pos=vector(tank_radius+0.1, 0, 0),
                      axis=vector(0.6, 0, 0), radius=0.05, color=color.red)
    
    # Gota de entrada
    drop = sphere(pos=inlet.pos + vector(0.6, 0, 0),
                  radius=0.06, color=color.blue, make_trail=True, retain=10)
    
    # Texto informativo
    info = label(pos=vector(0, tank_height + 0.7, 0),
                 text="", height=16, box=False, color=color.white)
    
    # Indicador de concentración (barra de color)
    conc_indicator = box(pos=vector(tank_radius+1, tank_height/2, 0), 
                         size=vector(0.3, tank_height, 0.3), 
                         color=concentration_to_color(0))
    conc_label = label(pos=vector(tank_radius+1.5, tank_height+0.3, 0),
                       text="Conc.", height=12, box=False, color=color.white)
    
    created_objects.extend([tank, water, inlet, outlet, drop, info, conc_indicator, conc_label])

    # ============================
    # VARIABLES DE SIMULACIÓN
    # ============================
    t = 0
    dt = 0.1
    C = 0.0        # g/L (inicialmente pura)
    water_height = water_height0

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
        rate(60)

        # EDO de concentración
        dCdt = (Qin*Cin - Qout*C) / (A * water_height) if water_height > 0 else 0
        C += dCdt * dt

        # EDO de nivel (balance de volumen)
        dHdt = (Qin - Qout) / A
        water_height += dHdt * dt
        t += dt

        # Condiciones de parada
        if water_height <= 0:
            water_height = 0
            info.text = f"Tanque vacío.\nTiempo: {t:.1f}s\nC: {C:.2f} g/L"
            break
        if water_height >= tank_height:
            water_height = tank_height
            info.text = f"Tanque lleno.\nTiempo: {t:.1f}s\nC: {C:.2f} g/L"
            break

        # Actualiza color del líquido
        water.color = concentration_to_color(C)

        # Actualiza nivel del agua
        water.axis = vector(0, water_height, 0)

        # Actualiza indicador de concentración
        conc_indicator.color = concentration_to_color(C)

        # Movimiento de la gota
        drop.pos.x += 0.08
        if drop.pos.x > inlet.pos.x + 0.6:
            drop.pos = inlet.pos + vector(0, 0, 0)
            drop.clear_trail()

        # Texto informativo
        info.text = (f"t = {t:.1f} s\n"
                     f"Nivel: {water_height:.2f} m\n"
                     f"C(t): {C:.2f} g/L")
        
        # Actualizar información general
        salida_info.text = f"\nTiempo: {t:.1f} s | Nivel: {water_height:.2f} m | Concentración: {C:.2f} g/L\n"

    # Limpiar botón de detener
    boton_detener.delete()

# Botón para iniciar simulación
boton_iniciar = button(text="Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")