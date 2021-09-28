from structs import CLASIFF
import pandas as pd


# Generar un csv que representa a la entidad CRYPTO(id, nombre, categoria)
CRYPTO_NAME = list()
CRYPTO_CAT = list()

for i in CLASIFF:
    for j in CLASIFF[i]:
        CRYPTO_CAT.append(i)
        CRYPTO_NAME.append(j)

df = pd.DataFrame({"nombre" : CRYPTO_NAME, "categoria" : CRYPTO_CAT})
df.to_csv("out/crypto.csv", index=False)