import sys
sys.path.append("src")
from LiquidacionNomina import Liquida_nomina
from controller.UserController import ControladorUsuarios

detalles = {}
def validate_empty(value):
    return value if value else "0"

# Verificación de la tabla 'usuarios'
"""
Esto se hace debido a que la ejecución de las pruebas
ocasionalmente genera que se elimine la tabla
"""

import sys
sys.path.append("src")
from LiquidacionNomina import Liquida_nomina
from controller.UserController import ControladorUsuarios

detalles = {}

def validate_empty(value):
    return value if value else "0"

# Verificación de la tabla 'usuarios'
try:
    if ControladorUsuarios.TablaUsuariosExiste():
        print("La tabla 'usuarios' ya existe. Continuando...")
    else:
        print("La tabla 'usuarios' no existe. Creando tabla...")
        ControladorUsuarios.CrearTabla()
except Exception as e:
    print(f"Error verificando/creando la tabla: {str(e)}")

while True:
    try:
        print('1. Registrarse')
        print('2. Iniciar Sesión')
        print('3. Cambiar contraseña')
        print('4. Eliminar cuenta')
        opcion = input('Ingrese una opción poniendo el número correspondiente: ')

        if opcion == '1':
            cedula = int(input("Ingrese su número de cédula: "))
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            correo = input("Ingrese su correo: ")
            contrasena = input("Ingrese su contraseña: ")
            usuario = ControladorUsuarios.RegistrarUsuario(cedula, nombre, apellido, correo, contrasena)
            ControladorUsuarios.InsertarUsuario(usuario)
            print("Usuario registrado exitosamente.")

        elif opcion == '2':
            cedula = int(input("Ingrese su número de cédula: "))
            contrasena = input("Ingrese su contraseña: ")
            if ControladorUsuarios.IniciarSesion(cedula, contrasena):
                print("Inicio de sesión exitoso.")
                break
            print('No se pudo iniciar sesión correctamente.')

        elif opcion == '3':
            cedula = int(input("Ingrese su número de cédula: "))
            contrasena = input("Ingrese su contraseña: ")
            new_contrasena = input("Ingrese su nueva contraseña: ")
            ControladorUsuarios.CambiarContrasena(cedula, contrasena, new_contrasena)
            print("Contraseña cambiada exitosamente.")

        elif opcion == '4':
            cedula = int(input("Ingrese su número de cédula: "))
            contrasena = input("Ingrese su contraseña: ")
            ControladorUsuarios.EliminarCuenta(cedula, contrasena)
            print("Cuenta eliminada exitosamente.")
        
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")


print("Acceso completado")
print("<<< PROGRAM RUNNING >>>")
print("::::::::::::::::::::::::::::::::")
print("**NOTE: For data that does not apply to your profile, please leave it blank, just press ENTER and continue with the next data point")
print("----------------------------------------------------------------------")
monthly_salary = validate_empty(input("Enter your monthly income ($COP):"))
weeks_worked = validate_empty(input("Enter the number of weeks worked to settle:"))
time_worked_on_holidays = validate_empty(input("Enter the hours worked on holidays (ONLY IF APPLICABLE):"))
overtime_day_hours = validate_empty(input("Enter the number of daytime overtime hours worked (ONLY IF APPLICABLE):"))
overtime_night_hours = validate_empty(input("Enter the number of nighttime overtime hours worked (ONLY IF APPLICABLE):"))
overtime_holiday_hours = validate_empty(input("Enter the overtime hours worked on holidays (ONLY IF APPLICABLE):"))
leave_days = validate_empty(input("Enter the number of days you had on leave during the working period (ONLY IF APPLICABLE):"))
sick_days = validate_empty(input("If you had any sick leave during the working period, enter the number of days (ONLY IF APPLICABLE):"))

try:
    liquidacion = Liquida_nomina.Liquidacion(
        monthly_salary=monthly_salary, weeks_worked=weeks_worked, time_worked_on_holidays=time_worked_on_holidays,
                                  overtime_day_hours=overtime_day_hours, overtime_night_hours=overtime_night_hours, 
                                overtime_holiday_hours=overtime_holiday_hours, leave_days=leave_days, sick_days=sick_days
    )
    total_payment, detalles= liquidacion.CalcularLiquidacion()
    print(f"The total amount of your settlement is: {total_payment}")
except Exception as up_error:
    print("*** ERROR ***")
    print(str(up_error))
