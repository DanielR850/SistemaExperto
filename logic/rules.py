# logic/rules.py

def clasificar_imc(imc, edad):
    if edad <= 17:
        if imc < 18.5:
            return "Delgadez"
        elif 18.5 <= imc < 25:
            return "Normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    elif 18 <= edad <= 59:
        if imc < 18.5:
            return "Delgadez"
        elif 18.5 <= imc < 25:
            return "Normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    else:
        if imc < 23:
            return "Delgadez"
        elif 23 <= imc < 28:
            return "Normal"
        elif 28 <= imc < 32:
            return "Sobrepeso"
        else:
            return "Obesidad"

def generar_recomendacion(clasificacion, fuma, ejercicio, antecedentes, fue_al_medico,
                           duerme_bien, come_verduras, es_sedentario, duerme_mal, estresado):
    recomendaciones = []

    if clasificacion == "Obesidad":
        recomendaciones.append("Tiene obesidad. Se recomienda acudir al médico.")
        recomendaciones.append("Inicie un plan alimenticio con nutricionista.")
        recomendaciones.append("Realice actividad física de bajo impacto.")
        recomendaciones.append("Evite alimentos ultraprocesados.")
        if fuma:
            recomendaciones.append("Fumar agrava el riesgo cardiovascular. Se recomienda dejar de fumar.")
        if antecedentes:
            recomendaciones.append("Antecedentes familiares incrementan el riesgo. Evalúe su salud regularmente.")
        if not fue_al_medico:
            recomendaciones.append("Debe realizarse un chequeo médico completo.")

    elif clasificacion == "Sobrepeso":
        recomendaciones.append("Tiene sobrepeso. Tome medidas preventivas.")
        if not ejercicio:
            recomendaciones.append("Realice ejercicio al menos 3 veces por semana.")
        if antecedentes:
            recomendaciones.append("Vigile su presión y niveles de glucosa.")
        if es_sedentario:
            recomendaciones.append("Evite pasar muchas horas sentado. Pausas activas ayudan.")
        recomendaciones.append("Reduzca el consumo de azúcares y grasas saturadas.")

    elif clasificacion == "Normal":
        recomendaciones.append("Buen IMC. Mantenga su estilo de vida saludable.")
        if not duerme_bien:
            recomendaciones.append("Mejore su higiene del sueño: duerma entre 7 y 9 horas.")
        if not come_verduras:
            recomendaciones.append("Incluya frutas y verduras en su alimentación diaria.")
        if fuma:
            recomendaciones.append("Evite fumar para conservar su buen estado de salud.")
        if not ejercicio:
            recomendaciones.append("Haga al menos caminatas diarias de 30 minutos.")

    elif clasificacion == "Delgadez":
        recomendaciones.append("Tiene delgadez. Puede haber riesgo nutricional.")
        recomendaciones.append("Considere realizar 5 comidas saludables al día.")
        if antecedentes:
            recomendaciones.append("Con antecedentes, es importante realizar chequeo médico.")
        if duerme_mal:
            recomendaciones.append("El mal descanso puede afectar su apetito y metabolismo.")
        recomendaciones.append("Evalúe posibles signos de anemia o deficiencias.")

    if estresado:
        recomendaciones.append("Reduzca su nivel de estrés. Técnicas como respiración y pausas ayudan.")

    return "\n- " + "\n- ".join(recomendaciones) if recomendaciones else "Evaluación completada."
