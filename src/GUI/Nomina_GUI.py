from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import sys
sys.path.append("src")
from LiquidacionNomina.Liquida_nomina import *
from LiquidacionNomina.Validations import *

class NominaCalculatorApp(App):
    def build(self):
        contenedor = BoxLayout(orientation='vertical')

        # Cambiar el color de fondo
        contenedor.canvas.before.clear()
        with contenedor.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.8, 0.9, 1, 1)  # Celeste pastel
            self.rect = Rectangle(size=contenedor.size, pos=contenedor.pos)

        contenedor.bind(size=self._update_rect, pos=self._update_rect)

        self.detalles = {}

        contenedor.add_widget(Label(text= "NominaCalculator APP", color=(0, 0, 0, 1), bold=True))
        contenedor.add_widget(Label(text="NOTA: Si deja un campo vacío, automáticamente se le asignará cero 0 ", color=(0, 0, 0, 1),font_size='14sp'))

        contenedor.add_widget(Label(text='Salario Mensual:', color=(0, 0, 0, 1)))
        self.salary_input = TextInput(multiline=False)
        contenedor.add_widget(self.salary_input)

        contenedor.add_widget(Label(text='Semanas Trabajadas:', color=(0, 0, 0, 1)))
        self.weeks_input = TextInput(multiline=False)
        contenedor.add_widget(self.weeks_input)

        contenedor.add_widget(Label(text='Tiempo Trabajado en Festivos:', color=(0, 0, 0, 1)))
        self.holiday_time_input = TextInput(multiline=False)
        contenedor.add_widget(self.holiday_time_input)

        contenedor.add_widget(Label(text='Horas Extras Diurnas:', color=(0, 0, 0, 1)))
        self.overtime_day_input = TextInput(multiline=False)
        contenedor.add_widget(self.overtime_day_input)

        contenedor.add_widget(Label(text='Horas Extras Nocturnas:', color=(0, 0, 0, 1)))
        self.overtime_night_input = TextInput(multiline=False)
        contenedor.add_widget(self.overtime_night_input)

        contenedor.add_widget(Label(text='Horas Extras Festivos:', color=(0, 0, 0, 1)))
        self.overtime_holiday_input = TextInput(multiline=False)
        contenedor.add_widget(self.overtime_holiday_input)

        contenedor.add_widget(Label(text='Días de licencia:', color=(0, 0, 0, 1)))
        self.leave_days_input = TextInput(multiline=False)
        contenedor.add_widget(self.leave_days_input)

        contenedor.add_widget(Label(text='Días de incapacidad:', color=(0, 0, 0, 1)))
        self.sick_day_input = TextInput(multiline=False)
        contenedor.add_widget(self.sick_day_input)

        contenedor.add_widget(Label(text=""))

        self.result_label = Label(text='', color=(0, 0, 0, 1), bold=True,font_size='17sp') 
        contenedor.add_widget(self.result_label)

        # Botón personalizado
        calculate_button = Button(text='Calcular Nómina', size_hint=(8, None), size=(100, 70),
                                  background_color=(0.2, 0.6, 0.7, 1), color=(1, 1, 1, 1), bold=True,font_size='25sp')
        calculate_button.bind(on_press=self.calculate_nomi)
        centro_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100)
        centro_layout.add_widget(Label(size_hint_x=0.5)) 
        centro_layout.add_widget(calculate_button)
        centro_layout.add_widget(Label(size_hint_x=0.5)) 

        details_button = Button(text='Ver Detalles', size_hint=(3, None), size=(60, 70),
                                background_color=(0.2, 0.6, 0.7, 1), color=(1, 1, 1, 1), bold=True, font_size='15sp')
        details_button.bind(on_press=self.obtener_detalles)
        centro_layout.add_widget(details_button)

        clear_button = Button(text='Limpiar', size_hint=(3,None), size=(20, 70), background_color=(0.2, 0.6, 0.7, 1), color=(1, 1, 1, 1), bold=True)
        clear_button.bind(on_press=self.clear_labels)
        centro_layout.add_widget(clear_button)
        
        contenedor.add_widget(centro_layout)
    
        return contenedor

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def calculate_nomi(self, sender):
        try:
            monthly_salary = (self.salary_input.text) if self.salary_input.text else 0
            weeks_worked = (self.weeks_input.text) if self.weeks_input.text else 0
            time_worked_on_holidays = (self.holiday_time_input.text) if self.holiday_time_input.text else 0
            overtime_day_hours = (self.overtime_day_input.text) if self.overtime_day_input.text else 0
            overtime_night_hours = (self.overtime_night_input.text) if self.overtime_night_input.text else 0
            overtime_holiday_hours = (self.overtime_holiday_input.text) if self.overtime_holiday_input.text else 0
            leave_days = (self.leave_days_input.text) if self.leave_days_input.text else 0
            sick_days = (self.sick_day_input.text) if self.sick_day_input.text else 0
            
            liquidacion = Liquidacion(monthly_salary, weeks_worked, time_worked_on_holidays,
                                   overtime_day_hours, overtime_night_hours,
                                   overtime_holiday_hours, leave_days, sick_days)

            # Calcular liquidación
            total_payment, self.detalles = liquidacion.CalcularLiquidacion()
            self.result_label.text = f"Total Liquidación de Nomina: ${total_payment:,}".replace(',', '.')

        except (NegativeValue, InvalidValue, MoreThan8HoursWorkedOnHoliday, 
                NotAnIntegerValue, CommaSeparator, ZeroWeeksWorked, ZeroSalary) as error:
            self.mostrar_error(str(error))

        except ValueError :
            text_error = "El valor ingresado no tiene un formato correcto.\nIngrese solo números y use punto como separador decimal"
            self.mostrar_error(text_error)

    def mostrar_error(self, mensaje_error):
        contenedor1 = BoxLayout(orientation='vertical')

        mensaje = Label(text=mensaje_error, color=(1, 1, 1, 1), halign="center", valign="middle")
        mensaje.text_size = (500, None) 
        mensaje.bind(size=mensaje.setter('text_size'))  # Ajusta el tamaño del texto automáticamente

        contenedor1.add_widget(mensaje)

        cerrar = Button(text="Close (X)", size=(300, 50), size_hint_y=None, height=30, background_color=(1, 0.5, 0.4, 1), color=(1, 1, 1, 1), bold=True)
        contenedor1.add_widget(cerrar)

        ventana = Popup(title="PRECAUCIÓN !!", content=contenedor1, size_hint=(0.9, 0.5))
        cerrar.bind(on_press=ventana.dismiss)
        ventana.open()

        return ventana
    
    def ver_detalles(self, instance):
        # Aquí creamos el popup que muestra los detalles
        detalles_texto = self.obtener_detalles()

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=detalles_texto))
        cerrar_button = Button(text='Cerrar', size_hint_y=None, height=50)
        content.add_widget(cerrar_button)

        popup = Popup(title='Detalles de la Liquidación', content=content, size_hint=(0.8, 0.8))
        cerrar_button.bind(on_press=popup.dismiss)
        popup.open()

    def obtener_detalles(self, instance):
        if self.detalles:  # Verifica si hay detalles
            details_text = "\n".join(f"{key}: {value:.1f}" for key, value in self.detalles.items() if value > 0)
            
            # Crea el contenido del Popup
            content = BoxLayout(orientation='vertical')
            details_label = Label(text=details_text)
            close_button = Button(text="Close (X)", size=(300, 50), size_hint_y=None, height=30, background_color=(1, 0.5, 0.4, 1), color=(1, 1, 1, 1), bold=True)
            close_button.bind(on_press=lambda x: popup.dismiss())  # Cierra el Popup al hacer clic

            # Agrega el label y el botón al contenido
            content.add_widget(details_label)
            content.add_widget(close_button)

            # Crea y abre el Popup
            popup = Popup(title='Detalles de la Liquidación', content=content, size_hint=(0.9, 0.9))
            popup.open()
        else:
            self.mostrar_error("Primero debes llenar los espacios con tus datos y calcular la nómina para así poder ver los detalles.")
    
    def clear_labels(self, instance):
        self.result_label.text = ""
        self.salary_input.text = ""
        self.weeks_input.text = ""
        self.holiday_time_input.text = ""
        self.overtime_day_input.text = ""
        self.overtime_night_input.text = ""
        self.overtime_holiday_input.text = ""
        self.leave_days_input.text = ""
        self.sick_day_input.text = ""



if __name__ == '__main__':
    NominaCalculatorApp().run()
