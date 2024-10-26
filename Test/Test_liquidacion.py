import unittest
import sys
sys.path.append("src")
from LiquidacionNomina import Validations
from LiquidacionNomina import Liquida_nomina
from controller.UserController import ControladorUsuarios
import psycopg2
from model.Usuario import Usuario


class LiquidationTest(unittest.TestCase):

    # Normal tests (expected cases)
    def test_basic_liquidation(self):
        liquidacion= Liquida_nomina.Liquidacion(monthly_salary=1500000, weeks_worked=24)
        result, detalles= liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 6773040.0)

    def test_complete_liquidation(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=1300000, weeks_worked=7, overtime_day_hours=13,
                                                     overtime_night_hours=3, time_worked_on_holidays=8, leave_days=7, sick_days=3)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 1653725.0) 
        
    def test_liquidation_with_overtime(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=2200000, weeks_worked=26, 
                                                     overtime_day_hours=10, overtime_night_hours=5)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 10853048.33)
    
    def test_normal_liquidation(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=3000000, weeks_worked=4, time_worked_on_holidays=8, 
                                                     overtime_day_hours=5, overtime_night_hours=3, overtime_holiday_hours=2, 
                                                     sick_days=5)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 2380750.00) 
        
    def test_regular_liquidation(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=2000000, weeks_worked=14, time_worked_on_holidays=5, 
                                                     overtime_day_hours=2, overtime_night_hours=1, overtime_holiday_hours=1, 
                                                     sick_days=3)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 5349440.0)

    def test_natural_liquidation(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=2600000, weeks_worked=4, time_worked_on_holidays=8, 
                                                     overtime_day_hours=4, overtime_night_hours=2, overtime_holiday_hours=1)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 2306823.33)

    # Extraordinary tests (boundary or unusual cases)
    def test_liquidation_with_sick_days(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=4000000, weeks_worked=20, sick_days=15)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 14054000.0)

    def test_liquidation_with_retention(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=7000000, weeks_worked=8, sick_days=1)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 9554300.0)

    def test_liquidation_without_transport(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=3000000, weeks_worked=10)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 5520000.00)
    
    def test_with_leave_days(self):
        monthly_salary = 1000000
        weeks_worked = 3
        leave_days = 6
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked, leave_days)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 741290.0)

    def test_low_salary_liquidation(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=900000, weeks_worked=2)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 480240.0)
    
    def test_one_leave_day(self):
        liquidacion = Liquida_nomina.Liquidacion(monthly_salary=1900000, weeks_worked=12, leave_days=1)
        result, detalles = liquidacion.CalcularLiquidacion()
        self.assertEqual(result, 4280906.67)

    # Error tests (error handling)
    def test_negative_salary(self):
        monthly_salary = -1000000
        weeks_worked = 20
        with self.assertRaises(Validations.NegativeValue):
            liquidacion = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked)
            liquidacion.CalcularLiquidacion()

    def test_weeks_worked_zero(self):
        monthly_salary = 2000000
        weeks_worked = 0 
        with self.assertRaises(Validations.ZeroWeeksWorked):
            liquidacion = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked)
            liquidacion.CalcularLiquidacion()

    def test_negative_daytime_overtime_hours(self):
        monthly_salary = 1300000
        weeks_worked = 4
        overtime_day_hours = -3
        with self.assertRaises(Validations.NegativeValue):
            result = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked, overtime_day_hours=overtime_day_hours)
            result.CalcularLiquidacion()

    def test_liquidation_more_than_8h_holiday(self):
        monthly_salary = 3000000
        weeks_worked = 4
        time_worked_on_holidays = 10
        overtime_day_hours = 5
        overtime_night_hours = 3
        overtime_holiday_hour = 2
        sick_days = 5
        with self.assertRaises(Validations.MoreThan8HoursWorkedOnHoliday):
            result = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked, time_worked_on_holidays, 
                                                    overtime_day_hours, overtime_night_hours, overtime_holiday_hour, 
                                                    sick_days)
            result.CalcularLiquidacion()

    def test_liquidation_negative_sick_days(self):
        monthly_salary = 3000000
        weeks_worked = 4
        time_worked_on_holidays = 6 
        overtime_day_hours = 5
        overtime_night_hours = 3 
        sick_days = -5
        with self.assertRaises(Validations.NegativeValue):
            result = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked, time_worked_on_holidays, 
                                                    overtime_day_hours, overtime_night_hours, sick_days)
            result.CalcularLiquidacion()

    def test_liquidation_non_numeric_salary(self):
        monthly_salary = "three million"
        weeks_worked = 7
        time_worked_on_holidays = 10
        overtime_day_hours = 5
        overtime_night_hours = 3
        overtime_holiday_hours = 2
        sick_days = 5
        with self.assertRaises(Validations.InvalidValue):
            result = Liquida_nomina.Liquidacion(monthly_salary, weeks_worked, time_worked_on_holidays, 
                                                    overtime_day_hours, overtime_night_hours, overtime_holiday_hours, 
                                                    sick_days)
            result.CalcularLiquidacion()

    def test_liquidation_non_numeric_overtime_hours(self):
        with self.assertRaises(Validations.InvalidValue):
            result = Liquida_nomina.Liquidacion(monthly_salary=3000000, weeks_worked=4, time_worked_on_holidays=10, 
                                                    overtime_day_hours="five", overtime_night_hours=3, overtime_holiday_hours=2, sick_days=5)
            result.CalcularLiquidacion()

    def test_liquidation_negative_holiday_time(self):
        with self.assertRaises(Validations.NegativeValue):
            result = Liquida_nomina.Liquidacion(monthly_salary=3000000, weeks_worked=4, time_worked_on_holidays=-10, 
                                                    overtime_day_hours=5, overtime_night_hours=3, overtime_holiday_hours=2, 
                                                    sick_days=5)
            result.CalcularLiquidacion()


if __name__ == '__main__':
    # unittest.main()
    unittest.main(verbosity=2, exit=False)

