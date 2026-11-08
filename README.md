# 🦺 Sistema Inteligente de Detección de EPPs en Obra

Sistema de **Visión Artificial y Deep Learning** desarrollado con **YOLOv8** y **OpenCV** para el monitoreo y prevención de riesgos laborales en obras de construcción. El sistema detecta en tiempo real si los trabajadores portan sus Equipos de Protección Personal obligatorios:

* ✅ **Casco de seguridad** (e infracción: `SIN-Casco`)
* ✅ **Chaleco reflectante** (e infracción: `SIN-Chaleco`)
* ✅ **Mascarilla** (e infracción: `SIN-Mascarilla`)
* ✅ **Persona, Maquinaria, Vehículos y Conos de seguridad**

---

## 📋 Requisitos Previos

* **Python 3.10 o superior** (probado y compatible con Python 3.14).
* Conexión a Internet (únicamente para descargar las librerías en la primera instalación).

---

## 🚀 Guía Rápida para Levantar el Proyecto

Siga estos sencillos pasos en su terminal de Windows (**PowerShell** o **CMD**):

### 1. Clonar el repositorio
```bash
git clone https://github.com/AldairGomez/Machine_Learning_Deep_Learning.git
cd Machine_Learning_Deep_Learning
```

### 2. Crear y activar el entorno virtual
Se recomienda usar un entorno virtual para aislar las dependencias:

**En Windows (PowerShell):**
```powershell
# Si PowerShell restringe la ejecución de scripts, ejecutar una sola vez:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

# Crear el entorno virtual:
python -m venv .venv

# Activar el entorno virtual:
.\.venv\Scripts\Activate.ps1
```

*(Sabrá que está activado porque verá `(.venv)` al inicio de su línea de comandos).*

### 3. Instalar las dependencias
Instale todas las librerías necesarias con una sola orden:
```powershell
pip install -r requirements.txt
```

---

## 🖥️ Cómo Ejecutar el Proyecto

### Opción A: Interfaz Gráfica de Usuario (Recomendado)
Para abrir la interfaz interactiva con botones para imágenes, videos y cámara en vivo:
```powershell
python interfaz.py
```

#### Funcionalidades de la Interfaz:
1. **Escaneo en Imágenes:**
   * Botones directos para **Imagen 1**, **Imagen 2**, **Imagen 3** e **Imagen 4** (cargadas desde la carpeta `imagenes prueba`).
   * Botón para buscar y analizar cualquier otra fotografía de su equipo.
2. **Escaneo en Videos:**
   * Botones directos para **Video 1** y **Video 2** (cargados desde la carpeta `video prueba`).
   * Botón para cargar cualquier otro archivo `.mp4`, `.avi`, etc.
3. **Monitoreo en Tiempo Real (Cámara Web / Celular):**
   * **Cámara Web:** Por defecto utiliza la cámara integrada de su laptop o PC.
   * **Cámara de Celular (IP Webcam):** Active la casilla *"Utilizar cámara de celular"*, ingrese la dirección IP que muestre la app en su teléfono móvil (por defecto viene sugerida `http://192.168.1.55:8080/video`) e inicie el monitoreo en vivo.
   * **Control de ventanas:** Puede cerrar cualquier video o cámara presionando la **"X"** de la ventana o la tecla **"q"**.

---

### Opción B: Cuaderno de Evidencias (Jupyter Notebook)
Para evaluar el cumplimiento de todas las evidencias de la rúbrica de SENATI:
* Abra el archivo **`Entregable_SENATI_EPP.ipynb`** directamente en **VS Code**, o ejecute:
```powershell
jupyter notebook
```
* **Contenido del cuaderno:**
  1. Preprocesamiento de imágenes (escala de grises, normalización $[0, 1]$, binarización y redimensionado).
  2. Ficha técnica de la arquitectura de la Red Neuronal Convolucional (YOLOv8 nano).
  3. Algoritmo de Regresión Lineal (horas de monitoreo vs. cumplimiento de seguridad).
  4. Algoritmo K-Means Clustering (agrupamiento de tamaños de EPPs para Anchor Boxes).
  5. Comparativa de exactitud entre algoritmos supervisados (KNN vs. SVM vs. CNN).
  6. Métricas de evaluación de 100 épocas de entrenamiento: Precisión (90%), Recall (73%), F1-Score (80.7%), mAP@50 (80.9%) y Matriz de Confusión.
  7. Detección visual sobre imágenes de obra con etiquetas traducidas al español.
  8. Respuestas fundamentadas a las 5 Preguntas Guías del documento de SENATI.

---

## 📊 Diagramas y Planos de Ingeniería Incluidos

El proyecto incluye los diagramas en alta resolución (300 DPI) con el cajetín oficial de SENATI:
* **`diagrama_1_despliegue.png`:** Diagrama de despliegue físico y topología de periféricos (red local Wi-Fi, smartphone con IP Webcam, router, laptop y Kaggle GPU).
* **`diagrama_2_flujo_operativo.png`:** Diagrama de flujo operativo y lógica de decisiones con alertas visuales de seguridad (cajas rojas para infracciones, cajas verdes para EPP conforme).
* **`diagrama_propuesta.html`:** Versión web interactiva del plano para exposiciones y presentaciones.

---

## 📂 Estructura del Repositorio

```text
Machine_Learning_Deep_Learning/
│
├── Construction-Safety/          # Dataset y pesos del modelo preentrenado
│   └── results_yolov8n_100e/     # Pesos (best.pt), matriz de confusión y curvas
│       └── kaggle/working/runs/detect/train/weights/best.pt
│
├── imagenes prueba/              # 4 fotografías de prueba (img1, img2, img3, img4)
├── video prueba/                 # 2 videos de prueba de obra (vid1.mp4, vid2.mp4)
│
├── interfaz.py                   # Interfaz gráfica principal (Tkinter + OpenCV)
├── main.py                       # Script secundario de ejecución por consola
├── Entregable_SENATI_EPP.ipynb   # Cuaderno Jupyter con todas las evidencias de SENATI
│
├── diagrama_1_despliegue.png      # Plano 1: Despliegue físico y periféricos (300 DPI)
├── diagrama_2_flujo_operativo.png # Plano 2: Flujo operativo y lógica SSOMA (300 DPI)
├── diagrama_propuesta.html       # Diagrama interactivo en HTML/CSS
│
├── requirements.txt              # Lista de librerías para replicar el entorno
├── .gitignore                    # Archivos y carpetas excluidos del repositorio Git
└── README.md                     # Guía de instalación y manual del proyecto
```

---

