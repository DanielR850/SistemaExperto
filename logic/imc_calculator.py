# logic/imc_calculator.py

def calcular_imc(peso, altura):
    """
    Calcula el Índice de Masa Corporal (IMC).
    
    Fórmula:
        IMC = peso (kg) / (altura (m))^2
    
    Args:
        peso (float): Peso en kilogramos
        altura (float): Altura en metros
    
    Returns:
        float: Valor del IMC redondeado a dos decimales
    """
    if altura <= 0:
        raise ValueError("La altura debe ser mayor que cero.")
    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")
    
    imc = peso / (altura ** 2)
    return round(imc, 2)
