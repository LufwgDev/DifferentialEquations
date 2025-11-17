from vpython import *
import time

scene.title = "Simulación: Vaciado de Tanques con Fluidos Diferentes"
scene.width = 1400
scene.height = 700
g = 9.8

# ---- Físicas de los fluidos ---- #
fluidos = {
    "Agua": {"rho": 1000, "Cd": 0.62, "color": color.cyan},
    "Aceite": {"rho": 900, "Cd": 0.55, "color": vector(1,0.7,0)},
    "Mercurio": {"rho": 13500, "Cd": 0.70, "color": color.gray(0.7)}
}

H0 = 2
radio = 1
A_tanque = pi * radio**2

diam_orificio = 0.1
A_orificio = pi * (diam_orificio/2)**2

dt = 0.01
paused = False

# ---- Variables independientes por tanque ---- #
niveles = {}
labels = {}
tiempos = {nombre: 0 for nombre in fluidos}
activo = {nombre: True for nombre in fluidos}

offsets = [-2.8, 0, 2.8]

# ---- Crear tanques ---- #
for i, (nombre, props) in enumerate(fluidos.items()):
    posx = offsets[i]

    cylinder(pos=vector(posx, 0, 0), axis=vector(0, 3, 0),
             radius=radio, opacity=0.25)

    niveles[nombre] = {
        "h": H0,
        "obj": cylinder(pos=vector(posx, 0, 0), axis=vector(0, H0, 0),
                        radius=radio, color=props["color"])
    }

    labels[nombre] = label(pos=vector(posx, 3.2, 0),
                           text=f"{nombre}\nh={H0:.2f} m\nTiempo: 0.00 s",
                           height=14, box=True)

# ---- Texto general ---- #
t_global = 0
txt_t = label(pos=vector(0, 4.2, 0), text="Tiempo Global: 0.00 s", height=18)

# NUEVO ➜ mostrar diámetro del orificio
txt_d = label(pos=vector(0, -0.9, 0),
              text=f"Diámetro del Orificio: {diam_orificio:.2f} m",
              height=16, box=True, color=color.white)

# ---- Controles ---- #
def toggle_pause(b):
    global paused
    paused = not paused
    b.text = "▶ Reanudar" if paused else "⏸ Pausar"

boton_pause = button(text="⏸ Pausar", bind=toggle_pause)
button(text="⏮ Reiniciar", bind=lambda b: reiniciar())

# ---- Sliders ---- #
def cambiar_altura(s):
    for nombre in niveles:
        if s.value > niveles[nombre]["h"]:
            niveles[nombre]["h"] = s.value
        niveles[nombre]["obj"].axis.y = niveles[nombre]["h"]
        

slider_altura = slider(min=0.5, max=3, value=H0,
                       bind=cambiar_altura, right=15)
wtext(text=" Altura inicial (m)       ")

def cambiar_diametro(s):
    global diam_orificio, A_orificio
    diam_orificio = s.value
    A_orificio = pi * (diam_orificio/2)**2
    txt_d.text = f"Diámetro del Orificio: {diam_orificio:.2f} m"  # 👌 se actualiza en vivo

slider_diam = slider(min=0.05, max=0.9, value=diam_orificio,
                     bind=cambiar_diametro, right=15)
wtext(text=" Diámetro orificio (m)\n\n")

# ---- Reiniciar ---- #
def reiniciar():
    global t_global, paused, tiempos, activo
    t_global = 0
    paused = False
    boton_pause.text = "⏸ Pausar"

    for nombre in niveles:
        niveles[nombre]["h"] = slider_altura.value
        niveles[nombre]["obj"].axis.y = slider_altura.value
        tiempos[nombre] = 0
        activo[nombre] = True
        labels[nombre].text = f"{nombre}\nh={slider_altura.value:.2f} m\nTiempo: 0.00 s"

# ---- Simulación ---- #
while True:
    rate(60)
    if paused:
        continue

    t_global += dt
    txt_t.text = f"Tiempo Global: {t_global:.2f} s"

    for nombre, props in fluidos.items():
        if not activo[nombre]:
            continue

        h = niveles[nombre]["h"]

        if h <= 0:
            activo[nombre] = False
            continue

        Cd = props["Cd"]
        v = Cd * sqrt(2 * g * h)
        dh = (A_orificio / A_tanque) * v * dt

        h = max(h - dh, 0)
        niveles[nombre]["h"] = h
        niveles[nombre]["obj"].axis.y = h

        tiempos[nombre] += dt

        labels[nombre].text = (
            f"{nombre}\nh={h:.2f} m\n"
            f"Tiempo: {tiempos[nombre]:.2f} s"
        )
