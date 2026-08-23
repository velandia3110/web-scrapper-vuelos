import re

from playwright.sync_api import sync_playwright

url = "https://www.latamairlines.com/co/es"
condicion = r'^COP \d{1,3}(\.\d{3})*$'

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="es-CO",
        )
        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )
        response = page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)  
        print(f"Status Code: {response.status}")
        print(f"Final URL: {page.url}")

        programas = []
        programasObtenidos = []
        if response.status == 200:
            spans = page.locator("span").all_text_contents()
            for i, nombreCarrera in enumerate(spans, start=1):
                if re.match(condicion, nombreCarrera):
                    precio = int(nombreCarrera.split(" ")[1].replace(".", ""))
                    if precio < 9000000:
                        print("  resultado    -->  " + nombreCarrera)
                        programas.append({"nombre": nombreCarrera})
                        programasObtenidos.append({"id": i, "nombre": nombreCarrera})
        else:
            print(f"Error: Código de estado {response.status}")

        browser.close()

    for programa in programas:
        print(programa)
    for programa in programasObtenidos:
        print(f"ID: {programa['id']}, Nombre: {programa['nombre']}")

except Exception as e:
    print(f"Error al realizar la solicitud: {e}")
