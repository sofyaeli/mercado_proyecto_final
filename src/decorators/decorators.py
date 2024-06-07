import time
import logging
def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        resultado = func(*args, **kwargs)
        end = time.time()
        print(f"Tiempo de ejecucion {func.__name__}: {end - start:.4f} segundos")
        return resultado
    return wrapper

def logit(func):
    """Decorador para registrar la ejecución de una función."""
    def wrapper(*args, **kwargs):
        logging.info(f"Running {func.__name__}")  
        result = func(*args, **kwargs)  
        logging.info(f"Completed {func.__name__}")  
        return result  
    return wrapper  