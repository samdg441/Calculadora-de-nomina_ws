-- Crea la tabla de usuarios
create table usuarios (
  cedula integer  NOT NULL,
  nombre text not null,
  apellido text not null,
  correo text,
  contrasena text,
  primary key (cedula)
); 