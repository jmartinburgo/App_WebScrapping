import requests
from bs4 import BeautifulSoup
from lxml import etree
from flask import Flask, jsonify


app= Flask(__name__)

@app.route('/mercadoLibre',methods=["GET"])
def mercadoLibre():

    lista_titulos=[]
    lista_urls=[]
    lista_precios=[]

    siguiente='https://listado.mercadolibre.com.ar/computadora'
    while True:
        r= requests.get(siguiente)
        if r.status_code ==200:
            soup=BeautifulSoup(r.content,'html.parser')
            #Titulos
            titulos=soup.find_all('h2',attrs={"class":"ui-search-item__title shops__item-title"})
            titulos= [i.text for i in titulos]
            lista_titulos.extend(titulos)
            #Urls
            urls=soup.find_all('a',attrs={"class":"ui-search-item__group__element shops__items-group-details ui-search-link"})
            urls=[i.get('href') for i in urls]
            lista_urls.extend(urls)
            #Precios
            dom= etree.HTML(str(soup))
            precios=dom.xpath('//div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="andes-money-amount__fraction"]')
            precios=[i.text for i in precios]
            lista_precios.extend(precios)
            ini= soup.find('span',attrs={'class':'andes-pagination__link'})
            ini=int(ini.text)
            can= soup.find('li',attrs={'class':'andes-pagination__page-count'})
            can=int(can.text.split(sep=" ",maxsplit=1)[1])


        else:
            break
        print(ini,can,siguiente)

        if ini==can:
            break
        siguiente=dom.xpath('//li[@class="andes-pagination__button andes-pagination__button--next shops__pagination-button"]//a[@class="andes-pagination__link shops__pagination-link ui-search-link"]')[0].get('href')
    return jsonify({"datos":{"titulos":lista_titulos,"urls":lista_urls,"precios":lista_precios}})

if __name__=="__main__":
    app.run(debug=True)

