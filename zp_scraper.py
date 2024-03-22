from bs4 import BeautifulSoup
import cloudscraper
from util import output_posts_info, Scraper, bcolors

###################################
# ZONA PROP
###################################

# busqueda "oficina vicente lopez" se traduce a "https://www.zonaprop.com.ar/alquiler-q-oficina-vicente-lopez.html"
# (no importa que categoría estaba seleccionada)
# tipo: alquiler, venta, etc
# por ende la estructura de la query es: "/{categoria a menos que la query la reemplace?}{tipo}-q-{palabras de busqueda separadas por - y sin tildes}"
# parece que el orden de los elementos de la query no importa :
# https://www.zonaprop.com.ar/alquiler-pagina-2-q-oficina-pilar.html
# ==
# https://www.zonaprop.com.ar/alquiler-q-oficina-pilar-pagina-2.html
# (cuando se hace la busqueda en el navegador, despues la pagina lo parsea como el primer ejemplo)
# 20 resultados máx por página

zp_attributes = {
    "price": {"data-qa": "POSTING_CARD_PRICE"},
    "address": {"class": "sc-ge2uzh-0 eWOwnE postingAddress"},
    "location": {"data-qa": "POSTING_CARD_LOCATION"},
    "expenses": {"data-qa": "expensas"},
    "features": {"data-qa": "POSTING_CARD_FEATURES"},
}

zp_scraper = Scraper(
    "https://www.zonaprop.com.ar/alquiler-q-oficina-vicente-lopez.html",
    "h1",
    {"class": "sc-1oqs0ed-0 cvTPma"},
)

num_pages = zp_scraper.get_num_pages()

post_counter = 0

for page in range(1, num_pages + 1):
    print(
        bcolors.OKBLUE
        + "---------- "
        + "PAGE "
        + str(page)
        + " ----------"
        + bcolors.ENDC
    )
    posts = zp_scraper.scrap_posts(
        f"https://www.zonaprop.com.ar/alquiler-q-oficina-vicente-lopez-pagina-{page}.html",
        {"data-posting-type": "PROPERTY"},
    )

    for p in posts:
        post_counter += 1
        price = p.find("div", zp_attributes["price"]).text
        address = p.find("div", zp_attributes["address"])
        location = p.find("h2", zp_attributes["location"]).text
        expenses = p.find("div", zp_attributes["expenses"])
        all_features = p.findAll("h3", zp_attributes["features"])
        link = "https://www.zonaprop.com.ar" + p.get("data-to-posting")

        if expenses:
            expenses = expenses.text
        else:
            expenses = False
        if address:
            address = address.text
        else:
            address = False

        print(post_counter)
        output_posts_info(posts, price, address, location, expenses, all_features, link)

print("\n")
print(bcolors.OKGREEN + "Results: " + str(post_counter) + bcolors.ENDC)
print("\n")
