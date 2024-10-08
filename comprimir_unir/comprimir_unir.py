import subprocess  # Para ejecutar Ghostscript
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger
import os  # Importa os para verificar el tamaño del archivo

# Función para comprimir el PDF
def comprimir_pdf(input_file, output_file, calidad):
    try:
        # Comando para Ghostscript
        comando = [
            "gswin64c",  # Cambia a "gswin32c" si tienes la versión de 32 bits
            "-dNOPAUSE",
            "-dBATCH",
            "-sDEVICE=pdfwrite",
            "-dPDFSETTINGS=/" + calidad,  # Ajusta la calidad según la opción seleccionada
            "-dColorImageResolution=80",  # Disminuye la resolución de imágenes en color
            "-dGrayImageResolution=80",  # Disminuye la resolución de imágenes en escala de grises
            "-dMonoImageResolution=80",  # Disminuye la resolución de imágenes en blanco y negro
            "-dCompressFonts=true",  # Comprime las fuentes
            "-dDownsampleColorImages=true",  # Disminuye la resolución de imágenes en color
            "-dDownsampleGrayImages=true",  # Disminuye la resolución de imágenes en escala de grises
            "-dDownsampleMonoImages=true",  # Disminuye la resolución de imágenes en blanco y negro
            "-dDeleteUnusedObjects=true",  # Elimina objetos no utilizados
            f"-sOutputFile={output_file}",
            input_file
        ]
        
        # Ejecutar el comando
        subprocess.run(comando, check=True)

        # Verificar el tamaño del archivo comprimido
        tamaño_archivo = os.path.getsize(output_file)
        tamaño_maximo = 10 * 1024 * 1024  # 10 MB en bytes

        if tamaño_archivo > tamaño_maximo:
            messagebox.showwarning("Advertencia", "El tamaño del archivo comprimido excede los 10 MB.")
        else:
            messagebox.showinfo("Éxito", "PDF comprimido correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Función para unir varios PDFs
def unir_pdfs(files, output_file):
    try:
        print(f"Archivos seleccionados: {files}")  # Verifica que sean rutas válidas
        merger = PdfMerger()
        for pdf in files:
            merger.append(pdf)
        
        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Éxito", "PDFs unidos correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al unir los PDFs: {str(e)}")

# Función para seleccionar los archivos PDF a unir
def seleccionar_archivos_para_unir():
    archivos = filedialog.askopenfilenames(
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Selecciona archivos PDF para unir"
    )
    if archivos:
        archivos_a_unir.clear()  # Limpiar la lista antes de agregar los nuevos archivos
        archivos_a_unir.extend(archivos)  # Agregar los archivos seleccionados a la lista
        # Mostrar la lista de archivos seleccionados en el campo de entrada
        archivos_seleccionados.set("; ".join(archivos_a_unir))

# Función para seleccionar el archivo PDF de entrada
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Selecciona un archivo PDF"
    )
    if archivo:
        entrada.set(archivo)

# Función para seleccionar la ubicación del archivo PDF de salida
def guardar_archivo():
    archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar PDF comprimido"
    )
    if archivo:
        salida.set(archivo)

# Función para guardar el archivo unido
def guardar_archivo_unido():
    archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar PDF unido"
    )
    if archivo:
        salida_unido.set(archivo)

# Función para ejecutar la compresión
def ejecutar_compresion():
    if not entrada.get() or not salida.get():
        messagebox.showwarning("Advertencia", "Por favor selecciona un archivo de entrada y salida.")
    else:
        calidad = calidad_var.get()  # Obtener el nivel de calidad seleccionado
        comprimir_pdf(entrada.get(), salida.get(), calidad)

# Función para ejecutar la unión de PDFs
def ejecutar_union():
    if not archivos_a_unir or not salida_unido.get():
        messagebox.showwarning("Advertencia", "Por favor selecciona los archivos a unir y el archivo de salida.")
    else:
        unir_pdfs(archivos_a_unir, salida_unido.get())

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Compresor y Unión de PDF")

# Variables de archivo de entrada y salida
entrada = tk.StringVar()
salida = tk.StringVar()
archivos_a_unir = []  # Ahora es una lista, no un StringVar
archivos_seleccionados = tk.StringVar()  # Nueva variable para mostrar los archivos seleccionados
salida_unido = tk.StringVar()

# Variable para seleccionar calidad de compresión
calidad_var = tk.StringVar(value="ebook")  # Valor predeterminado

# Diseño de la ventana
tk.Label(ventana, text="Archivo PDF de entrada:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(ventana, textvariable=entrada, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(ventana, text="Seleccionar", command=seleccionar_archivo).grid(row=0, column=2, padx=10, pady=10)

tk.Label(ventana, text="Archivo PDF comprimido (salida):").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(ventana, textvariable=salida, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(ventana, text="Guardar", command=guardar_archivo).grid(row=1, column=2, padx=10, pady=10)

tk.Label(ventana, text="Calidad de compresión:").grid(row=2, column=0, padx=10, pady=10)
calidades = ["screen", "ebook", "printer", "prepress", "default"]  # Opciones de calidad
calidad_combobox = ttk.Combobox(ventana, textvariable=calidad_var, values=calidades)
calidad_combobox.grid(row=2, column=1, padx=10, pady=10)
calidad_combobox.set("ebook")  # Valor predeterminado

tk.Button(ventana, text="Comprimir PDF", command=ejecutar_compresion).grid(row=3, column=1, padx=10, pady=20)

# Funcionalidad para unir PDFs
tk.Label(ventana, text="Archivos PDF para unir:").grid(row=4, column=0, padx=10, pady=10)
tk.Entry(ventana, textvariable=archivos_seleccionados, width=50).grid(row=4, column=1, padx=10, pady=10)
tk.Button(ventana, text="Seleccionar archivos", command=seleccionar_archivos_para_unir).grid(row=4, column=2, padx=10, pady=10)

tk.Label(ventana, text="Archivo PDF unido (salida):").grid(row=5, column=0, padx=10, pady=10)
tk.Entry(ventana, textvariable=salida_unido, width=50).grid(row=5, column=1, padx=10, pady=10)
tk.Button(ventana, text="Guardar", command=guardar_archivo_unido).grid(row=5, column=2, padx=10, pady=10)

tk.Button(ventana, text="Unir PDFs", command=ejecutar_union).grid(row=6, column=1, padx=10, pady=20)

# Iniciar la aplicación
ventana.mainloop()
