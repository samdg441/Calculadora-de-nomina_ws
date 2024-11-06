import sys
sys.path.append( "src" )
sys.path.append(".")
from flask import Flask, render_template, request, redirect, url_for
from LiquidacionNomina.Liquida_nomina import Liquidacion 
from controller.UserController import  ControladorUsuarios
from model.Usuario import Usuario# Asegúrate de que esta ruta sea correcta

app = app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')


# Ruta para la función de búsqueda en la base de datos
@app.route('/basededatos')
def basededatos():
    return render_template('basededatos.html')


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
# Ruta para mostrar datos
@app.route('/mostrar')
def mostrar():
    usuarios = ControladorUsuarios.MostrarUsuarios()
    return render_template('mostrar.html', usuarios=usuarios)

# Ruta para agregar datos
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        usuario = Usuario(cedula=cedula, nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena)
        ControladorUsuarios.InsertarUsuario(usuario)

        return render_template('agregar.html', mensaje="Usuario agregado exitosamente.")
    
    return render_template('agregar.html')

# Ruta para eliminar datos
@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    mensaje = None  # Mensaje que se mostrará después de intentar eliminar

    if request.method == 'POST':
        cedula = request.form['cedula']
        
        # Intentar eliminar el usuario usando ControladorUsuarios.EliminarCuenta
        try:
            if ControladorUsuarios.EliminarCuenta(cedula, contrasena=None):  # Modifica según la lógica de contraseña
                mensaje = "Usuario eliminado exitosamente."
            else:
                mensaje = "Error al eliminar el usuario. Verifique la cédula."
        except Exception as e:
            mensaje = str(e)  # Captura y muestra el mensaje de excepción

    return render_template('eliminar.html', mensaje=mensaje)

# Ruta para buscar usuario por cédula
# Ruta para buscar usuario por cédula
@app.route('/buscar', methods=['GET', 'POST'])
def buscar_usuario():
    usuario = None  # Inicializa el usuario como None
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        usuario = ControladorUsuarios.BuscarUsuarioCedula(cedula)  # Busca el usuario por cédula
    return render_template('buscar.html', usuario=usuario)



if __name__ == '__main__':
    app.run(debug=True)

