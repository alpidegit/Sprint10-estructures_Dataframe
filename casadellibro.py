import scrapy
import pandas as pd

class CasadellibroSpider(scrapy.Spider):
    name = "casadellibro"
    allowed_domains = ["casadellibro.com"]
    start_urls = ["https://www.casadellibro.com/"]

    def parse(self, response):
        # Your existing code for handling cookies_popup goes here...

        # Identifico el botón de "Lo más leído" y hago clic en él
        elemento_lo_mas_leido = response.css('a[title="Ver más"]')
        if elemento_lo_mas_leido:
            yield response.follow(elemento_lo_mas_leido, callback=self.parse_mas_leidos)

    def parse_mas_leidos(self, response):
        # Creo las listas para almacenar la información de genero de los libros
        generos = ["masleidosficcion23", "masleidosnoficcion23", "comic23", "juvenil23", "infantil23"]

        # Lista para almacenar todos los datos de los libros
        Libros = []

        for gen in generos:
            # Encuentro la sección de los libros del género más leídos de la semana
            seccion_element = response.css(f'#{gen}')

            # Encuentro todos los contenedores de libros del genero dentro de la sección
            contenedores_libros = seccion_element.css("div.compact-product")

            # Itero a través de los contenedores de libros y extraigo la información
            for contenedor in contenedores_libros:
                titulo = contenedor.css(".compact-product-title::text").get().strip() 
                formato = contenedor.css(".feature::text").get().strip()
                autor = contenedor.css(".compact-product-authors::text").get().strip()
                precio = contenedor.css(".main-price::text").get().strip()

                 # :: es un selector que permite seleccionar algo de lo buscado, en este caso, el texto deelemento buscado con CSS
              
            # Agrego los datos a la lista de todos los libros
                Libros.append({
                    "Género": gen,
                    "Título": titulo,
                    "Formato": formato,
                    "Autor": autor,
                    "Precio": precio
                })

        # Creo el DataFrame con toda la información de los libros
        df_libros = pd.DataFrame(Libros)

        # Guardo el DataFrame en un archivo CSV
        df_libros.to_csv("libros_casadellibro.csv", index=False)