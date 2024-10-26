class Usuario:
    """
    Pertenece la Capa de Reglas de Negocio (Model)

    Representa a un usuario de la Calucladora de Nómina en la aplicación
    """
    def __init__( self, cedula, nombre, apellido, correo, contrasena )  :
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena

    def esIgual( self, comparar_con ) :
        """
        Compara el objeto actual, con otra instancia de la clase Usuario
        """
        assert( self.cedula == comparar_con.cedula )
        assert( self.nombre == comparar_con.nombre )
        assert( self.apellido== comparar_con.apellido )
        assert( self.correo== comparar_con.correo )
        assert( self.contrasena == comparar_con.contrasena)


