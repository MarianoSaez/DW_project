import requests
import json
import time
from datetime import timedelta, datetime
from structs import CRYPTO, DATES


COIN_GECKO_API = "https://api.coingecko.com/api/v3/"

ENDPOINT_LIST = [
    "asset_platforms",
    "coins/{id}/history?date={date}",
]

class CoinGeckoAPI():

    def __init__(self, ):
        self.ids = CRYPTO
        self.file = open("data/coin.log", "w+")
        self.result = {i : dict() for i in self.ids}
        print(f"[CoinGeckoAPI][INFO] : Se obtuvieron {len(self.ids)} identificadores!")


    def get_ids(self):
        response = requests.get(COIN_GECKO_API + ENDPOINT_LIST[0])
        data = response.json()

        # Agregar bitcoin
        data.append({"id" : "bitcoin"})
        return [ crypto["id"] for crypto in data ]

    def get_history_all(self):

        print(f"[CoinGeckoAPI][INFO] : Buscando historial de precios")
        history = {i : dict() for i in DATES}
        for date in DATES:
            for identifier in self.ids:
                try:
                    response = requests.get(COIN_GECKO_API + ENDPOINT_LIST[1].format(id=identifier, date=date))
                    data = response.json()
                    history[date][identifier] = {
                                                    "volumen" : data["market_data"]["total_volume"]["usd"],
                                                    "cap_bursatil" : data["market_data"]["market_cap"]["usd"],
                                                    "precio" : data["market_data"]["current_price"]["usd"],
                                                }
                except KeyError as e:
                    print(f"[CoinGeckoAPI][ERROR] : No hay {e} para {identifier}! - No se agregara a la lista")
                except json.JSONDecodeError:
                    print(f"[CoinGeckoAPI][ERROR] : Demasiadas peticiones! - Esperando 65 segundos [LA API ES GRATIS]")
                    print(f"[CoinGeckoAPI][INFO] : La ultima fecha solicitada es {date}")
                    time.sleep(65)
                    self.ids.remove(identifier)
                    self.ids.append(identifier)
                except Exception as e:
                    f = open("data/aux.log", "w+")
                    f.write(json.dumps(history, indent=8))
                    f.flush()
                    print(f"[CoinGeckoAPI][ERROR] : Error fatal - {e} - Guardado en data/aux.log")
    
        self.file.write(json.dumps(history, indent=8))

        print(f"[CoinGeckoAPI][INFO] : Historial generado con exito!")

        return history


def mainGecko():
    g = CoinGeckoAPI()
    g.get_history_all()


if __name__ == "__main__":
    mainGecko()