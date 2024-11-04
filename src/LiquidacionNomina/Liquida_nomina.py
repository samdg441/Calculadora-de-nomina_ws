import sys
sys.path.append( "src" )
sys.path.append(".")
from LiquidacionNomina import Validations

class Liquidacion():
    def __init__(self,monthly_salary, weeks_worked, time_worked_on_holidays=0, overtime_day_hours=0,
                 overtime_night_hours=0, overtime_holiday_hours=0, leave_days=0, sick_days=0):
        
        self.variables = {
            'monthly_salary': [monthly_salary, True],
            'weeks_worked' :[weeks_worked, False],
            'time_worked_on_holidays':  [time_worked_on_holidays, False],
            'overtime_day_hours': [overtime_day_hours, False],
            'overtime_night_hours': [overtime_night_hours, False],
            'overtime_holiday_hours': [overtime_holiday_hours, False],
            'leave_days': [leave_days, True],
            'sick_days': [sick_days, True]
        }
    
    def Validar_salario(self):
        if self.variables['monthly_salary'][0] < 2000:
            raise Validations.ZeroSalary("VALOR INVÁLIDO: Asegúrese de que el valor en salario sea su salario mensual (número mayor de cero '0').")

    def Validar_semanas_trabajadas(self):
        if self.variables['weeks_worked'][0] == 0:
            raise Validations.ZeroWeeksWorked("VALOR INVÁLIDO: Las semanas trabajadas deben ser un número mayor o igual a 1.")

    def Validar_time_worked_on_holidays(self):
        if self.variables['time_worked_on_holidays'][0] > 8:
            raise Validations.MoreThan8HoursWorkedOnHoliday("VALOR INVÁLIDO: El tiempo festivo laborado no puede ser mayor a 8 horas.")
    
    def CalcularLiquidacion(self):
        """
        Calculates the payroll settlement for employees in Colombia.
        """
        self.variables = Validations.validate_variables(self.variables)
        
        TOTAL_DAYS_IN_MONTH = 30
        DAILY_WORKING_HOURS = 8
        MAXIMUM_SALARY_WITH_TRANSPORT_ALLOWANCE = 2600000
        TOTAL_WORK_DAYS_PER_WEEK = 6
        VALUE_PER_HOUR_WORKED_ON_HOLIDAY = 1.75
        VALUE_PER_OVERTIME_DAY_HOUR = 1.25
        VALUE_PER_OVERTIME_NIGHT_HOUR = 1.75
        VALUE_PER_OVERTIME_HOLIDAY_HOUR = 2
        PERCENTAGE_TO_DEDUCT_FOR_HEALTH = 0.04
        PERCENTAGE_TO_DEDUCT_FOR_PENSION = 0.04
        PERCENTAGE_TO_DEDUCT_FOR_SOLIDARITY_FUND = 0.01
        SALARY_TO_DEDUCT_FOR_FUND = 4000000
        PERCENTAGE_TO_DEDUCT_FOR_WITHHOLDING = 0.05
        SALARY_TO_DEDUCT_FOR_WITHHOLDING = 4300000
        PERCENTAGE_TO_DEDUCT_FOR_DISABILITY = 0.333

        self.Validar_salario()
        self.Validar_semanas_trabajadas()
        self.Validar_time_worked_on_holidays()

        days_worked = self.variables['weeks_worked'][0] * TOTAL_WORK_DAYS_PER_WEEK  # Convert weeks to days worked

        # Initial calculations
        transport_allowance = 162000 if self.variables['monthly_salary'][0] <= MAXIMUM_SALARY_WITH_TRANSPORT_ALLOWANCE else 0
        daily_salary = self.variables['monthly_salary'][0] / TOTAL_DAYS_IN_MONTH
        hourly_salary = daily_salary / DAILY_WORKING_HOURS
        
        # Calculation of additional payments
        earnings_for_holidays = self.variables['time_worked_on_holidays'][0] * hourly_salary * VALUE_PER_HOUR_WORKED_ON_HOLIDAY 
        earnings_for_overtime_day = self.variables['overtime_day_hours'][0] * hourly_salary * VALUE_PER_OVERTIME_DAY_HOUR
        earnings_for_overtime_night = self.variables['overtime_night_hours'][0] * hourly_salary * VALUE_PER_OVERTIME_NIGHT_HOUR
        earnings_for_overtime_holidays = self.variables['overtime_holiday_hours'][0] * hourly_salary * VALUE_PER_OVERTIME_HOLIDAY_HOUR

        # Total income
        total_income = (daily_salary * days_worked) + transport_allowance + earnings_for_holidays + \
                    earnings_for_overtime_day + earnings_for_overtime_night + earnings_for_overtime_holidays
            
        # Deductions
        health_deduction = total_income * PERCENTAGE_TO_DEDUCT_FOR_HEALTH
        pension_deduction = total_income * PERCENTAGE_TO_DEDUCT_FOR_PENSION
        solidarity_fund_deduction = total_income * PERCENTAGE_TO_DEDUCT_FOR_SOLIDARITY_FUND if self.variables['monthly_salary'][0] > SALARY_TO_DEDUCT_FOR_FUND else 0
        leave_payment = self.variables['leave_days'][0] * daily_salary
        withholding_tax = total_income * PERCENTAGE_TO_DEDUCT_FOR_WITHHOLDING if self.variables['monthly_salary'][0] > SALARY_TO_DEDUCT_FOR_WITHHOLDING else 0
        disability_deduction = self.variables['sick_days'][0] * daily_salary * PERCENTAGE_TO_DEDUCT_FOR_DISABILITY

        # Total amount to receive
        total_settlement = total_income - (health_deduction + pension_deduction + solidarity_fund_deduction + disability_deduction + 
                                        leave_payment + withholding_tax)
        
        detalles = {
            'Auxilio de transporte':transport_allowance,
            'Monto por laborar festivos': earnings_for_holidays,
            'Monto por extras diurnos': earnings_for_overtime_day,
            'Monto por extras nocturnos': earnings_for_overtime_night,
            'Monto por extras en festivo': earnings_for_overtime_holidays,
            'Total de ingresos': total_income,
            'Resta por salud': health_deduction,
            'Resta por pension': pension_deduction,
            'Resta de fondo_solidario': solidarity_fund_deduction,
            'Pagos por licencia': leave_payment,
            'Retención de fuente': withholding_tax,
            'Deduccion por incapacidad': disability_deduction
        }

        return (round(total_settlement, 2),detalles)
    

