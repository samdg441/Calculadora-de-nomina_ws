import sys
sys.path.append("src")
sys.path.append(".")

import psycopg2
from psycopg2 import sql
from model.Usuario import Usuario
import controller.SecretConfig


class ControladorUsuarios:

    @staticmethod
    def ObtenerCursor():
        """ Crea la conexion a la base de datos y retorna un cursor para hacer consultas """
        connection = psycopg2.connect(database=controller.SecretConfig.PGDATABASE, 
                                       user=controller.SecretConfig.PGUSER, 
                                       password=controller.SecretConfig.PGPASSWORD, 
                                       host=controller.SecretConfig.PGHOST, 
                                       port=controller.SecretConfig.PGPORT)
        return connection.cursor(), connection  # Retorna cursor y conexión

    @staticmethod
    def CrearTabla():
        """ Crea la tabla de usuario en la BD """
        cursor, connection = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            cedula INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT,
            contrasena TEXT,
            PRIMARY KEY (cedula)
            ); """)
        connection.commit()
        connection.close()

    @staticmethod
    def EliminarTabla():
        """ Borra la tabla de usuarios de la BD """
        cursor, connection = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""DROP TABLE IF EXISTS usuarios;""")
        connection.commit()
        connection.close()

    @staticmethod
    def InsertarUsuario(usuario: Usuario):
        """ Recibe una instancia de la clase Usuario y la inserta en la tabla respectiva """
        cursor, connection = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""INSERT INTO usuarios (cedula, nombre, apellido, correo, contrasena) 
                          VALUES (%s, %s, %s, %s, %s)""", 
                       (usuario.cedula, usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena))
        connection.commit()
        connection.close()

    @staticmethod
    def BuscarUsuarioCedula(cedula):
        """ Trae un usuario de la tabla de usuarios por la cedula """
        cursor, connection = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""SELECT cedula, nombre, apellido, correo, contrasena
                          FROM usuarios WHERE cedula = %s;""", (cedula,))
        fila = cursor.fetchone()
        connection.close()
        if fila:
            return Usuario(cedula=fila[0], nombre=fila[1], apellido=fila[2], correo=fila[3], contrasena=fila[4])
        return None

    @staticmethod
    def MostrarUsuarios():
        """ Muestra todos los usuarios en la tabla """
        cursor, connection = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""SELECT cedula, nombre, apellido, correo,contrasena FROM usuarios;""")
        filas = cursor.fetchall()
        connection.close()
        usuarios = []
        for fila in filas:
            usuarios.append(Usuario(cedula=fila[0], nombre=fila[1], apellido=fila[2], correo=fila[3],contrasena=fila[4]))
        return usuarios

    @staticmethod
    def IniciarSesion(cedula, contrasena: str):
        usuario = ControladorUsuarios.BuscarUsuarioCedula(cedula)
        if usuario and usuario.contrasena == contrasena:
            return True
        return False

    @staticmethod
    def CambiarContrasena(cedula, contrasena, new_contrasena):
        if ControladorUsuarios.IniciarSesion(cedula, contrasena):
            cursor, connection = ControladorUsuarios.ObtenerCursor()
            cursor.execute("""UPDATE usuarios SET contrasena = %s WHERE cedula = %s;""", (new_contrasena, cedula))
            connection.commit()
            connection.close()
            return True
        raise Exception("Credenciales incorrectas")

    @staticmethod
    def EliminarCuenta(cedula, contrasena):
        if ControladorUsuarios.IniciarSesion(cedula, contrasena):
            cursor, connection = ControladorUsuarios.ObtenerCursor()
            cursor.execute("""DELETE FROM usuarios WHERE cedula = %s;""", (cedula,))
            connection.commit()
            connection.close()
            return True
        raise Exception("Credenciales incorrectas")

    @staticmethod
    def TablaUsuariosExiste():
        """ Verifica si la tabla 'usuarios' ya existe en la base de datos. """
        cursor, connection = ControladorUsuarios.ObtenerCursor()
        try:
            query = sql.SQL("""SELECT EXISTS (
                                SELECT 1 
                                FROM information_schema.tables 
                                WHERE table_schema = 'public' 
                                AND table_name = 'usuarios');""")
            cursor.execute(query)
            existe = cursor.fetchone()[0]
            return existe  # True si la tabla existe, False en caso contrario
        except psycopg2.Error as e:
            print(f"Error al verificar la tabla: {e}")
            return False
        finally:
            connection.close()
