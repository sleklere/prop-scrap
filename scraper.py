from bs4 import BeautifulSoup
import cloudscraper

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


references = {
    "price_class": "sc-12dh9kl-3 iqNJlX",
    "address_class": "sc-ge2uzh-0 eWOwnE postingAddress",
}

attributes = {
    "price": {"data-qa": "POSTING_CARD_PRICE"},
    "address": {"class": references["address_class"]},
    "location": {"data-qa": "POSTING_CARD_LOCATION"},
    "expenses": {"data-qa": "expensas"},
    "features": {"data-qa": "POSTING_CARD_FEATURES"},
}

scraper = cloudscraper.create_scraper()

page_to_scrape = scraper.get(
    "https://www.zonaprop.com.ar/alquiler-q-oficina-vicente-lopez.html"
)

soup = BeautifulSoup(page_to_scrape.text, "lxml")

posts = soup.findAll("div", attrs={"data-posting-type": "PROPERTY"})

num_results_h1 = soup.find("h1", attrs={"class": "sc-1oqs0ed-0 cvTPma"}, recursive=True)
num_results = int(num_results_h1.text.split(" ")[0])
num_pages = round(num_results / 10)

########
# OUTPUT
########

counter = 0

for p in posts:
    price = p.find("div", attributes["price"])
    address = p.find("div", attributes["address"])
    location = p.find("h2", attributes["location"])
    expenses = p.find("div", attributes["expenses"])
    all_features = p.findAll("h3", attributes["features"])

    counter += 1

    print(counter)
    if address:
        print("Dirección: " + address.text)
    print("Ubicación: " + location.text)
    print("Precio: " + price.text)
    if expenses:
        print(expenses.text)
    else:
        print("Post without address")

    span_tags = all_features[0].findAll("span")
    features_str = ""
    for span in span_tags:
        features_str += span.text + " - "
    print("Otras características: " + features_str)
    link = "https://www.zonaprop.com.ar" + p.get("data-to-posting")
    print(link)
    print("\n")
