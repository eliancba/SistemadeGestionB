import sqlite3

conn = sqlite3.connect("productos.db")
cursor = conn.cursor()

# CREACIÓN DE LA TABLA PRODUCTOS PARA ESTE SISTEMA :)

cursor.execute ('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    articulo TEXT NOT NULL,
    entrada INTEGER DEFAULT 0,
    salida INTEGER DEFAULT 0,
    stock INTEGER DEFAULT 0,
    fecha_ingreso TEXT,
    precio_compra REAL,
    precio_venta REAL
)
''')

# TABLA ENTRADAS (AGREGAR AL STOCK)

cursor.execute('''
CREATE TABLE IF NOT EXISTS entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_entrada TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)            
''')

# TABLA VENTAS (SALIDAS)

cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    total REAL,
    fecha_venta TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREING KEY (producto_id) REFERENCES productos(id)
)               
''')

conn.commit()
conn.close()
print("Base de datos creada con sus respectivas tablas :)")