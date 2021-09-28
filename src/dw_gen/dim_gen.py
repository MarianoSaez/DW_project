import pandas as pd
import json


dfMercado = pd.read_csv("out/mercado.csv")
dfCrypto = pd.read_csv("out/crypto.csv")
dfFactores = pd.read_csv("out/factores.csv")

def genDimTiempo():
    # Creando la dimension tiempo
    #   dimTiempo(idFecha, dia, mes, year)
    listaFechas = set(dfMercado["fecha"].to_list())
    listaDias = list()
    listaMeses = list()
    listaYear = list()

    for fecha in listaFechas:
        splited = fecha.split("-")
        listaDias.append(splited[0])
        listaMeses.append(splited[1])
        listaYear.append(splited[2])

    dfTiempo = pd.DataFrame({
        "dia" : listaDias,
        "mes" : listaMeses,
        "year" : listaYear,
    })

    dfTiempo.to_csv("dim/dimTiempo.csv", index=True, index_label="idTiempo")

    return dfTiempo


def genDimCrypto():
    # Creando la dimension Crypto
    #   dimCrypto(idCrypto, nombre, categoria)
    dfCrypto.to_csv("dim/dimCrypto.csv", index=True, index_label="idCrypto")

    return dfCrypto


def genDimFactExt():
    # Creando la dimension FactExt
    #   dimFactExt(idFactExt, nombre, categoria)
    campos = ["descripcion", "categoria"]
    dfFactores.to_csv("dim/dimFactExt.csv", columns=campos, index=True, index_label="idFactExt")

    return dfFactores


if __name__ == "__main__":
    dfTiempo = genDimTiempo()
    dfCrypto = genDimCrypto()
    dfFactExt = genDimFactExt()

    data = open("data/coin.log", "r").read()
    coin = json.loads(data)

    listaIdTiempo = list()
    listaIdCrypto = list()
    listaIdFactExt = list()
    listaVolumenes = list()
    listaMediaMovil = list()

    for date in coin:
        splited = date.split("-")
        dayFilter = dfTiempo.loc[dfTiempo["dia"] == splited[0]]
        monthFilter = dayFilter.loc[dayFilter["mes"] == splited[1]]
        yearFilter = monthFilter.loc[monthFilter["year"] == splited[2]]

        # idTiempo para la tabla de hechos
        idTiempo = yearFilter.index.to_list()[0]

        #idFactExt para la tabla de hechos
        idFactExt = dfFactExt.index[dfFactores["fecha"] == date].to_list()[0]
        
        cryptoDict = coin[date]

        for crypto in cryptoDict:
            # idCrypto para la tabla de hechos
            idCrypto = dfCrypto.index[dfCrypto["nombre"] == crypto].to_list()[0]

            volumen = cryptoDict[crypto]["volumen"]
            mediaMovil = cryptoDict[crypto]["precio"]

            listaIdTiempo.append(idTiempo)
            listaIdFactExt.append(idFactExt)
            listaIdCrypto.append(idCrypto)
            listaVolumenes.append(volumen)
            listaMediaMovil.append(mediaMovil)
            

    dfTablaHechos = pd.DataFrame({
        "idFecha" : listaIdTiempo,
        "idCrypto" : listaIdCrypto,
        "idFactExt" : listaIdFactExt,
        "volumen" : listaVolumenes,
        "mediaMovil" : listaMediaMovil,
    })
    dfTablaHechos.to_csv("dim/tablaHechos.csv", index=False)


