from bs4 import BeautifulSoup
import cloudscraper
from util import output_posts_info, Scraper, bcolors

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

ap_scraper = Scraper(
    "https://www.argenprop.com/oficinas/alquiler/vicente-lopez",
    "p",
    {"class": "listing-header__results"},
)


num_pages = ap_scraper.get_num_pages()

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
    posts = ap_scraper.scrap_posts(
        f"https://www.argenprop.com/oficinas/alquiler/vicente-lopez?pagina-{page}",
        {"class": "listing__item"},
    )
    for p in posts:
        post_counter += 1
        price = p.find("p", ap_attributes["price"]).text
        address = p.find("p", ap_attributes["address"]).text.strip()
        location = p.find("p", ap_attributes["location"]).text
        expenses = p.find("span", ap_attributes["expenses"])
        all_features = p.findAll("ul", ap_attributes["features"])
        relative_link = p.find("a")
        link = "https://www.argenprop.com" + relative_link.get("href")

        if expenses:
            expenses = expenses.text.split(";")[1].split(" ")[1]
            price = price.split("&")[0]
        else:
            expenses = False
        price = price.strip()

        output_posts_info(posts, price, address, location, expenses, all_features, link)

print("\n")
print(bcolors.OKGREEN + "Results: " + str(post_counter) + bcolors.ENDC)
print("\n")
