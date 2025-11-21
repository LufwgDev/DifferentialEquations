📘 Proyecto de Simulaciones Interactivas de Ecuaciones Diferenciales
Modelos visuales, dinámicos y completamente paramétricos en Python

Este proyecto reúne un conjunto de simulaciones interactivas diseñadas para visualizar, experimentar y comprender el comportamiento de sistemas clásicos modelados por ecuaciones diferenciales.

Cada simulación es completamente parametrizable, animada en tiempo real y construida en un entorno unificado usando Python + VPython para la animación 3D y la interfaz con sliders.

El objetivo principal es que cualquier persona pueda manipular parámetros, observar cambios instantáneos y entender cómo se comporta cada modelo físico/matemático.

🚀 Simulaciones Incluidas
🧪 1. Tanque de Mezclas (TanqueDeMezclas.py)

Simulación del clásico problema de mezcla con entrada y salida de solución salina.

Incluye:

Concentración variable en el tanque

Flujo de entrada y salida ajustables

Visualización 3D del volumen y color del líquido (simula concentración)

Gráficas en tiempo real de la concentración

🕳️ 2. Vaciado de Tanques Cilíndricos (VaciadoDeTanques.py)

Basado en la ley de Torricelli.
Esta es una de las simulaciones más completas del proyecto.

Incluye:

Animación 3D del tanque y el nivel de agua bajando

Gráficas simultáneas de altura y volumen vs tiempo

Ecuación diferencial mostrada dinámicamente

Solución analítica calculada y mostrada paso a paso

Comparación entre solución numérica y teórica

Error porcentual en cada instante

Parámetros ajustables:

Altura inicial

Radio del tanque

Radio del orificio

Coeficiente de descarga

🔌 3. Circuito RLC (CircuitosRLC.py)

Simula:

Carga, corriente y tensión en el circuito

Los tres regímenes: subamortiguado, críticamente amortiguado y sobreamortiguado

Gráfica en tiempo real

Parámetros ajustables:

R (resistencia)

L (inductancia)

C (capacitancia)

Condiciones iniciales

Se utiliza SciPy/Numpy para el modelo matemático y VPython para visualizar componentes animados.

🌀 4. Sistema Masa–Resorte (SistemaMasaResorte.py)

Incluye:

Oscilación realista del resorte y la masa en 3D

Damping opcional

Constante k, masa m, y condiciones iniciales ajustables

Gráfica de desplazamiento vs tiempo

Animación suave y basada en el modelo diferencial

🧰 Tecnologías Utilizadas

El proyecto está completamente desarrollado en Python, bajo un único entorno coherente:

🔹 VPython

Motor gráfico 3D

Sliders, botones y texto interactivo

Permite animaciones físicas claras y didácticas

🔹 Numpy

Cálculos numéricos

Evaluación de ecuaciones diferenciales

🔹 SciPy (en algunos módulos, como CircuitosRLC)

Integración de ODEs

🔹 Matplotlib (cuando es necesario)

Gráficas adicionales

🔹 Pandas

Organización de datos (cuando hace falta)

Todo está pensado para ser ejecutado en un único entorno Python, sin depender de navegadores o motores de videojuegos.

🎛️ Interactividad

Cada simulación usa sliders y botones de VPython, permitiendo ajustar:

Condiciones iniciales

Parámetros físicos

Constantes del modelo

Características geométricas (como radios o volúmenes)

Los cambios se reflejan de inmediato en la animación 3D y en las gráficas numéricas.

⚠️ Posible Configuración Necesaria en Windows (VPython)

En algunos equipos con Windows es necesario habilitar rutas largas para que VPython funcione correctamente.

🔧 Habilitar Long Paths (método recomendado)

Presiona Win + R, escribe:

gpedit.msc


y presiona Enter.

Navega a:
Computer Configuration → Administrative Templates → System → Filesystem

Busca la opción:
Enable Win32 long paths

Ábrela y selecciona Enabled

Aplica los cambios y reinicia el computador

📦 Ejecución

Cualquier simulación puede iniciarse simplemente ejecutando su archivo:

python VaciadoDeTanques.py
python TanqueDeMezclas.py
python CircuitosRLC.py
python SistemaMasaResorte.py


Cada una abrirá su ventana 3D con controles interactivos listos para usar.

🎉 Objetivo General del Proyecto

Hacer que el estudio de ecuaciones diferenciales sea visual, intuitivo y manipulable, permitiendo ver cómo responden los sistemas reales cuando se ajustan sus parámetros fundamentales.