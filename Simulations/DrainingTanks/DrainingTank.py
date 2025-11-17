from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Vaciado de un tanque cilíndrico",
               width=900, height=600, background=color.white)

# lista para llevar los objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del modelo ---\n")

# Sliders con valores dinámicos
# --- Altura inicial ---
texto_h0 = wtext(text="Altura inicial (h₀): 2.00 m\n")

def actualizar_h0(s):
    texto_h0.text = f"Altura inicial (h₀): {s.value:.2f} m\n"

slider_h0 = slider(min=0.5, max=10, value=2, step=0.1, bind=actualizar_h0)


# --- Constante k ---
texto_k = wtext(text="\nConstante de vaciado (k): 0.40\n")

def actualizar_k(s):
    texto_k.text = f"\nConstante de vaciado (k): {s.value:.2f}\n"

slider_k = slider(min=0.05, max=1.5, value=0.4, step=0.05, bind=actualizar_k)


# --- Radio R ---
texto_R = wtext(text="\nRadio del tanque (R): 0.50 m\n")

def actualizar_R(s):
    texto_R.text = f"\nRadio del tanque (R): {s.value:.2f} m\n"

slider_R = slider(min=0.2, max=2.5, value=0.5, step=0.05, bind=actualizar_R)


wtext(text="\n")

# Salidas numéricas
salida_info = wtext(text="\nTiempo total: ---\n")

# -------------------------------------------------
# ECUACIÓN DIFERENCIAL
# -------------------------------------------------
def dhdt(h, k):
    return -k * np.sqrt(h)


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
    h0 = float(slider_h0.value)
    k = float(slider_k.value)
    R = float(slider_R.value)

    # Ocultar objetos previos
    hide_previous_objects()

    # Crear tanque y agua
    tanque = cylinder(pos=vector(0, 0, 0), axis=vector(0, 3, 0),
                      radius=R, opacity=0.15, color=color.gray(0.5))
    agua = cylinder(pos=vector(0, 0, 0), axis=vector(0, h0, 0),
                    radius=R * 0.98, color=color.cyan, opacity=0.6)
    label_h = label(text=f"Altura del agua: {h0:.2f} m",
                    pos=vector(0, 3.2, 0), box=False, height=20)

    created_objects.extend([tanque, agua, label_h])

    # Variables de simulación
    h = h0
    dt = 0.01
    tiempo_total = 0.0

    # Loop
    while h > 0:
        rate(60)

        # Euler
        h = max(h + dhdt(h, k) * dt, 0)

        tiempo_total += dt

        # Actualizar agua y etiqueta
        agua.axis = vector(0, h, 0)
        label_h.text = f"Altura del agua: {h:.2f} m"

    # Mostrar resultados
    salida_info.text = (f"\nTiempo total: {tiempo_total:.2f} s\n")


# Botón para iniciar simulación
boton = button(text="Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")
