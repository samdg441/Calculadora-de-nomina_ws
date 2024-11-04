from flask import Flask, render_template, request, redirect, url_for
from LiquidacionNomina import Liquida_nomina  # Asegúrate de que esta ruta sea correcta

app = app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')


# Ruta para la función de búsqueda en la base de datos
@app.route('/buscar')
def buscar():
    return "Aquí va la función de búsqueda en la base de datos"

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
    liquidacion = Liquida_nomina(
        monthly_salary, weeks_worked, time_worked_on_holidays,
        overtime_day_hours, overtime_night_hours, overtime_holiday_hours,
        leave_days, sick_days
    )
    total_settlement, detalles = liquidacion.CalcularLiquidacion()

    # Pasar los resultados a la plantilla de resultados
    return render_template('resultado.html', total=total_settlement, detalles=detalles)

if __name__ == '__main__':
    app.run(debug=True)

