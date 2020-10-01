from bs4 import BeautifulSoup
import requests


def getBrands():
    base        = 'https://www.cultbeauty.co.uk'
    soup        = BeautifulSoup(requests.get(base + '/brands').text, 'html.parser')
    parent      = soup.find('ul', { 'class' : 'brandsList' })
    brands      = list(map(lambda n : base + n['href'].split('?')[0], parent.find_all('a', href = True)))
    return brands

def getProducts(link):
    base        = 'https://www.cultbeauty.co.uk/skin-care.html'
    soup        = BeautifulSoup(requests.get(link).text, 'html.parser')
    parent      = soup.find('div', { 'class' : 'productGrid' })
    products    = list(map(lambda n : base + n['href'].split('#')[0], parent.find_all('a', href = True)))
    return products


def getDetails(link):

    load_number = 0
    
    def getContent(items, text): #henter alle "kasserne" fra produkt siden
        for item in items:
            if item.find('div', {'class' : 'itemHeader'}).text.strip() == text.strip():
                return item.find('div', {'class' : 'itemContent'})
    
    def getDetails(node, tag, name):
        if (name == 'productSize'):
            return node.find(tag, {'class' : name}) #lav noget hacky hacky her
        else:
            return node.find(tag, {'class' : name}).text.strip('( )')
    
    soup    = BeautifulSoup(requests.get(link).text, 'html.parser')

    brand   = getDetails(soup, 'div' , 'productBrandTitle'  )
    name    = getDetails(soup, 'div' , 'productTitle'       )
    size    = getDetails(soup, 'span', 'productSize'        )  #AttributeError: 'NoneType' object has no attribute 'text' (se linje 33)
    sign    = getDetails(soup, 'span', 'productCurrency'    )
    price   = getDetails(soup, 'span', 'productPrice'       )
    

    
    boxes   = soup.find('ul', {'class' : 'productInfoInner' }).find_all('li')
    ingredients = getContent(boxes, 'Full ingredients list ').text

    print(brand, name, sign, price, ingredients, sep = ';') # seperer med ',' hvis gemmes i CSV
    print('\n')

products = getProducts('https://www.cultbeauty.co.uk/skin-care.html')  #  /products?loadedAmount=1980  # https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=1980&path=%2Fskin-care.html&parameters=%7B%7D
#print(len(products))

for p in products: 
    getDetails(p)













