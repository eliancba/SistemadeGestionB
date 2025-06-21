import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# FUNCIONES
def conectar():
    return sqlite3.connect("productos.db")

def guardar():
    try: 
        codigo = e_codigo.get()
        articulo = e_articulo.get()
        entrada = int(e_entrada.get())
        precio_compra = float(e_compra.get())
        precio_venta = float(e_venta.get())
        salida = 0 
        stock = entrada
        fecha = datetime.now().strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Compruebe que todos los campos estan completos.")
        return
    
    if not codigo or not articulo:
        messagebox.showerror("Error", "Codigo y articulo son obligatorios.")
        return
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO productos (codigo, articulo, entrada, salida, stock, fecha_ingreso, precio_compra, precio_venta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, articulo, entrada, salida, stock, fecha, precio_compra, precio_venta))
        conn.commit()
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        limpiar_campos()
        cargar_productos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El codigo ya existe en la base.")
    conn.close()

def actualizar_precios(*args):
    try:
        compra = float(e_compra.get())
        venta = compra * 2
        e_venta.delete(0, tk.END)
        e_venta.insert(0, f"{venta:.2f}")
    except ValueError:
        e_venta.delete(0, tk.END)

def limpiar_campos():
    e_codigo.delete(0, tk.END)
    e_articulo.delete(0, tk.END)
    e_entrada.delete(0, tk.END)
    e_compra.delete(0, tk.END)
    e_venta.delete(0, tk.END)

def cargar_productos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, articulo, entrada, salida, stock, precio_compra, precio_venta FROM productos")
    for row in cursor.fetchall():
        tabla.insert("", "end", values=row)
    conn.close()

# INTERFAZ 

root = tk.Tk()
root.title("Sistema de Gestión de Productos")
root.geometry("850x600")
root.minsize(600,400)
root.maxsize(850,600)
root.iconbitmap("bonita icono.ico")

# FORMULARIO 

frm = tk.Frame(root)
frm.pack(pady=10)

tk.Label(frm, text="Código:").grid(row=0, column=0, sticky="e")
e_codigo = tk.Entry(frm)
e_codigo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frm, text="Artículo:").grid(row=1, column=0, sticky="e")
e_articulo = tk.Entry(frm)
e_articulo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frm, text="Entrada:").grid(row=2, column=0, sticky="e")
e_entrada = tk.Entry(frm)
e_entrada.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frm, text="Precio compra:").grid(row=3, column=0, sticky="e")
e_compra = tk.Entry(frm)
e_compra.grid(row=3, column=1, padx=5, pady=5)
e_compra.bind("<KeyRelease>", actualizar_precios)

tk.Label(frm, text="Precio venta:").grid(row=4, column=0, sticky="e")
e_venta = tk.Entry(frm)
e_venta.grid(row=4, column=1, padx=5, pady=5)

tk.Button(frm, text="Guardar producto", command=guardar).grid(row=5, columnspan=2, pady=15)

# TABLA

tk.Label(root, text="Productos cargados:", font=("Arial", 12)).pack(pady=10)

columnas = ("codigo", "articulo", "entrada", "salida", "stock", "precio_compra", "precio_venta")
tabla = ttk.Treeview(root, columns=columnas, show="headings", height=10)

for col in columnas:
    tabla.heading(col, text=col.capitalize())
    tabla.column(col, anchor="center", width=100)

tabla.pack(expand=True, fill="both", padx=20, pady=10)

# Inicializa la tabla al iniciar
cargar_productos()

root.mainloop()