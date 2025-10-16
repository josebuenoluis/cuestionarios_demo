import PyPDF2
import re
import time
import json
from openai import OpenAI
import os


API_KEY = os.getenv('OPENAI_API_KEY') 
client = OpenAI(api_key=API_KEY)

def extraer_texto_pdf_directo(archivo_pdf):
    """Extrae texto directamente de un objeto UploadedFile"""
    texto_completo = ""
    try:
        lector_pdf = PyPDF2.PdfReader(archivo_pdf)
        for pagina in lector_pdf.pages:
            texto_completo += pagina.extract_text()
    except Exception as e:
        raise Exception(f"Error al leer el PDF: {str(e)}")
    return texto_completo

def dividir_texto_en_secciones(texto, num_secciones=10):
    """
    Divide el texto en secciones aproximadamente iguales.
    """
    # Dividir el texto en oraciones usando expresiones regulares
    oraciones = re.split(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$', texto)

    # Filtrar oraciones vacías
    oraciones = [oracion.strip() for oracion in oraciones if oracion.strip()]

    # Calcular el número de oraciones por sección
    oraciones_por_seccion = max(1, len(oraciones) // num_secciones)

    # Crear las secciones
    secciones = []
    for i in range(0, len(oraciones), oraciones_por_seccion):
        seccion = " ".join(oraciones[i:i + oraciones_por_seccion])
        secciones.append(seccion)

    return secciones

def optimizar_texto(texto, max_tokens=800):
    """
    Optimiza el texto para reducir tokens manteniendo la información más relevante.
    """
    # Dividir el texto en oraciones usando expresiones regulares
    oraciones = re.split(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$', texto)

    # Filtrar oraciones vacías
    oraciones = [oracion.strip() for oracion in oraciones if oracion.strip()]

    # Eliminar oraciones duplicadas o muy similares
    oraciones_unicas = []
    for oracion in oraciones:
        # Normalizar la oración (eliminar espacios extra, convertir a minúsculas)
        oracion_norm = re.sub(r'\s+', ' ', oracion).strip().lower()

        # Verificar si una oración similar ya está en la lista
        es_duplicada = False
        for oracion_existente in oraciones_unicas:
            oracion_existente_norm = re.sub(r'\s+', ' ', oracion_existente).strip().lower()
            # Si hay más de 80% de similitud, considerar como duplicada
            if len(oracion_norm) > 0 and len(oracion_existente_norm) > 0:
                # Calcular similitud basada en caracteres comunes
                chars_comunes = sum(1 for c in oracion_norm if c in oracion_existente_norm)
                similitud = chars_comunes / max(len(oracion_norm), len(oracion_existente_norm))
                if similitud > 0.8:
                    es_duplicada = True
                    break

        if not es_duplicada and len(oracion.strip()) > 0:
            oraciones_unicas.append(oracion)

    # Estimar tokens (aproximadamente 1.3 tokens por palabra)
    palabras_por_oracion = [len(oracion.split()) for oracion in oraciones_unicas]
    tokens_estimados = [int(palabras * 1.3) for palabras in palabras_por_oracion]

    # Seleccionar oraciones hasta alcanzar el límite de tokens
    texto_optimizado = ""
    tokens_acumulados = 0

    # Priorizar las primeras oraciones (introducción) y las últimas (conclusiones)
    num_oraciones = len(oraciones_unicas)
    indices_prioritarios = list(range(min(5, num_oraciones))) + list(range(max(0, num_oraciones-5), num_oraciones))
    indices_restantes = list(range(5, max(5, num_oraciones-5)))

    # Ordenar los índices para procesar primero los prioritarios
    indices_ordenados = indices_prioritarios + indices_restantes

    for idx in indices_ordenados:
        if idx < len(oraciones_unicas):
            if tokens_acumulados + tokens_estimados[idx] <= max_tokens:
                texto_optimizado += oraciones_unicas[idx] + " "
                tokens_acumulados += tokens_estimados[idx]
            else:
                # Si ya no caben más oraciones completas, parar
                break

    return texto_optimizado.strip()

def contar_tokens_aproximados(texto):
    """
    Estima el número de tokens en un texto.
    """
    # Aproximación: 1 token ≈ 4 caracteres en inglés o 1.3 tokens por palabra
    palabras = len(texto.split())
    return int(palabras * 1.3)

def limpiar_pregunta(texto_pregunta):
    """
    Limpia el texto de la pregunta eliminando frases como "según el texto" y haciendo
    que suene más natural.
    """
    # Patrones a eliminar
    patrones = [
        r'\s+según\s+el\s+texto\s*[.?]?',
        r'\s+de\s+acuerdo\s+al\s+texto\s*[.?]?',
        r'\s+en\s+el\s+texto\s*[.?]?',
        r'\s+mencionado\s+en\s+el\s+texto\s*[.?]?',
        r'\s+como\s+se\s+menciona\s+en\s+el\s+texto\s*[.?]?',
        r'\s+que\s+aparece\s+en\s+el\s+texto\s*[.?]?'
    ]

    # Aplicar los patrones
    texto_limpio = texto_pregunta
    for patron in patrones:
        texto_limpio = re.sub(patron, '?', texto_limpio, flags=re.IGNORECASE)

    # Asegurarse de que la pregunta termine con signo de interrogación
    if not texto_limpio.endswith('?'):
        texto_limpio = texto_limpio.rstrip('.') + '?'

    return texto_limpio

def generar_cuestionario_json_por_seccion(texto, num_preguntas=8, max_tokens_salida=800, n_respuestas=4):
    """
    Genera un cuestionario en formato JSON basado en una sección de texto usando GPT-3.5-Turbo.
    Versión mejorada para generar preguntas más naturales y directas para cualquier tipo de PDF.
    """
    try:
        # Crear etiquetas para las opciones según el número de respuestas
        etiquetas_opciones = [chr(97 + i) + ")" for i in range(n_respuestas)]
        ejemplo_opciones = "\n".join([f"{etiquetas_opciones[i]} Opción {chr(65 + i)}." for i in range(n_respuestas)])
        
        # Crear el prompt para la API con instrucciones más específicas y genéricas
        prompt = f"""
        Analiza el siguiente texto extraído de un PDF y genera un cuestionario educativo con {num_preguntas} preguntas.

        INSTRUCCIONES IMPORTANTES:
        1. Identifica los conceptos clave, definiciones, hechos importantes y relaciones en el texto.
        2. Formula preguntas directas y claras que evalúen la comprensión de estos conceptos.
        3. Cada pregunta debe ser autocontenida y no hacer referencia al "texto" o "documento".
        4. Cada pregunta debe tener {n_respuestas} opciones de respuesta con una sola respuesta correcta.
        5. Las opciones deben ser breves y claras, etiquetadas como {', '.join(etiquetas_opciones)}.
        6. Ignora elementos no informativos como encabezados, pies de página, números de página, etc.
        7. Si el texto contiene temas técnicos, asegúrate de que las preguntas sean precisas y utilicen la terminología correcta.

        Ejemplo del formato de pregunta deseado:
        "¿Qué tipo de prueba evalúa el funcionamiento de un módulo específico de una aplicación?"
        {ejemplo_opciones}
        Respuesta correcta: {etiquetas_opciones[2]}

        Devuelve el resultado en formato JSON con la siguiente estructura:
        [
            {{
                "pregunta": "¿Pregunta directa?",
                "opciones": [{', '.join([f'"{etiqueta} Opción"' for etiqueta in etiquetas_opciones])}],
                "respuesta_correcta": 0  // Índice (0-{n_respuestas-1}) de la opción correcta en el array
            }},
            // Más preguntas...
        ]

        Asegúrate de que el JSON sea válido y que cada pregunta tenga exactamente {n_respuestas} opciones.

        Texto: {texto}
        """

        # Realizar la consulta a la API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en educación que crea cuestionarios de alta calidad sobre cualquier tema. Tus preguntas son claras, precisas y evalúan la comprensión de conceptos clave sin hacer referencia al texto fuente."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens_salida,
            temperature=0.7
        )

        # Extraer y devolver el cuestionario generado
        cuestionario_json_texto = response.choices[0].message.content

        # Extraer solo el JSON de la respuesta (eliminar texto adicional si existe)
        json_match = re.search(r'\[.*\]', cuestionario_json_texto, re.DOTALL)
        if json_match:
            cuestionario_json_texto = json_match.group(0)

        # Convertir el texto JSON a una lista de Python
        cuestionario_json = json.loads(cuestionario_json_texto)

        # Validar que cada pregunta tenga exactamente n_respuestas opciones
        for pregunta in cuestionario_json:
            if len(pregunta["opciones"]) != n_respuestas:
                # Ajustar el número de opciones si es necesario
                if len(pregunta["opciones"]) > n_respuestas:
                    # Recortar opciones extras
                    pregunta["opciones"] = pregunta["opciones"][:n_respuestas]
                else:
                    # Añadir opciones faltantes
                    while len(pregunta["opciones"]) < n_respuestas:
                        nueva_opcion = f"{etiquetas_opciones[len(pregunta['opciones'])]} Opción adicional."
                        pregunta["opciones"].append(nueva_opcion)
            
            # Asegurarse de que respuesta_correcta esté dentro del rango válido
            if pregunta["respuesta_correcta"] >= n_respuestas:
                pregunta["respuesta_correcta"] = n_respuestas - 1

        # Limpiar y mejorar las preguntas para hacerlas más naturales
        for pregunta in cuestionario_json:
            # Limpiar la pregunta de frases como "según el texto"
            pregunta["pregunta"] = limpiar_pregunta(pregunta["pregunta"])

            # Hacer las opciones más naturales (eliminar patrones formales)
            for i, opcion in enumerate(pregunta["opciones"]):
                # Eliminar frases como "según el texto" de las opciones también
                pregunta["opciones"][i] = re.sub(r'\s+según\s+el\s+texto\s*[.?]?', '', opcion, flags=re.IGNORECASE)

        # Calcular tokens utilizados
        tokens_entrada = contar_tokens_aproximados(prompt)
        tokens_salida = contar_tokens_aproximados(cuestionario_json_texto)

        print(f"Tokens de entrada: ~{tokens_entrada}")
        print(f"Tokens de salida: ~{tokens_salida}")
        print(f"Costo estimado: ${(tokens_entrada/1000*0.0015) + (tokens_salida/1000*0.002):.6f}")
        print(f"Preguntas generadas: {len(cuestionario_json)}")
        guardar_cuestionario_json(cuestionario_json,'cuestionario.json')
        return cuestionario_json

    except Exception as e:
        print(f"Error al generar el cuestionario JSON: {str(e)}")
        if 'response' in locals():
            print(f"Respuesta recibida: {response.choices[0].message.content}")
        return []

def guardar_cuestionario_json(cuestionario_json, nombre_archivo):
    """
    Guarda el cuestionario generado en un archivo JSON.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump({"cuestionario": cuestionario_json}, archivo, ensure_ascii=False, indent=2)
        print(f"Cuestionario JSON guardado en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar el cuestionario JSON: {str(e)}")

def procesar_pdf_y_generar_cuestionario_json(texto_completo, total_preguntas=10, max_tokens_entrada=800, max_tokens_salida=800,
                                             n_respuestas=4):
    """
    Procesa un PDF grande y genera un cuestionario en formato JSON con muchas preguntas,
    dividiendo el proceso en secciones para optimizar costos.
    Versión mejorada para generar preguntas más naturales y directas.
    """
    if not texto_completo:
        return []

    # Calcular el número de secciones necesarias
    preguntas_por_seccion = 10  # Ajustado para generar todas las preguntas en una sección si son 10 o menos
    num_secciones = (total_preguntas + preguntas_por_seccion - 1) // preguntas_por_seccion

    # Dividir el texto en secciones
    print(f"Dividiendo el texto en {num_secciones} secciones...")
    secciones = dividir_texto_en_secciones(texto_completo, num_secciones)

    # Lista para almacenar todas las preguntas
    todas_las_preguntas = []
    costo_total = 0
    preguntas_generadas = 0

    # Procesar cada sección
    i = 0
    while preguntas_generadas < total_preguntas and i < len(secciones):
        seccion = secciones[i]
        print(f"\nProcesando sección {i+1}/{len(secciones)}...")

        # Optimizar el texto de la sección
        texto_optimizado = optimizar_texto(seccion, max_tokens_entrada)

        # Calcular cuántas preguntas generar en esta sección
        preguntas_restantes = total_preguntas - preguntas_generadas
        preguntas_a_generar = min(preguntas_por_seccion, preguntas_restantes)

        # Generar cuestionario para esta sección
        print(f"Generando {preguntas_a_generar} preguntas para la sección {i+1}...")
        preguntas_seccion = generar_cuestionario_json_por_seccion(
            texto_optimizado,
            num_preguntas=preguntas_a_generar,
            max_tokens_salida=max_tokens_salida,
            n_respuestas=n_respuestas
        )

        # Si generamos menos preguntas de las esperadas, intentar de nuevo con parámetros diferentes
        if len(preguntas_seccion) < preguntas_a_generar:
            preguntas_faltantes = preguntas_a_generar - len(preguntas_seccion)
            print(f"Se generaron solo {len(preguntas_seccion)} de {preguntas_a_generar} preguntas. Generando {preguntas_faltantes} preguntas adicionales...")

            # Intentar con un prompt ligeramente diferente o más tokens
            preguntas_adicionales = generar_cuestionario_json_por_seccion(
                texto_optimizado,
                num_preguntas=preguntas_faltantes,
                max_tokens_salida=max_tokens_salida + 200,  # Aumentar tokens para el reintento
                n_respuestas=n_respuestas
            )

            preguntas_seccion.extend(preguntas_adicionales)
            print(f"Total de preguntas generadas para esta sección después del reintento: {len(preguntas_seccion)}")

        # Agregar las preguntas a la lista completa
        todas_las_preguntas.extend(preguntas_seccion)

        # Actualizar contador de preguntas
        preguntas_generadas += len(preguntas_seccion)

        # Calcular costo de esta sección
        tokens_entrada = contar_tokens_aproximados(texto_optimizado)
        tokens_salida = contar_tokens_aproximados(json.dumps(preguntas_seccion))
        costo_seccion = (tokens_entrada/1000*0.0015) + (tokens_salida/1000*0.002)
        costo_total += costo_seccion

        print(f"Costo de la sección {i+1}: ${costo_seccion:.6f}")
        print(f"Preguntas generadas hasta ahora: {preguntas_generadas}/{total_preguntas}")

        # Incrementar el contador de secciones
        i += 1

        # Si hemos procesado todas las secciones pero aún necesitamos más preguntas,
        # volvemos a procesar algunas secciones con diferentes parámetros
        if i >= len(secciones) and preguntas_generadas < total_preguntas:
            print("\nNo se generaron suficientes preguntas. Procesando secciones adicionales...")
            # Reiniciar el contador para procesar secciones adicionales
            i = 0
            # Aumentar el número de preguntas por sección para las iteraciones adicionales
            preguntas_por_seccion += 2

        # Pequeña pausa para evitar límites de rate en la API
        time.sleep(1)

    print(f"\nCosto total del cuestionario: ${costo_total:.6f}")
    print(f"Costo promedio por pregunta: ${costo_total/preguntas_generadas:.6f}")
    # guardar_cuestionario_json(todas_las_preguntas,"cuestionario.json")
    return todas_las_preguntas

# Función para generar un cuestionario a partir de un texto
def generar_cuestionario(texto_pdf, num_preguntas=10, n_respuestas=4):
    """
    Genera un cuestionario a partir del texto de un PDF.

    Args:
        texto_pdf (str): Texto extraído del PDF.
        num_preguntas (int): Número de preguntas a generar.
        n_respuestas (int): Número de opciones de respuesta por pregunta.

    Returns:
        dict: Cuestionario en formato JSON.
    """
    # Generar las preguntas
    preguntas = procesar_pdf_y_generar_cuestionario_json(
        texto_pdf,
        total_preguntas=num_preguntas,
        max_tokens_entrada=800,
        max_tokens_salida=800,
        n_respuestas=n_respuestas
    )

    # Formatear el resultado como un diccionario con la clave "cuestionario"
    return {"cuestionario": preguntas}

# Función para extraer texto de un archivo PDF
def extraer_texto_pdf(ruta_pdf):
    """
    Extrae texto de un archivo PDF.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.

    Returns:
        str: Texto extraído del PDF.
    """
    texto_completo = ""
    try:
        with open(ruta_pdf, 'rb') as archivo:
            lector_pdf = PyPDF2.PdfReader(archivo)
            for pagina in lector_pdf.pages:
                texto_completo += pagina.extract_text()
    except Exception as e:
        print(f"Error al leer el PDF: {str(e)}")
    return texto_completo

# Ejemplo de uso
def generar_cuestionario_desde_pdf(ruta_pdf, num_preguntas=10, n_respuestas=4, nombre_archivo_salida="cuestionario.json"):
    """
    Genera un cuestionario a partir de un archivo PDF y lo guarda en un archivo JSON.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.
        num_preguntas (int): Número de preguntas a generar.
        n_respuestas (int): Número de opciones de respuesta por pregunta.
        nombre_archivo_salida (str): Nombre del archivo JSON de salida.
    """
    # Extraer texto del PDF
    print(f"Extrayendo texto de {ruta_pdf}...")
    texto_pdf = extraer_texto_pdf(ruta_pdf)

    if not texto_pdf:
        print("No se pudo extraer texto del PDF.")
        return

    # Generar cuestionario
    print(f"Generando cuestionario con {num_preguntas} preguntas y {n_respuestas} opciones por pregunta...")
    cuestionario = generar_cuestionario(texto_pdf, num_preguntas, n_respuestas)

    # Guardar cuestionario en archivo JSON
    guardar_cuestionario_json(cuestionario["cuestionario"], nombre_archivo_salida)

    print(f"\nCuestionario generado y guardado en {nombre_archivo_salida}")
    print(f"Total de preguntas generadas: {len(cuestionario['cuestionario'])}")