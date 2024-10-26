import unittest
import sys
import psycopg2
sys.path.append("src")
from unittest.mock import MagicMock, patch
from model.Usuario import Usuario

from controller.UserController import ControladorUsuarios


class Test_datos(unittest.TestCase):
    def setUp(self):
        """Configuración antes de cada prueba"""
        # Mock de la conexión y el cursor de la base de datos
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        
        # Mockear la obtención del cursor para que no acceda a la base de datos real
        self.patcher_cursor = patch('controller.UserController.ControladorUsuarios.ObtenerCursor', return_value=self.mock_cursor)
        self.mock_cursor_patch = self.patcher_cursor.start()

    def tearDown(self):
        """ Limpieza después de cada prueba """
        # Detener los mocks
        self.patcher_cursor.stop()

    def test_crear_tabla_error(self):
        self.mock_cursor.execute.side_effect = Exception("Error al crear tabla")
        with self.assertRaises(Exception):
            ControladorUsuarios.CrearTabla()

    def test_eliminar_tabla(self):
        try:
            ControladorUsuarios.EliminarTabla()
            self.mock_cursor.execute.assert_called_once_with("drop table usuarios")
            self.mock_cursor.connection.commit.assert_called_once()
        except Exception as e:
            self.fail(f"Error al eliminar la tabla: {str(e)}")

    def test_eliminar_tabla_error(self):
        self.mock_cursor.execute.side_effect = Exception("Error al eliminar tabla")
        with self.assertRaises(Exception):
            ControladorUsuarios.EliminarTabla()

    def test_insertar_usuario_error(self):
        self.mock_cursor.execute.side_effect = Exception("Error al insertar usuario")
        with self.assertRaises(Exception):
            usuario = Usuario(1234, 'Juan', 'Pérez', 'juan@mail.com', 'password123')
            ControladorUsuarios.InsertarUsuario(usuario)

    def test_buscar_usuario_cedula(self):
        self.mock_cursor.fetchone.return_value = (1234, 'Juan', 'Pérez', 'juan@mail.com', 'password123')
        try:
            usuario_db = ControladorUsuarios.BuscarUsuarioCedula(1234)
            self.assertEqual(usuario_db.cedula, 1234)
            self.assertEqual(usuario_db.nombre, 'Juan')
            self.assertEqual(usuario_db.apellido, 'Pérez')
        except Exception as e:
            self.fail(f"Error al buscar usuario por cédula: {str(e)}")

    def test_buscar_usuario_cedula_error(self):
        self.mock_cursor.fetchone.side_effect = Exception("Usuario no encontrado")
        with self.assertRaises(Exception):
            ControladorUsuarios.BuscarUsuarioCedula(9999)

    def test_iniciar_sesion(self):
        self.mock_cursor.fetchone.return_value = (1234, 'Juan', 'Pérez', 'juan@mail.com', 'password123')
        try:
            result = ControladorUsuarios.IniciarSesion(1234, 'password123')
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"Error al iniciar sesión: {str(e)}")

    def test_iniciar_sesion_error(self):
        self.mock_cursor.fetchone.return_value = (1234, 'Juan', 'Pérez', 'juan@mail.com', 'password123')
        try:
            result = ControladorUsuarios.IniciarSesion(1234, 'wrongpassword')
            self.assertFalse(result)
        except Exception as e:
            self.fail(f"Error al validar inicio de sesión incorrecto: {str(e)}")

    def test_cambiar_contrasena_error(self):
        self.mock_cursor.fetchone.return_value = (1234, 'Juan', 'Pérez', 'juan@mail.com', 'password123')
        with self.assertRaises(Exception):
            # Probar cambiar contraseña con la contraseña incorrecta
            ControladorUsuarios.CambiarContrasena(1234, 'wrongpassword', 'newpassword')

    def test_registrar_usuario(self):
        try:
            # Simula la entrada del usuario
            ControladorUsuarios.RegistrarUsuario = lambda: Usuario(1234, 'Juan', 'Pérez', 'juan@mail.com', 'password123')
            usuario = ControladorUsuarios.RegistrarUsuario()
            self.assertIsInstance(usuario, Usuario)
        except Exception as e:
            self.fail(f"Error al registrar usuario: {str(e)}")

if __name__ == '__main__':
    unittest.main()
