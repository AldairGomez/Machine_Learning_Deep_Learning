from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from ultralytics import YOLO

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carpetas de archivos multimeadia de pruebas
CARPETA_IMAGENES = BASE_DIR / "imagenes prueba"
CARPETA_VIDEOS = BASE_DIR / "video prueba"

# Ruta del modelo entrenado
RUTA_MODELO = BASE_DIR / "Construction-Safety" / "results_yolov8n_100e" / "kaggle" / "working" / "runs" / "detect" / "train" / "weights" / "best.pt"

# Diccionario de traducción de etiquetas al español
NOMBRES_ESPAÑOL = {
    0: 'Casco',
    1: 'Mascarilla',
    2: 'Sin-Casco',
    3: 'Sin-Mascarilla',
    4: 'Sin-Chaleco',
    5: 'Persona',
    6: 'Cono de seguridad',
    7: 'Chaleco',
    8: 'Maquinaria',
    9: 'Vehiculo'
}


# Cargamos el modelo de Yolo
if not RUTA_MODELO.exists():
    messagebox.showerror("Error", f"No se encontró el archivo de pesos en:\n{RUTA_MODELO}")
    modelo = None
else:
    modelo = YOLO(str(RUTA_MODELO))
    if hasattr(modelo, "model") and hasattr(modelo.model, "names"):
        modelo.model.names = NOMBRES_ESPAÑOL


# FUNCIONES DE PROCESAMIENTO DE IMAGENES
def analizar_imagen(ruta_archivo):
    if modelo is None:
        messagebox.showerror("Error", "El modelo no se encuentra cargado.")
        return

    ruta = Path(ruta_archivo)
    if not ruta.exists():
        messagebox.showwarning("Atención", f"No se encontró la imagen en:\n{ruta}")
        return

    frame = cv2.imread(str(ruta))
    if frame is None:
        messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{ruta}")
        return

    # Realizar la prediccion con el modelo
    resultados = modelo(frame)
    if resultados and len(resultados) > 0:
        frame_anotado = resultados[0].plot()
    else:
        frame_anotado = frame

    nombre_ventana = f"Deteccion de EPPs: {ruta.name}"
    cv2.imshow(nombre_ventana, frame_anotado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def abrir_imagen_1():
    analizar_imagen(CARPETA_IMAGENES / "img1.jpg")

def abrir_imagen_2():
    analizar_imagen(CARPETA_IMAGENES / "img2.jpg")

def abrir_imagen_3():
    analizar_imagen(CARPETA_IMAGENES / "img3.jpg")

def abrir_imagen_4():
    analizar_imagen(CARPETA_IMAGENES / "img4.webp")

def seleccionar_otra_imagen():
    archivo = filedialog.askopenfilename(
        title="Seleccionar Imagen para Detección de EPPs",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.jfif *.webp *.bmp")]
    )
    if archivo:
        analizar_imagen(archivo)


# FUNCIONES DE PROCESAMIENTO DE VIDEOS

def reproducir_video(ruta_archivo):
    if modelo is None:
        messagebox.showerror("Error", "El modelo no se encuentra cargado.")
        return

    ruta = Path(ruta_archivo)
    if not ruta.exists():
        messagebox.showwarning("Atención", f"No se encontró el video en:\n{ruta}")
        return

    cap = cv2.VideoCapture(str(ruta))
    if not cap.isOpened():
        messagebox.showerror("Error", f"No se pudo abrir el archivo de video:\n{ruta}")
        return

    nombre_ventana = f"Deteccion de EPPs: {ruta.name}"

    while cap.isOpened():
        exito, frame = cap.read()
        if not exito:
            break

        resultados = modelo(frame)
        if resultados and len(resultados) > 0:
            frame_anotado = resultados[0].plot()
        else:
            frame_anotado = frame

        cv2.imshow(nombre_ventana, frame_anotado)

        # Salir si presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Cerrar ventana
        if cv2.getWindowProperty(nombre_ventana, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


def abrir_video_1():
    reproducir_video(CARPETA_VIDEOS / "vid1.mp4")

def abrir_video_2():
    reproducir_video(CARPETA_VIDEOS / "vid2.mp4")

def seleccionar_otro_video():
    archivo = filedialog.askopenfilename(
        title="Seleccionar Video para Detección de EPPs",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    if archivo:
        reproducir_video(archivo)

# FUNCIONES DE PROCESAMIENTO DE CÁMARA
def procesar_camara():
    if modelo is None:
        messagebox.showerror("Error", "El modelo no se encuentra cargado.")
        return

    usar_celular = variable_celular.get()

    if usar_celular == 1:
        # Modo camara de celular por IP Webcam
        url_camara = entrada_ip.get().strip()
        if not url_camara:
            messagebox.showwarning("Atención", "Por favor ingrese la URL que muestra la app IP Webcam en su celular.")
            return
        origen_camara = url_camara
    else:
        # Modo camara web integrada
        origen_camara = 0

    cap = cv2.VideoCapture(origen_camara)

    # Alerta si no se puede aperturar la camara
    if not cap.isOpened():
        cap.release()
        mensaje_error = (
            "No se detectó una cámara web disponible en su equipo.\n\n"
            "RECOMENDACIÓN:\n"
            "1. Instale la aplicación 'IP Webcam' en su teléfono móvil (Android/iOS).\n"
            "2. Conecte su teléfono a la misma red Wi-Fi que esta computadora.\n"
            "3. En la aplicación móvil, pulse 'Iniciar servidor'.\n"
            "4. Marque la casilla 'Utilizar cámara de celular (IP Webcam)'.\n"
            "5. Cambie la dirección IP por la que actualmente le muestra su celular."
        )
        messagebox.showwarning("Cámara no detectada", mensaje_error)
        return

    nombre_ventana = "Deteccion de EPPs en Tiempo Real"

    while cap.isOpened():
        exito, frame = cap.read()
        if not exito:
            messagebox.showwarning("Conexión perdida", "Se perdió la señal de la cámara.")
            break

        resultados = modelo(frame)
        if resultados and len(resultados) > 0:
            frame_anotado = resultados[0].plot()
        else:
            frame_anotado = frame

        cv2.imshow(nombre_ventana, frame_anotado)

        # Salir si presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Salir de la ventana
        if cv2.getWindowProperty(nombre_ventana, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


def actualizar_estado_celular():
    if variable_celular.get() == 1:
        entrada_ip.config(state="normal")
        # IP por defecto
        if not entrada_ip.get().strip():
            entrada_ip.insert(0, "http://192.168.1.55:8080/video")
        etiqueta_ip.config(fg="#d90429", text="IMPORTANTE: Cambie la IP por la que actualmente le muestra su celular:")
    else:
        entrada_ip.config(state="disabled")
        etiqueta_ip.config(fg="gray", text="Ruta IP de la cámara (se activará al marcar la casilla):")


# CONSTRUCCION DE LA INTERFAZ
ventana = tk.Tk()
ventana.title("SENATI - Sistema de Detección de EPPs")
ventana.geometry("620x760")
ventana.resizable(False, False)
ventana.config(bg="#f4f6f9")

# Titulo principal
marco_titulo = tk.Frame(ventana, bg="#0d3b66", pady=12)
marco_titulo.pack(fill="x")

lbl_titulo = tk.Label(
    marco_titulo,
    text="SISTEMA DE DETECCIÓN DE EPPs EN OBRA",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#0d3b66"
)
lbl_titulo.pack()

lbl_subtitulo = tk.Label(
    marco_titulo,
    text="Caso Práctico SENATI - Visión por Computadora (YOLOv8)",
    font=("Segoe UI", 9),
    fg="#e0e1dd",
    bg="#0d3b66"
)
lbl_subtitulo.pack()

#ESCANEO EN IMaGENES
marco_img = tk.LabelFrame(
    ventana,
    text=" 1. Escaneo de EPPs en Imágenes ",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#0d3b66",
    padx=15,
    pady=10
)
marco_img.pack(fill="x", padx=20, pady=8)

lbl_desc_img = tk.Label(
    marco_img,
    text="Selecciona una de las 4 imágenes de prueba o carga una desde tu equipo:",
    font=("Segoe UI", 9),
    bg="white",
    fg="#495057"
)
lbl_desc_img.pack(anchor="w", pady=(0, 6))

# Botones de imagenes de prueba
marco_botones_img = tk.Frame(marco_img, bg="white")
marco_botones_img.pack(fill="x", pady=2)

btn_img1 = tk.Button(
    marco_botones_img,
    text="📷 Imagen 1",
    font=("Segoe UI", 9, "bold"),
    bg="#e3f2fd",
    fg="#0d47a1",
    relief="groove",
    cursor="hand2",
    command=abrir_imagen_1,
    width=13,
    pady=4
)
btn_img1.grid(row=0, column=0, padx=4, pady=2)

btn_img2 = tk.Button(
    marco_botones_img,
    text="📷 Imagen 2",
    font=("Segoe UI", 9, "bold"),
    bg="#e3f2fd",
    fg="#0d47a1",
    relief="groove",
    cursor="hand2",
    command=abrir_imagen_2,
    width=13,
    pady=4
)
btn_img2.grid(row=0, column=1, padx=4, pady=2)

btn_img3 = tk.Button(
    marco_botones_img,
    text="📷 Imagen 3",
    font=("Segoe UI", 9, "bold"),
    bg="#e3f2fd",
    fg="#0d47a1",
    relief="groove",
    cursor="hand2",
    command=abrir_imagen_3,
    width=13,
    pady=4
)
btn_img3.grid(row=0, column=2, padx=4, pady=2)

btn_img4 = tk.Button(
    marco_botones_img,
    text="📷 Imagen 4",
    font=("Segoe UI", 9, "bold"),
    bg="#e3f2fd",
    fg="#0d47a1",
    relief="groove",
    cursor="hand2",
    command=abrir_imagen_4,
    width=13,
    pady=4
)
btn_img4.grid(row=0, column=3, padx=4, pady=2)

# Botón para seleccionar otra imagen desde la computadora
btn_otra_img = tk.Button(
    marco_img,
    text="📁  Seleccionar otra imagen desde la computadora...",
    font=("Segoe UI", 9),
    bg="#1976d2",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=seleccionar_otra_imagen,
    pady=4
)
btn_otra_img.pack(fill="x", pady=(6, 2))


#ESCANEO DE VIDEOS
marco_video = tk.LabelFrame(
    ventana,
    text=" 2. Escaneo de EPPs en Video ",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#0d3b66",
    padx=15,
    pady=10
)
marco_video.pack(fill="x", padx=20, pady=8)

lbl_desc_video = tk.Label(
    marco_video,
    text="Selecciona uno de los videos de prueba o carga uno desde tu equipo:",
    font=("Segoe UI", 9),
    bg="white",
    fg="#495057"
)
lbl_desc_video.pack(anchor="w", pady=(0, 6))

# Botones de videos prueba
marco_botones_vid = tk.Frame(marco_video, bg="white")
marco_botones_vid.pack(fill="x", pady=2)

btn_vid1 = tk.Button(
    marco_botones_vid,
    text="🎬 Video 1 (vid1.mp4)",
    font=("Segoe UI", 9, "bold"),
    bg="#e8f5e9",
    fg="#1b5e20",
    relief="groove",
    cursor="hand2",
    command=abrir_video_1,
    width=28,
    pady=4
)
btn_vid1.grid(row=0, column=0, padx=4, pady=2)

btn_vid2 = tk.Button(
    marco_botones_vid,
    text="🎬 Video 2 (vid2.mp4)",
    font=("Segoe UI", 9, "bold"),
    bg="#e8f5e9",
    fg="#1b5e20",
    relief="groove",
    cursor="hand2",
    command=abrir_video_2,
    width=28,
    pady=4
)
btn_vid2.grid(row=0, column=1, padx=4, pady=2)

# Botón para seleccionar otro video desde la computadora
btn_otro_video = tk.Button(
    marco_video,
    text="📁  Seleccionar otro video desde la computadora...",
    font=("Segoe UI", 9),
    bg="#2e7d32",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=seleccionar_otro_video,
    pady=4
)
btn_otro_video.pack(fill="x", pady=(6, 2))



#USO DE CAMARA WEB/CELULAR
marco_camara = tk.LabelFrame(
    ventana,
    text=" 3. Monitoreo en Tiempo Real (Cámara Web / Celular) ",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#0d3b66",
    padx=15,
    pady=10
)
marco_camara.pack(fill="x", padx=20, pady=8)

lbl_desc_cam = tk.Label(
    marco_camara,
    text="Por defecto usa la cámara web. Si usas tu celular, activa la casilla:",
    font=("Segoe UI", 9),
    bg="white",
    fg="#495057"
)
lbl_desc_cam.pack(anchor="w", pady=(0, 4))

# Checkbox para activar camara de celular
variable_celular = tk.IntVar(value=0)
chk_celular = tk.Checkbutton(
    marco_camara,
    text="Utilizar cámara de celular (IP Webcam)",
    variable=variable_celular,
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#0d3b66",
    activebackground="white",
    command=actualizar_estado_celular
)
chk_celular.pack(anchor="w", pady=(2, 4))

# Etiqueta con indicación para la IP
etiqueta_ip = tk.Label(
    marco_camara,
    text="IP de la cámara (se activará al marcar la casilla):",
    font=("Segoe UI", 8, "bold"),
    bg="white",
    fg="gray"
)
etiqueta_ip.pack(anchor="w")

# URL por defecto
entrada_ip = tk.Entry(
    marco_camara,
    font=("Consolas", 10),
    relief="solid",
    bd=1,
    state="disabled"
)
entrada_ip.insert(0, "http://192.168.1.55:8080/video")
entrada_ip.pack(fill="x", pady=(2, 8))

btn_camara = tk.Button(
    marco_camara,
    text="📹  Iniciar Monitoreo con Cámara",
    font=("Segoe UI", 10, "bold"),
    bg="#e65100",
    fg="white",
    padx=10,
    pady=6,
    relief="flat",
    cursor="hand2",
    command=procesar_camara
)
btn_camara.pack(fill="x")

# Iniciar la interfaz grafica
if __name__ == "__main__":
    ventana.mainloop()
