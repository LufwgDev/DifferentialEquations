from vpython import *
import numpy as np

# -------------------------------------------------
# Parámetros del modelo (puedes hacerlos variables)
# -------------------------------------------------
h0 = 2.0        # altura inicial del agua (m)
k = 0.4         # constante de vaciado (1/s)
R = 0.5         # radio del tanque (m)

# -------------------------------------------------
# Escena 3D básica
# -------------------------------------------------
scene = canvas(title="Vaciado de un tanque cilíndrico",
               width=700, height=500, background=color.white)

# Cilindro exterior (tanque)
tanque = cylinder(pos=vector(0,0,0), axis=vector(0,3,0),
                  radius=R, opacity=0.15, color=color.gray(0.5))

# Nivel de agua (un cilindro interno cuyo alto cambia)
agua = cylinder(pos=vector(0,0,0), axis=vector(0,h0,0),
                radius=R*0.98, color=color.cyan, opacity=0.6)

# Etiqueta visible
label_h = label(text=f"Altura del agua: {h0:.2f} m",
                pos=vector(0,3.2,0), box=False, height=20)

# -------------------------------------------------
# Ecuación diferencial: dh/dt = -k * sqrt(h)
# -------------------------------------------------
def dhdt(h):
    return -k * np.sqrt(h)

# Integración simple (Euler)
def actualizar_altura(h, dt):
    return max(h + dhdt(h)*dt, 0)  # evita valores negativos


# -------------------------------------------------
# Loop principal de animación
# -------------------------------------------------
h = h0
dt = 0.01

while h > 0:
    rate(60)  # velocidad visual (fps)

    # Actualizar altura con la ED
    h = actualizar_altura(h, dt)

    # Actualizar visualmente el cilindro de agua
    agua.axis = vector(0, h, 0)

    # Actualizar etiqueta
    label_h.text = f"Altura del agua: {h:.2f} m"
