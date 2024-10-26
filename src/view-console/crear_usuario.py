import sys
sys.path.append("src")

from model.Usuario import Usuario
from controller.UserController import ControladorUsuarios


# Insertar un Usuario en la tabla
usuario  = Usuario( cedula="", nombre="", apellido="", correo="")

print("Por favor ingrese los datos del usuario que desea crear")

usuario.cedula = input("Cedula : ")
usuario.nombre = input("Nombre : ")
usuario.apellido = input("Apellido : ")
usuario.correo = input("Correo : ")

ControladorUsuarios.InsertarUsuario( usuario )

print("Usuario insertado correctamente!")
