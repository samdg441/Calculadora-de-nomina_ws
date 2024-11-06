# Calculadora de Nómina
## ¿Quién hizo esto?
**Autores de Calculadora de Nómina**:
- Steven Oviedo
- Valentina Morales
**Autores de la base de datos**:
- Felix Prada
- Dilan Urrego
**Autores de La Aplicación Web**:
- Samuel Gallego
- Isabella Ceballos
  
## ¿Qué es y para qué es?
Este proyecto es una aplicación que calcula el total a pagar de una empresa a un empleado (pago de nómina). Este pago corresponde a la diferencia entre los valores devengados y las deducciones de ley que aplican al salario del trabajador.
## ¿Cómo lo hago funcionar?
### Prerrequisito
Asegurese de tener ``Python`` instalado en su sistema. Ademas de también añadir `unittest` que es el encargado de correr las pruebas unitarias, así como también debe añadir `kivy`  que es el encargado de procesar la interfaz de usuario.<br>
De resto no hay otro prerrequisito.

### Ejecución
Para correr el programa por fuera del entorno de desarrollo :
1. Navegar a la carpeta: una vez que hayas clonado el archivo, abre el cmd y navega a la carpeta donde guardaste el archivo, por ejemplo:
   ```bash
   cd C:\Users\Usuario\OneDrive\Documentos\U\Sexto Semestre\Código limpio\Clean-Code-1
   ``` 
2. A continuación puedes ejecutar la consola para comprobar el funcionamiento, esto mediante las siguinetes lineas: <br>
   ```bash
   src\Console\Console.py
   python src\Console\Console.py
   ```
3. Tambien puedes ejecutar el script principal donde se encuentra la interfaz, la cual es mas amigable con el usuario: <br>
   ```bash
   src\GUI\Nomina_GUI.py
   python src\GUI\Nomina_GUI.py
   ```

## ¿Cómo está hecho?
### Arquitectura del proyecto
El proyecto está organizado en dos carpetas principales:
- **src**: Contiene el código fuente de la aplicación.
   - **Console**: Contiene el script `Console.py` para la interacción del usuario.
   - **GUI**: Contiene el script principal `Nomina_GUI.py` que desde una interfaz amigable con el ususario puede interactuar con el programa.
   - **Recursos**: Contiene una imagen que se usa como recurso para hacer la interfaz mas amigable `precaution.png` 
   - **LiquidacionNomina**: Contiene la lógica para el cálculo de la nómina `Liquida_nomina.py` y las validaciones necesarias para asegurar que las variables cumplan los estándares `Validations.py`.
  
- **Test**: Contiene pruebas unitarias para validar la funcionalidad del código `Test_liquidacion.py`.
### Organización del módulo
- `src\GUI\Nomina_GUI.py`: Contiene el script principal, el cual recopila las entradas del usuario mediante una interfaz y muestra los resultados por medio de la misma.
- `src\Console\Console.py`: Contiene el script para la interacción del usuario de manera plana. Recopilando las entradas del usuario y muestra los resultados.
- `src\LiquidacionNomina\Liquida_nomina.py`: Contiene las funciones lógicas para el cálculo de la nomina, incluida la validación de las entradas y el cálculo del pago.
### Dependencias
- `unittest`: Librería estándar de Python para pruebas unitarias.
- `kivy`: Librería de Python para el desarrollo de interfaces gráficas.
## Uso
Para ejecutar las pruebas unitarias desde la carpeta `test`, utilice el siguiente comando:
```bash
python Test/Test_liquidacion.py
```
Para ejecutar la interfaz gráfica amigable con el usuario y comprobar el funcionamiento, utilice el siguiente comando:
```bash
python src\GUI\Nomina_GUI.py
```
Para ejecutar la consola y probar el funcionamiento del programa, utilice el siguiente comando:
```bash
python src\Console\Console.py
```
