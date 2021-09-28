from structs import DATES, EXT_FACT_CAT, CRYPTO, COUNTRY, PEOPLE
from random import choice, sample
import pandas as pd

if __name__ == "__main__":
    # Generar un csv con eventos que ocurrieron para una fecha determinada
    RAND_DESC = list()
    RAND_DESC_CAT = list()
    RAND_DATES = sample(DATES, k=len(DATES))
    for i in RAND_DATES:
        category = choice(list(EXT_FACT_CAT))
        fact = choice(EXT_FACT_CAT[category])
        RAND_DESC.append(fact)
        RAND_DESC_CAT.append(category)

    df = pd.DataFrame({"descripcion" : RAND_DESC, "categoria" : RAND_DESC_CAT, "fecha" : RAND_DATES})
    df.to_csv("out/factores.csv", index=False)