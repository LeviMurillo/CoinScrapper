import requests
import base64
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36")

#Obtiene el precio de una moneda en particular, usa menos recursos que Bitso2
def Bitso(coin):
    response = requests.get("http://bitso.com/market/"+coin+"/mxn")
    parsedHTML = BS(response.text,'html.parser')
    price = parsedHTML.find_all(class_="stat-value")[5].strings
    return {i:a.strip() for i,a in zip(['value','currency'],price)}

#Obtiene el precio de una moneda en particular, es mejor usar Binance2
def Binance(coin):
    browser = webdriver.Chrome(options=chromeOptions)
    browser.get("http://www.binance.com/en/trade/"+coin)
    info = browser.find_elements_by_css_selector('div.subPrice')
    price = [a.text for a in info]
    browser.quit()
    return {'value':price[0],'currency':'USD'}

def Binance2():
    browser = webdriver.Chrome(options=chromeOptions)
    browser.get("http://www.binance.com/en/markets")
    tabs = browser.find_elements_by_css_selector('div.css-sin44v')
    tabs += browser.find_elements_by_css_selector('div.css-l62sg9')
    #La página muestra varias pestañas, la información que nos interesa se encuentra en la pestaña 'Zones'
    for a in tabs:
        if a.text == 'Zones':
            a.click()
    browser.implicitly_wait(10)
    names = browser.find_elements_by_css_selector('div.css-1wp9rgv')
    prices = browser.find_elements_by_css_selector('div.css-ydcgk2')
    info = dict(zip([name.text for name in names],[price.text+' USD' for price in prices]))
    browser.quit()
    return info

def Coinbase():    
    browser = webdriver.Chrome(options=chromeOptions)
    browser.get("https://coinbase.com/es/price")
    browser.implicitly_wait(10)
    names = browser.find_elements_by_class_name('cdqGcC')
    prices = browser.find_elements_by_class_name('bxoSRw') 
    #hay 4 elementos con esta misma clase (bxoSRw) en cada fila, pero podemos filtrar estos resultados usando enumerate dentro de una comprensión de lista  
    info = dict(zip([name.text for name in names],[price[1].text for price in enumerate(prices) if price[0]%4 == 0]))
    browser.quit()
    return info

def Yahoo():
    response = requests.get("http://finance.yahoo.com/cryptocurrencies/")
    parsedHTML = BS(response.text,'html.parser')
    search = lambda i: parsedHTML.select('[data-reactid="'+str(i)+'"]')[0].text
    info = {search(i):search(i+5) for i in range(87,249,32)} #Solo tomamos los primeros 5
    #TODO: Checar si la numeración cambia con el tiempo
    return info
    
def Bitso2():
    browser = webdriver.Chrome(options=chromeOptions)
    browser.set_window_size(1920, 1080) #El tamaño por default del navegador no muestra algunos elementos.
    browser.get("http://bitso.com/")
    browser.implicitly_wait(10)
    hover = ActionChains(browser).move_to_element(browser.find_element_by_class_name('deniUR'))
    hover.perform() # para mostrar la columna con los precios
    names = browser.find_elements_by_class_name('ldYZUj')
    prices = browser.find_elements_by_class_name('hokqet')
    info = dict(zip([name.text for name in names],[price.text for price in prices]))
    browser.quit()
    return info

#TODO: Usar websockets, ya que es muy similar a los anteriores
def CoinMarketCap(): 
    return 1 

#TODO: Homogeneizar los datos
print("Bitso\n", Bitso2())
print("Binance\n", Binance2())
print("Coinbase\n", Coinbase())
print("Yahoo Finance:\n", Yahoo())
