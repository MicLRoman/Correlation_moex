import requests
from time import sleep

class MOEX():

    base = "https://iss.moex.com"

    def get_correlations_data(self, start=0):

        data = []

        while data==[]:
            try:
                data = requests.get(f"{self.base}/iss/statistics/engines/stock/markets/shares/correlations.json?start={start}")
                print(f"{self.base}/iss/statistics/engines/stock/markets/shares/correlations.json?start={start}")
            except:
                sleep(5)

        return data.json()
    
    def get_correlation_on_ticker(self, ticker, limit):

        res = [] 
        data = self.get_correlations_data()
        total = data["coefficients.cursor"]["data"][0][1]
        diff = data["coefficients.cursor"]["data"][0][2]

        start = 0
        while total>=start:
            data = (self.get_correlations_data(start=start))["coefficients"]

            #[nedded, finded, coeff]

            #Second stage
            for share in data["data"]:
                if ticker == share[1] and ticker!=share[0]:
                    if ((ticker, share[0], share[3]) not in res) and (type(share[3])==float) and (len(share[0])<10):
                        res.append((ticker, share[0], share[3]))

            #First stage
            for share in data["data"]:
                if ticker == share[0] and ticker!=share[1]:
                    if ((ticker, share[1], share[3]) not in res) and (type(share[3])==float) and (len(share[1])<10):
                        res.append((ticker, share[1], share[3]))

            start += diff

        res.sort(key=lambda x: x[2], reverse=True)

        return res[:limit]


    
if __name__ == "__main__":

    bot = MOEX()

    ticker_in = input("Введите нужный вам тикер:\n")
    limit_in = int(input("Сколько мест будет в вашем топе корреляций:\n"))
    print("\nждём.\n")
    res = bot.get_correlation_on_ticker(ticker=ticker_in, limit=limit_in)


    print(f"Ваш тикер ; Коррелирующий тикер ; Коофициент корреляции")
    l = 1
    for correlation in res:
        print(f"{l}. {correlation[0]} ; {correlation[1]} ; {correlation[2]}")
        l += 1

    out = input("\nНажмите Enter чтобы выйти")