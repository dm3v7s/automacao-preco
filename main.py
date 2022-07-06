from google_shopping import busca_google
from americanas import americanas
import pandas as pd

# importando a base de informações
lista = pd.read_excel("lista.xlsx")

# Criando a tabela
tabela_ofertas = pd.DataFrame()

for linha in lista.index:
    produto = lista.loc[linha, "Nome"]
    termos_banidos = lista.loc[linha, "Termos banidos"]
    preco_min = lista.loc[linha, "Preço mínimo"]
    preco_max = lista.loc[linha, "Preço máximo"]



    lista_ofertas_google = busca_google(produto, termos_banidos, preco_max, preco_min)
    if lista_ofertas_google:
        tabela_google = pd.DataFrame(lista_ofertas_google, columns=['nome', 'preco', 'link'])
    else:
        tabela_google = None

    lista_ofertas_americanas = americanas(produto, termos_banidos, preco_max, preco_min)
    if lista_ofertas_americanas:
        tabela_americanas = pd.DataFrame(lista_ofertas_americanas, columns=['nome', 'preco', 'link'])
    else:
        tabela_americanas = None

    display(tabela_ofertas)

