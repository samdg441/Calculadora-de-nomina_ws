# Calculadora de Nómina - Aplicación Web

## Descripción
**Calculadora de Nómina** es una aplicación web diseñada para calcular el total a pagar de una empresa a sus empleados, considerando las deducciones legales y los valores devengados del salario. Esta herramienta facilita el manejo de nóminas en un entorno accesible, amigable y eficiente.

## Autores
- **Aplicación Web**: Samuel Gallego, Isabella Ceballos
- **Base de Datos**: Felix Prada, Dilan Urrego
- **Lógica de Cálculo**: Steven Oviedo, Valentina Morales

## Funcionalidad
La aplicación permite a las empresas calcular automáticamente el salario neto de sus empleados

## Requisitos Previos
Para configurar y ejecutar el proyecto, necesitas tener instalados los siguientes elementos:
- **Python**: Para ejecutar el backend del cálculo de nómina.
- **Flask**: Para la estructura y desarrollo de la aplicación web.
- **Unittest**: Biblioteca para pruebas unitarias.
- **Kivy**: (Opcional, si se usa para interfaces locales).
Ademas debes tener una base de datos en Neon Tech
-Para crearla debes ir a la pagina oficial de Neon Tech: https://neon.tech.
a.	Debes iniciar sesión en su sitio web, o registrarte si no tinenes una cuenta creada.
b.	Creas un nuevo proyecto.
c.	Te diriges al apartado que dice "Dashboard".
d.	En el apartado Database, selecciona la base de datos donde quieras guardar la base de datos y su información.
e.	Haz click donde dice "ConnectionString", se desplegará un menú.
f.	Selecciona la que dice "Parameters only".
-¿Qué hacer con la información?.
g.	Una vez la página te muestre los parámetros de la base de datos dírigete a la carpeta "src".
h.	Encontraras al archivo "secret_config_esample".
i.	Finalmente deberás seguir los pasos indicados en el archivo 'secret_config_esample.py' para continuar con el proceso de conexión con la base de datos.
Asegúrate de tener un entorno virtual para evitar conflictos de dependencias y mantener el entorno limpio.
## Instalación y Ejecución 
### Clonar el repositorio ```bash git clone < https://github.com/samdg441/Calculadora-de-nomina_ws/tree/main/src > 
### Instalar dependencias``` 
- Modifica el archivo de configuración settings.py en el directorio del proyecto para ajustar la conexión a la base de datos.
-Ejecuta las migraciones: 
### Acceso a la aplicación``` Abre un navegador y navega a http://127.0.0.1:5000 para acceder a la interfaz.
## Arquitectura del Proyecto
El proyecto está organizado en varias carpetas para mantener una estructura modular y clara:
-*calculadora_nómina*: Contiene los archivos de configuración del proyecto de Django.
-src: Contiene la lógica de cálculo y validación de la nómina.
-view-console: Define las vistas para manejar la interacción de los usuarios con la interfaz web.
-model: Define los modelos de base de datos.
-templates: Contiene los archivos HTML para la interfaz de usuario.
-static: Archivos CSS, JS y otros recursos estáticos.
-Test: Contiene pruebas unitarias para validar la funcionalidad de la lógica de cálculo y las vistas.






