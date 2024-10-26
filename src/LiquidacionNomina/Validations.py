import re
# Custom exceptions for specific validation error cases
class NegativeValue(Exception): 
    pass

class InvalidValue(Exception): 
    pass

class NotAnIntegerValue(Exception):
    pass

class CommaSeparator(Exception):
    pass

class MoreThan8HoursWorkedOnHoliday(Exception):
    pass

class ZeroWeeksWorked(Exception):
    pass

class ZeroSalary(Exception):
    pass

def validate_and_convert(entry, variable_name, should_be_integer=False):
    try:
        entry_str = str(entry)
        
        # Check if the entry contains a comma as a decimal separator
        if ',' in entry_str:
            raise CommaSeparator(f"ERROR: Dato inválido en {variable_name}: Use un punto (.) como separador decimal, no una coma (,)")

        # Convert to float to ensure it's numeric
        value = float(entry)

        # If it should be an integer, check that it has no decimals
        if should_be_integer and value != int(value):
            raise NotAnIntegerValue(f"ERROR: Dato inválido en {variable_name}: Se esperaba un número entero.")

        # Check if it's negative
        if value < 0:
            raise NegativeValue(f"ERROR: Dato inválido en {variable_name}: Los números no pueden ser negativos.")

        # Return the correct type (integer or float)
        return int(value) if should_be_integer else value

    except ValueError:
        raise InvalidValue(f"ERROR: Dato inválido en {variable_name}: Asegúrese de que sea un valor númerico, no negativo y sin letras o caracteres especiales.")

def validate_variables(variables):
    for variable_name in variables:
        value = validate_and_convert(variables[variable_name][0],variable_name, variables[variable_name][1])
        variables[variable_name][0] = value
        
        
    # return converted_variables
    return variables
