import requests
from bs4 import BeautifulSoup
from ..decorators.decorators import medir_tiempo


base_url = "https://listado.mercadolibre.com.ec/computacion-notebooks"



def obtener_datos_productos(url):
    try:
        response = requests.get(url)
        # Verifica si el estado de respuesta es 200 (OK)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            productos = []
            items = soup.select(".ui-search-result__content-wrapper")

            for item in items:
                name_element = item.select_one(".ui-search-item__title")
                price_element = item.select_one(".andes-money-amount__fraction")

                if name_element and price_element:
                    name = name_element.get_text(strip=True)
                    price = price_element.get_text(strip=True)
                    productos.append((name, price))

            return productos
        else:
            print(f"Error HTTP {response.status_code} al obtener datos de la URL {url}")
            return []
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud a la URL {url}: {e}")
        return []
    except Exception as e:
        print(f"Error al procesar el contenido de la URL {url}: {e}")
        return []




