#pip install vpython
from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Simulación de Circuito RLC",
               width=1400, height=800, background=color.white)

# Lista para objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del Circuito RLC ---\n")

# Sliders con valores dinámicos
# --- Resistencia ---
texto_R = wtext(text="Resistencia (R): 10.00 Ω\n")
def actualizar_R(s):
    texto_R.text = f"Resistencia (R): {s.value:.2f} Ω\n"
slider_R = slider(min=0.1, max=50.0, value=10.0, step=0.5, bind=actualizar_R)

# --- Inductancia ---
texto_L = wtext(text="\nInductancia (L): 1.00 H\n")
def actualizar_L(s):
    texto_L.text = f"\nInductancia (L): {s.value:.2f} H\n"
slider_L = slider(min=0.1, max=5.0, value=1.0, step=0.1, bind=actualizar_L)

# --- Capacitancia ---
texto_C = wtext(text="\nCapacitancia (C): 0.10 F\n")
def actualizar_C(s):
    texto_C.text = f"\nCapacitancia (C): {s.value:.2f} F\n"
slider_C = slider(min=0.01, max=1.0, value=0.1, step=0.01, bind=actualizar_C)

# --- Carga inicial ---
texto_Q0 = wtext(text="\nCarga inicial (Q₀): 1.00 C\n")
def actualizar_Q0(s):
    texto_Q0.text = f"\nCarga inicial (Q₀): {s.value:.2f} C\n"
slider_Q0 = slider(min=0.0, max=5.0, value=1.0, step=0.1, bind=actualizar_Q0)

# --- Corriente inicial ---
texto_I0 = wtext(text="\nCorriente inicial (I₀): 0.00 A\n")
def actualizar_I0(s):
    texto_I0.text = f"\nCorriente inicial (I₀): {s.value:.2f} A\n"
slider_I0 = slider(min=-2.0, max=2.0, value=0.0, step=0.1, bind=actualizar_I0)

# --- Voltaje de fuente ---
texto_V0 = wtext(text="\nVoltaje fuente (V₀): 5.00 V\n")
def actualizar_V0(s):
    texto_V0.text = f"\nVoltaje fuente (V₀): {s.value:.2f} V\n"
slider_V0 = slider(min=0.0, max=20.0, value=5.0, step=0.5, bind=actualizar_V0)

# --- Frecuencia de fuente ---
texto_omega = wtext(text="\nFrecuencia fuente (ω): 2.00 rad/s\n")
def actualizar_omega(s):
    texto_omega.text = f"\nFrecuencia fuente (ω): {s.value:.2f} rad/s\n"
slider_omega = slider(min=0.0, max=10.0, value=2.0, step=0.5, bind=actualizar_omega)

wtext(text="\n")

# Mostrar ecuación diferencial
ecuacion_text = wtext(text="\nEcuación: L·Q'' + R·Q' + Q/C = V₀·cos(ω·t)\n")
wtext(text="(donde Q es la carga e I = Q' es la corriente)\n")

# Salidas numéricas
salida_info = wtext(text="\nTiempo actual: 0.00 s\n")

# -------------------------------------------------
# FUNCIONES DE SIMULACIÓN
# -------------------------------------------------

def hide_previous_objects():
    global created_objects
    for obj in created_objects:
        try:
            obj.visible = False
        except:
            pass
    created_objects = []

def simular(ev):
    global created_objects

    # Leer parámetros desde sliders
    R = float(slider_R.value)
    L = float(slider_L.value)
    C = float(slider_C.value)
    Q0 = float(slider_Q0.value)
    I0 = float(slider_I0.value)
    V0 = float(slider_V0.value)
    omega = float(slider_omega.value)

    # Ocultar objetos previos
    hide_previous_objects()

    # Función de voltaje externo
    def V(t):
        return V0 * np.cos(omega * t)

    # ============================
    # CONFIGURACIÓN DE ESCENA
    # ============================
    
    # Dimensiones del circuito
    circuit_width = 8
    circuit_height = 4
    
    # Componentes del circuito (representación visual)
    # Fuente de voltaje (izquierda)
    source = cylinder(pos=vector(-circuit_width/2, 0, 0), 
                     axis=vector(0, circuit_height, 0),
                     radius=0.15, color=color.orange)
    source_label = label(pos=vector(-circuit_width/2 - 0.8, circuit_height/2, 0),
                        text="V(t)", height=14, box=False, color=color.black)
    
    # Resistencia (arriba)
    resistor = box(pos=vector(0, circuit_height, 0),
                  size=vector(1.5, 0.3, 0.3),
                  color=color.red)
    resistor_label = label(pos=vector(0, circuit_height + 0.5, 0),
                          text=f"R={R:.1f}Ω", height=12, box=False, color=color.black)
    
    # Inductancia (derecha superior)
    inductor = helix(pos=vector(circuit_width/2 - 1, circuit_height, 0),
                    axis=vector(0, -1.5, 0),
                    radius=0.3, coils=8, thickness=0.08,
                    color=color.blue)
    inductor_label = label(pos=vector(circuit_width/2 + 0.8, circuit_height - 0.75, 0),
                          text=f"L={L:.1f}H", height=12, box=False, color=color.black)
    
    # Capacitor (derecha inferior)
    cap1 = box(pos=vector(circuit_width/2, 1.0, 0),
              size=vector(0.3, 0.8, 0.6), color=color.green)
    cap2 = box(pos=vector(circuit_width/2, 0.5, 0),
              size=vector(0.3, 0.8, 0.6), color=color.green)
    capacitor_label = label(pos=vector(circuit_width/2 + 0.8, 0.75, 0),
                           text=f"C={C:.2f}F", height=12, box=False, color=color.black)
    
    # Cables del circuito
    wire1 = cylinder(pos=vector(-circuit_width/2, circuit_height, 0),
                    axis=vector(circuit_width/2 - 0.75, 0, 0),
                    radius=0.05, color=color.gray(0.3))
    wire2 = cylinder(pos=vector(circuit_width/2 - 0.75, circuit_height, 0),
                    axis=vector(0.75, 0, 0),
                    radius=0.05, color=color.gray(0.3))
    wire3 = cylinder(pos=vector(circuit_width/2, 0, 0),
                    axis=vector(-circuit_width, 0, 0),
                    radius=0.05, color=color.gray(0.3))
    
    # Partícula que representa la carga en movimiento
    charge = sphere(pos=vector(-circuit_width/2, 0, 0),
                   radius=0.25, color=color.yellow,
                   make_trail=True, trail_type="points",
                   trail_radius=0.08, interval=5, retain=100)
    
    # Labels informativos
    label_Q = label(text=f"Carga: {Q0:.2f} C", pos=vector(0, -2, 0),
                   box=False, height=16, color=color.black)
    label_I = label(text=f"Corriente: {I0:.2f} A", pos=vector(0, -2.5, 0),
                   box=False, height=16, color=color.black)
    label_V = label(text=f"Voltaje: {V(0):.2f} V", pos=vector(0, -3.0, 0),
                   box=False, height=16, color=color.black)
    
    # Indicador de tipo de amortiguamiento
    label_tipo = label(text="", pos=vector(0, -3.5, 0),
                      box=True, height=14, color=color.black)
    
    # Calcular tipo de amortiguamiento
    discriminante = (R/(2*L))**2 - 1/(L*C)
    if discriminante > 0:
        tipo_amort = "Sobreamortiguado"
        label_tipo.color = color.blue
    elif discriminante < 0:
        tipo_amort = "Subamortiguado (oscilatorio)"
        label_tipo.color = color.red
    else:
        tipo_amort = "Críticamente amortiguado"
        label_tipo.color = color.green
    label_tipo.text = f"Régimen: {tipo_amort}"
    
    created_objects.extend([source, source_label, resistor, resistor_label,
                           inductor, inductor_label, cap1, cap2, capacitor_label,
                           wire1, wire2, wire3, charge, label_Q, label_I, label_V,
                           label_tipo])

    # ============================
    # VARIABLES DE SIMULACIÓN
    # ============================
    t = 0
    dt = 0.005
    Q = Q0
    I = I0  # I = dQ/dt
    
    # Puntos del circuito para la animación de la carga
    circuit_path = []
    # Lado izquierdo (subiendo)
    for y in np.linspace(0, circuit_height, 30):
        circuit_path.append(vector(-circuit_width/2, y, 0))
    # Arriba (hacia la derecha)
    for x in np.linspace(-circuit_width/2, circuit_width/2, 40):
        circuit_path.append(vector(x, circuit_height, 0))
    # Derecha (bajando)
    for y in np.linspace(circuit_height, 0, 30):
        circuit_path.append(vector(circuit_width/2, y, 0))
    # Abajo (hacia la izquierda)
    for x in np.linspace(circuit_width/2, -circuit_width/2, 40):
        circuit_path.append(vector(x, 0, 0))
    
    path_index = 0
    charge_speed = 2.0  # velocidad base de animación

    # ============================
    # BUCLE DE SIMULACIÓN
    # ============================
    running = True
    
    def stop_simulation(ev):
        nonlocal running
        running = False
    
    boton_detener = button(text="Detener simulación", bind=stop_simulation)
    created_objects.append(boton_detener)
    
    while running:
        rate(100)

        # EDO: L·Q'' + R·Q' + Q/C = V(t)
        # donde Q'' = dI/dt
        dI_dt = (V(t) - R*I - Q/C) / L

        # Actualizar corriente y carga
        I += dI_dt * dt
        Q += I * dt

        # Actualizar etiquetas
        label_Q.text = f"Carga: {Q:.3f} C"
        label_I.text = f"Corriente: {I:.3f} A"
        label_V.text = f"Voltaje: {V(t):.3f} V"
        
        # Actualizar tiempo
        salida_info.text = f"\nTiempo actual: {t:.2f} s\n"

        # Animar la carga moviéndose por el circuito
        # La velocidad de la partícula es proporcional a la corriente
        speed_factor = charge_speed * abs(I)
        steps = max(1, int(speed_factor * 10 * dt))
        
        for _ in range(steps):
            if I > 0:  # Corriente positiva (sentido normal)
                path_index = (path_index + 1) % len(circuit_path)
            else:  # Corriente negativa (sentido inverso)
                path_index = (path_index - 1) % len(circuit_path)
            
        charge.pos = circuit_path[path_index]
        
        # Cambiar color de la carga según la magnitud de la corriente
        intensity = min(abs(I) / 2.0, 1.0)
        charge.color = vector(1, 1-intensity, 0)  # De amarillo a naranja
        
        t += dt

    boton_detener.delete()

# Botón para iniciar simulación
boton_iniciar = button(text="Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")