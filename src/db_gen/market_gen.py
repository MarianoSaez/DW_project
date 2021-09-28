from structs import DATES
from json import loads, dumps
import pandas as pd


if __name__ == "__main__":
    CRYPTO_NAME = list()
    CRYPTO_PRICE = list()
    CRYPTO_MC = list()
    CRYPTO_DATE = list()
    CRYPTO_VOL = list()
    
    f = open("data/coin.log", "r")
    data = loads(f.read())
    for date in data:
        for crypto in data[date]:
            CRYPTO_DATE.append(date)
            CRYPTO_NAME.append(crypto)
            CRYPTO_PRICE.append(data[date][crypto]["precio"])
            CRYPTO_MC.append(data[date][crypto]["cap_bursatil"])
            CRYPTO_VOL.append(data[date][crypto]["volumen"])


    df = pd.DataFrame({"nombre" : CRYPTO_NAME, "fecha" : CRYPTO_DATE, "precio" : CRYPTO_PRICE, "cap_bursatil" : CRYPTO_MC, "volumen" : CRYPTO_VOL})
    df.to_csv("out/mercado.csv", index=False)