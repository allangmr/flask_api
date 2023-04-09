# Valida el nombre (si es un texto sin espacios en blanco de entre 1 y 30 caracteres).
def validate_course_name(name: str) -> bool:
    name = name.strip()
    return (len(name) > 0 and len(name) <= 50)

