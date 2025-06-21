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

def registrar_entrada():
    codigo = e_codigo_entrada.get()
    cantidad = e_cantidad_entrada.get()

    if not codigo or not cantidad.isdigit():
        messagebox.showerror("Completa los campos")
        return
    
    cantidad = int(cantidad)
    fecha = datetime.now().strftime("%Y-%m-%d")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT stock FROM productos WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()

    if resultado:
        stock_actual = resultado[0]
        nuevo_stock = stock_actual + cantidad

        cursor.execute("UPDATE productos SET stock = stock + ?, entrada = entrada + ? WHERE codigo = ?", (cantidad, cantidad, codigo))

        cursor.execute("INSERT INTO entradas (codigo, cantidad, fecha) VALUES (?, ?, ?)", (codigo, cantidad, fecha))

        conn.commit()
        messagebox.showinfo("Éxito", f"Entrada registrada. Nuevo stock: {nuevo_stock}")
        e_codigo_entrada.delete(0, tk.END)
        e_cantidad_entrada.delete(0, tk.END)
        cargar_productos()
    else:
        messagebox.showerror("Error", "El código no existe en la base.")
    conn.close()

def registrar_venta():
    codigo = e_codigo_venta.get()
    cantidad = e_cantidad_venta.get()

    if not codigo or not cantidad.isdigit():
        messagebox.showerror("Error", "Completá correctamente")
        return
    
    cantidad = int(cantidad)
    fecha = datetime.now().strftime("%Y-%m-%d")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT stock, precio_venta FROM productos WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()

    if resultado:
        stock_actual, precio_venta = resultado
        if cantidad > stock_actual:
            messagebox.showerror("Error", f"No hay suficiente stock. Disponible: {stock_actual}")
            conn.close()
            return

        nuevo_stock = stock_actual - cantidad
        total = cantidad * precio_venta

        cursor.execute("UPDATE productos SET stock = ?, salida = salida + ? WHERE codigo = ?", (nuevo_stock, cantidad, codigo))

        cursor.execute("INSERT INTO ventas (codigo, cantidad, total, fecha_venta) VALUES (?, ?, ?, ?)", (codigo, cantidad, total, fecha))

        conn.commit()
        messagebox.showinfo("Venta registrada", f"Venta exitosa.\nTotal: ${total:.2f}\nStock restante: {nuevo_stock}")

        e_codigo_venta.delete(0, tk.END)
        e_cantidad_venta.delete(0, tk.END)

        cargar_productos()
    else:
        messagebox.showerror("Error", "El código no existe.")
    
    conn.close()    

# INTERFAZ 

root = tk.Tk()
root.title("Sistema de Gestión de Productos")
root.geometry("850x600")
root.minsize(600,400)
root.maxsize(850,600)
root.iconbitmap("bonita icono.ico")

# PESTAÑAS
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_agregar = ttk.Frame(notebook)
tab_entrada = ttk.Frame(notebook)
tab_venta = ttk.Frame(notebook)
tab_stock = ttk.Frame(notebook)

notebook.add(tab_agregar, text="➕ Agregar producto")
notebook.add(tab_entrada, text="🔄 Entrada de stock")
notebook.add(tab_venta, text="💸 Registrar venta")
notebook.add(tab_stock, text="📦 Ver productos")

# FORMULARIO PARA AGREGAR PRODUCTO

frm = tk.Frame(tab_agregar)
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


# PESTAÑA ENTRADA

frm_entrada = tk.Frame(tab_entrada)
frm_entrada.pack(pady=20)

tk.Label(frm_entrada, text="Código del producto:").grid(row=0, column=0, sticky="e")
e_codigo_entrada = tk.Entry(frm_entrada)
e_codigo_entrada.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frm_entrada, text="Cantidad a ingresar:").grid(row=1, column=0, sticky="e")
e_cantidad_entrada = tk.Entry(frm_entrada)
e_cantidad_entrada.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frm_entrada, text="Registrar entrada", command=registrar_entrada).grid(row=2, columnspan=2, pady=15)

# PESTAÑAS VENTAS 
frm_venta =tk.Frame(tab_venta)
frm_venta.pack(pady=20)

tk.Label(frm_venta, text="Código del producto:").grid(row=0, column=0, sticky="e")
e_codigo_venta = tk.Entry(frm_venta)
e_codigo_venta.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frm_venta, text="Cantidad a vender:").grid(row=1, column=0, sticky="e")
e_cantidad_venta = tk.Entry(frm_venta)
e_cantidad_venta.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frm_venta, text="Registrar venta", command=registrar_venta).grid(row=2, columnspan=2, pady=15)


# TABLA VER PRODUCTOS

tk.Label(tab_stock, text="Productos cargados:", font=("Arial", 12)).pack(pady=10)

columnas = ("codigo", "articulo", "entrada", "salida", "stock", "precio_compra", "precio_venta")
tabla = ttk.Treeview(tab_stock, columns=columnas, show="headings", height=10)

for col in columnas:
    tabla.heading(col, text=col.capitalize())
    tabla.column(col, anchor="center", width=100)

tabla.pack(expand=True, fill="both", padx=20, pady=10)

cargar_productos()

root.mainloop()