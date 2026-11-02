#######################
# Agente Basico De IA #
# Herramientas        #
#######################

# Importacion para el manejo de sistema
import os

# Importacion para hacer llamados HTTP a las APIs externas
import requests

class BasicTools:

    def __init__(self):
        pass

    # Herramienta para consultar el tipo de cambio
    def consultar_tipo_cambio(self, moneda: str = ""):
        print(f"Herramienta consultar_tipo_cambio llamada con {moneda}")

        if moneda.upper() == "USD":
            return "El tipo de cambio es 7.80 quetzales por dólar"
        else:
            return f"No tengo información para la moneda {moneda}"

    # Herramienta para consultar el clima actual de una ciudad (Open-Meteo, gratis, sin API key)
    def consultar_clima(self, ciudad: str = ""):
        print(f"Herramienta consultar_clima llamada con {ciudad}")

        try:
            # Paso 1: convertir el nombre de la ciudad en coordenadas (geocoding)
            geo_resp = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": ciudad, "count": 1, "language": "es"},
                timeout=10
            )
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                return f"No se encontró la ciudad '{ciudad}'"

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            nombre_encontrado = geo_data["results"][0].get("name", ciudad)

            # Paso 2: consultar el clima actual con las coordenadas
            clima_resp = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current_weather": True
                },
                timeout=10
            )
            clima_data = clima_resp.json()
            actual = clima_data.get("current_weather")

            if not actual:
                return "No se pudo obtener el clima en este momento"

            temperatura = actual.get("temperature")
            viento = actual.get("windspeed")

            return (
                f"El clima actual en {nombre_encontrado} es de {temperatura}°C "
                f"con viento de {viento} km/h"
            )
        except requests.RequestException:
            return "No se pudo consultar el clima en este momento"

    # Herramienta para buscar noticias recientes (NewsData.io, requiere API key gratuita)
    def consultar_noticias(self, tema: str = ""):
        print(f"Herramienta consultar_noticias llamada con {tema}")

        api_key = os.environ.get("NEWSDATA_API_KEY")
        if not api_key:
            return "No hay una API key configurada para el servicio de noticias"

        try:
            resp = requests.get(
                "https://newsdata.io/api/1/news",
                params={
                    "apikey": api_key,
                    "q": tema,
                    "language": "es"
                },
                timeout=10
            )
            data = resp.json()
            resultados = data.get("results", [])[:5]

            if not resultados:
                return f"No se encontraron noticias sobre '{tema}'"

            titulos = [n.get("title", "Sin título") for n in resultados]
            return "Noticias encontradas:\n" + "\n".join(f"- {t}" for t in titulos)
        except requests.RequestException:
            return "No se pudo consultar noticias en este momento"

    # Herramienta para obtener la definicion de una palabra en ingles (Free Dictionary API, gratis)
    def consultar_definicion(self, palabra: str = ""):
        print(f"Herramienta consultar_definicion llamada con {palabra}")

        try:
            resp = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{palabra}",
                timeout=10
            )

            if resp.status_code != 200:
                return f"No se encontró la palabra '{palabra}'"

            data = resp.json()
            entrada = data[0]
            significados = entrada.get("meanings", [])

            if not significados:
                return f"No se encontró definición para '{palabra}'"

            primer_significado = significados[0]
            tipo = primer_significado.get("partOfSpeech", "")
            definicion = primer_significado.get("definitions", [{}])[0].get("definition", "")

            return f"{palabra} ({tipo}): {definicion}"
        except requests.RequestException:
            return "No se pudo consultar la definición en este momento"

    # Herramienta para obtener informacion general de un pais (REST Countries, gratis)
    def consultar_pais(self, pais: str = ""):
        print(f"Herramienta consultar_pais llamada con {pais}")

        try:
            resp = requests.get(
                f"https://restcountries.com/v3.1/name/{pais}",
                timeout=10
            )

            if resp.status_code != 200:
                return f"No se encontró el país '{pais}'"

            data = resp.json()[0]
            nombre = data.get("name", {}).get("common", pais)
            capital = (data.get("capital") or ["Desconocida"])[0]
            region = data.get("region", "Desconocida")
            poblacion = data.get("population", "Desconocida")
            monedas = list((data.get("currencies") or {}).keys())
            idiomas = list((data.get("languages") or {}).values())

            return (
                f"{nombre} — Capital: {capital}, Región: {region}, "
                f"Población: {poblacion}, Monedas: {', '.join(monedas) or 'N/A'}, "
                f"Idiomas: {', '.join(idiomas) or 'N/A'}"
            )
        except requests.RequestException:
            return "No se pudo consultar información del país en este momento"

    # Herramienta para obtener los feriados publicos de un pais en un anio (Nager.Date, gratis)
    def consultar_feriados(self, codigo_pais: str = "", anio: int = None):
        print(f"Herramienta consultar_feriados llamada con {codigo_pais}, {anio}")

        try:
            resp = requests.get(
                f"https://date.nager.at/api/v3/PublicHolidays/{anio}/{codigo_pais.upper()}",
                timeout=10
            )

            if resp.status_code != 200:
                return f"No se encontraron feriados para '{codigo_pais}' en {anio}"

            data = resp.json()

            if not data:
                return f"No se encontraron feriados para '{codigo_pais}' en {anio}"

            lista = [f"{f.get('date')}: {f.get('localName')}" for f in data]
            return f"Feriados de {codigo_pais.upper()} en {anio}:\n" + "\n".join(lista)
        except requests.RequestException:
            return "No se pudo consultar feriados en este momento"