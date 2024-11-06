import sys
from flask import Flask, render_template, request
from LiquidacionNomina.Liquida_nomina import Liquidacion
from LiquidacionNomina import Validations  # Excepciones específicas
from controller.UserController import ControladorUsuarios
from model.Usuario import Usuario  # Verifica que la ruta sea correcta

# Agregar rutas a sys.path para evitar problemas de importación
sys.path.append("src")
sys.path.append(".")

app = Flask(__name__)

# Página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')

# Página de base de datos
@app.route('/basededatos')
def basededatos():
    return render_template('basededatos.html')

# Página para entrada de datos de liquidación
@app.route('/calcular')
def entrada_datos():
    return render_template('entrada_datos.html')

# Cálculo de liquidación de nómina
@app.route('/calcular_liquidacion', methods=['POST'])
def calcular_liquidacion():
    # Captura de datos del formulario
    monthly_salary = float(request.form.get('monthly_salary', 0))
    weeks_worked = int(request.form.get('weeks_worked', 0))
    time_worked_on_holidays = float(request.form.get('time_worked_on_holidays', 0))
    overtime_day_hours = float(request.form.get('overtime_day_hours', 0))
    overtime_night_hours = float(request.form.get('overtime_night_hours', 0))
    overtime_holiday_hours = float(request.form.get('overtime_holiday_hours', 0))
    leave_days = int(request.form.get('leave_days', 0))
    sick_days = int(request.form.get('sick_days', 0))

    try:
        # Cálculo de liquidación
        liquidacion = Liquidacion(
            monthly_salary, weeks_worked, time_worked_on_holidays,
            overtime_day_hours, overtime_night_hours, overtime_holiday_hours,
            leave_days, sick_days
        )
        total_settlement, detalles = liquidacion.CalcularLiquidacion()
        return render_template('resultado.html', total=total_settlement, detalles=detalles)

    except (Validations.ZeroSalary, Validations.ZeroWeeksWorked, Validations.MoreThan8HoursWorkedOnHoliday) as e:
        # Muestra el mensaje de error específico
        return render_template('resultado.html', error=str(e))

    except Exception:
        # Error genérico
        return render_template('resultado.html', error="Ocurrió un error inesperado. Inténtelo de nuevo.")

# Mostrar usuarios
@app.route('/mostrar')
def mostrar():
    usuarios = ControladorUsuarios.MostrarUsuarios()
    return render_template('mostrar.html', usuarios=usuarios)

# Agregar nuevo usuario
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        # Creación y registro del usuario
        usuario = Usuario(cedula=cedula, nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena)
        ControladorUsuarios.InsertarUsuario(usuario)

        return render_template('agregar.html', mensaje="Usuario agregado exitosamente.")
    
    return render_template('agregar.html')

# Eliminar usuario
@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    mensaje = None

    if request.method == 'POST':
        cedula = request.form['cedula']
        
        try:
            # Eliminar usuario con cédula
            if ControladorUsuarios.EliminarCuenta(cedula, contrasena=None):
                mensaje = "Usuario eliminado exitosamente."
            else:
                mensaje = "Error al eliminar el usuario. Verifique la cédula."
        except Exception as e:
            mensaje = str(e)

    return render_template('eliminar.html', mensaje=mensaje)

# Buscar usuario por cédula
@app.route('/buscar', methods=['GET', 'POST'])
def buscar_usuario():
    usuario = None
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        usuario = ControladorUsuarios.BuscarUsuarioCedula(cedula)

    return render_template('buscar.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
