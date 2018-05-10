from bs4 import BeautifulSoup
import requests
import time


class Quiniela:
    __url__ = "http://www.jugandoonline.com.ar/laquiniela/sorteos.asp?FechaFresh={0}"
    __WORDS__ = ["QUINIELA", "ALL"]
    @staticmethod
    def getpremios(date, parm):
        print(date)
        page = requests.get(Quiniela.__url__.format(date or time.strftime("%m/%d/%Y")))
        soup = BeautifulSoup(page.text, "html.parser")
        quinielas = soup.findAll(attrs={"face": "Verdana, Arial, Helvetica, sans-serif", "size": "1"})
        premios = soup.findAll(attrs={"color": "#FF0033", "size": 3})
        result = dict()
        for quini, premio in zip(quinielas, premios):
            if (parm.upper() in Quiniela.__WORDS__) or (quini.get_text().upper().find(parm.upper()) >= 0):
                result[quini.get_text()] = premio.get_text()
        return [{"Resultados": 0}, result][len(result) > 0]


if __name__ == '__main__':
    print(Quiniela.getpremios(''))
