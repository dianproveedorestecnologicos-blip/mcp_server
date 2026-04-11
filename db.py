import pymysql

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="julian",
        password="julidar123",   # en Laragon muchas veces root no tiene contraseña
        database="mcp_inventario",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )