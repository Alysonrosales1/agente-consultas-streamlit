#######################
# Agente Basico De IA #
# Herramientas        #
#######################

# Importacion para el manejo de sistema
import os
import requests

class IntermediateTools:

    def __init__(self):
        pass

    # Herramienta para consultar el tipo de cambio
    def consultar_tipo_cambio_api(self, moneda: str):
        print(f"Herramienta consultar_tipo_cambio_api llamada con moneda: {moneda}")

        if not moneda:
            return "Error: Se requiere el código de la moneda para obtener el tipo de cambio."

        # URL del servicio para obtener el tipo de cambio según la moneda:
        url = (
            f"https://open.er-api.com/v6/latest/{moneda.upper()}"
        )

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
            return response.json()  # Intentar decodificar la respuesta como JSON
        except Exception as e:
            print(f"Error al obtener_tipo_cambio_api: {moneda}. Error: {e}")
            return f"ERROR: No se pudo obtener el tipo de cambio para la moneda: {moneda}" 