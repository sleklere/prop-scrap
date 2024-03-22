from bs4 import BeautifulSoup
import cloudscraper

###################################
# ARGEN PROP
###################################

# no se puede buscar "asi nomas" como en zona prop, solo se puede buscar por ubicacion y seleccionando una opcion disponible

ap_attributes = {
    "price": {"class": "card__price"},
    "address": {"class": "card__address"},
    "location": {"class": "card__title--primary"},
    "expenses": {"class": "card__expenses"},
    "features": {"class": "card__main-features"},
}

scraper = cloudscraper.create_scraper()
page_to_scrape = scraper.get(
    "https://www.argenprop.com/oficinas/alquiler/vicente-lopez"
)  # para las siguientes paginas se agrega "?pagina-{num}"

soup = BeautifulSoup(page_to_scrape.text, "lxml")

posts = soup.findAll("div", attrs={"class": "listing__item"})

num_results_h1 = soup.find("p", attrs={"class": "listing-header__results"})
num_results = int(num_results_h1.text.split(" ")[0])
num_pages = round(num_results / 20)

########
# OUTPUT
########

print("Results: " + str(num_results))

counter = 0

if posts != True:
    print("No posts were found.")

for p in posts:
    price = p.find("p", ap_attributes["price"])
    address = p.find("p", ap_attributes["address"])
    location = p.find("p", ap_attributes["location"])
    expenses = p.find("span", ap_attributes["expenses"])
    all_features = p.findAll("ul", ap_attributes["features"])
    link = p.find("a")

    counter += 1

    print(counter)
    print("Precio: " + price.text.strip())
    if address:
        print("Dirección: " + address.text.strip())
    print("Ubicación: " + location.text)
    if expenses:
        print(expenses.text)
    else:
        print("Post without expenses")

    span_tags = all_features[0].findAll("span")
    features_str = ""
    for span in span_tags:
        features_str += span.text.strip() + " - "
    print("Otras características: " + features_str)
    url = "https://www.argenprop.com" + link.get("href")
    print(url)
    print("------------------------------")
    # print("\n")
