
import re
def emailvalidator(email:str)->bool:
    import re

    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    result = True if re.fullmatch(regex, email) else False
    return result
