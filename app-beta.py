import sys
sys.path.append("src")
sys.path.append(".")
from flask import Flask, render_template, request, redirect, url_for
from LiquidacionNomina.Liquida_nomina import Liquidacion
from controller.UserController import ControladorUsuarios  # Asegúrate de que esta ruta sea correcta
from model.Usuario import Usuario

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')
@app.route('/basededatos')
def basededatos():
    return render_template('opciones_basededatos.html')


# Ruta para la función de búsqueda en la base de datos
@app.route('/usuario', methods=['POST'])
def buscar_usuario():
    cedula = request.form.get('cedula')
    usuario = ControladorUsuarios.BuscarUsuarioCedula(cedula)
    if usuario:
        return render_template('resultado_busqueda.html', usuario=usuario)
    return "Usuario no encontrado."


# Ruta para mostrar todos los usuarios
@app.route('/mostrar')
def mostrar():
    usuarios = ControladorUsuarios.MostrarUsuarios()
    return render_template('mostrar.html', usuarios=usuarios)


# Ruta para agregar un nuevo usuario
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        
        nuevo_usuario = Usuario(cedula, nombre, apellido, correo, contrasena)
        ControladorUsuarios.InsertarUsuario(nuevo_usuario)
        return redirect(url_for('mostrar'))
    return render_template('agregar_usuario.html')  # Muestra el formulario para agregar un usuario


# Ruta para eliminar un usuario
@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        contrasena = request.form.get('contrasena')
        if ControladorUsuarios.EliminarCuenta(cedula, contrasena):
            return "Cuenta eliminada con éxito."
        return "No se pudo eliminar la cuenta."
    return render_template('eliminar_usuario.html')  # Muestra el formulario para eliminar un usuario


# Ruta para la página de entrada de datos para la liquidación de nómina
@app.route('/calcular')
def entrada_datos():
    return render_template('entrada_datos.html')


# Ruta para procesar el cálculo de liquidación de nómina
@app.route('/calcular_liquidacion', methods=['POST'])
def calcular_liquidacion():
    # Obtener los datos del formulario
    monthly_salary = float(request.form.get('monthly_salary', 0))
    weeks_worked = int(request.form.get('weeks_worked', 0))
    time_worked_on_holidays = float(request.form.get('time_worked_on_holidays', 0))
    overtime_day_hours = float(request.form.get('overtime_day_hours', 0))
    overtime_night_hours = float(request.form.get('overtime_night_hours', 0))
    overtime_holiday_hours = float(request.form.get('overtime_holiday_hours', 0))
    leave_days = int(request.form.get('leave_days', 0))
    sick_days = int(request.form.get('sick_days', 0))

    # Crear instancia de Liquidacion y calcular
    liquidacion = Liquidacion(
        monthly_salary, weeks_worked, time_worked_on_holidays,
        overtime_day_hours, overtime_night_hours, overtime_holiday_hours,
        leave_days, sick_days
    )
    total_settlement, detalles = liquidacion.CalcularLiquidacion()

    # Pasar los resultados a la plantilla de resultados
    return render_template('resultado.html', total=total_settlement, detalles=detalles)


if __name__ == '__main__':
    app.run(debug=True)
