
import sys
sys.path.append( "src" )
sys.path.append(".")


import psycopg2
from psycopg2 import sql
from model.Usuario import Usuario
import controller.SecretConfig


class ControladorUsuarios :

    def CrearTabla():
        """ Crea la tabla de usuario en la BD """
        cursor = ControladorUsuarios.ObtenerCursor()

        cursor.execute("""create table usuarios (
            cedula integer  NOT NULL,
            nombre text not null,
            apellido text not null,
            correo text,
            contrasena text,
            primary key (cedula)
            ); """)
        cursor.connection.commit()

    def EliminarTabla():
        """ Borra la tabla de usuarios de la BD """
        cursor = ControladorUsuarios.ObtenerCursor()

        cursor.execute("""drop table usuarios""" )
        # Confirma los cambios realizados en la base de datos
        # Si no se llama, los cambios no quedan aplicados
        cursor.connection.commit()


    def InsertarUsuario( usuario : Usuario ):
        """ Recibe un a instancia de la clase Usuario y la inserta en la tabla respectiva"""
        cursor = ControladorUsuarios.ObtenerCursor()
        cursor.execute( f"""insert into usuarios (cedula, nombre, apellido, correo, contrasena) 
                        values ('{usuario.cedula}', '{usuario.nombre}', '{usuario.apellido}', '{usuario.correo}', '{usuario.contrasena}')""" )

        cursor.connection.commit()

    def BuscarUsuarioCedula( cedula ):
        """ Trae un usuario de la tabla de usuarios por la cedula """
        cursor = ControladorUsuarios.ObtenerCursor()

        cursor.execute(f"""select cedula, nombre, apellido, correo, contrasena
        from usuarios where cedula = {cedula}""" )
        fila = cursor.fetchone()
        resultado = Usuario( cedula=fila[0], nombre=fila[1], apellido=fila[2], correo=fila[3] , contrasena=fila[4] )
        return resultado

    def ObtenerCursor():
        """ Crea la conexion a la base de datos y retorna un cursor para hacer consultas """
        connection = psycopg2.connect(database=controller.SecretConfig.PGDATABASE, user=controller.SecretConfig.PGUSER, password=controller.SecretConfig.PGPASSWORD, host=controller.SecretConfig.PGHOST, port=controller.SecretConfig.PGPORT)
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor = connection.cursor()
        return cursor

    def RegistrarUsuario(cedula, nombre, apellido, correo, contrasena):
        usuario:Usuario = Usuario(cedula, nombre, apellido, correo, contrasena)
        return usuario
    
    def IniciarSesion(cedula, contrasena:str):
        usuario = ControladorUsuarios.BuscarUsuarioCedula(cedula)        
        if usuario.contrasena == contrasena:
            return True
        return False

    def CambiarContrasena(cedula, contrasena, new_contrasena):
        if ControladorUsuarios.IniciarSesion(cedula, contrasena):
            cursor = ControladorUsuarios.ObtenerCursor()
            cursor.execute(f"""UPDATE usuarios set contrasena = '{new_contrasena}' WHERE cedula = '{cedula}' """)
            cursor.connection.commit()
            return True
        raise Exception
        

    def EliminarCuenta(cedula, contrasena):
        if ControladorUsuarios.IniciarSesion(cedula, contrasena):
            cursor = ControladorUsuarios.ObtenerCursor()
            cursor.execute(f"""DELETE FROM usuarios WHERE cedula = '{cedula}' """)
            cursor.connection.commit()
            return True

    @staticmethod
    def TablaUsuariosExiste():
        """Verifica si la tabla 'usuarios' ya existe en la base de datos."""
        cursor = ControladorUsuarios.ObtenerCursor()
        try:
            query = sql.SQL("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'usuarios'
                );
            """)
            cursor.execute(query)
            existe = cursor.fetchone()[0]
            return existe  # True si la tabla existe, False en caso contrario
        except psycopg2.Error as e:
            print(f"Error al verificar la tabla: {e}")
            return False
        finally:
            cursor.connection.close()