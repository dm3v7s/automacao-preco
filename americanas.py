from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def americanas(produto, palavras_banidas, preco_max, preco_min):
    # input do produto para pesquisa de preço
    produto = produto.lower()

    # Declaração dos termos banidos
    palavras_banidas = palavras_banidas.lower()

    # lista com os termos banidos
    lista_palavras_banidas = palavras_banidas.split(" ")

    # Lista dos termos do produto
    lista_termos_produtos = produto.split(" ")

    # Preço max e preço min
    preco_max = float(preco_max)
    preco_min = float(preco_min)

    # Criação do navegador
    browser = webdriver.Firefox()

    # Entrando no site
    browser.get("https://www.americanas.com.br/")

    # Selecionando a barra e pesquisando o produto
    barra_de_pesquisa = browser.find_element(By.XPATH,
                                             '/html/body/div/div/div/header/div[1]/div[1]/div/div[1]/form/input')
    barra_de_pesquisa.send_keys(produto, Keys.ENTER)

    # esperar
    time.sleep(9)

    # lista de ofertas
    lista_de_ofertas = []

    # Selecionando o resultado
    selecao_do_resultado = browser.find_elements(By.CLASS_NAME, 'inStockCard__Wrapper-sc-1ngt5zo-0')

    # Percorrendo os elementos dentro da selecao do resultado
    for elemento in selecao_do_resultado:
        # Nomes dos produtos
        nome_elemento_produto = elemento.find_element(By.CLASS_NAME, 'product-name__Name-sc-1shovj0-0').text
        nome_elemento_produto = nome_elemento_produto.lower()

        # Percorrendo a lista para verificar se o termo banido está no nome
        tem_palavra_banida = False
        for palavra in lista_palavras_banidas:
            if palavra in nome_elemento_produto:
                tem_palavra_banida = True

        # Verificar se a pesquisa é igual ao resultado
        # Percorrendo a lista de palavras da pesquisa
        tem_todas_as_palavras = True
        for palavra in lista_termos_produtos:
            if palavra not in nome_elemento_produto:
                tem_todas_as_palavras = False

        if tem_palavra_banida == False and tem_todas_as_palavras:
            # preço do produto
            preco_elemento_produto = elemento.find_element(By.CLASS_NAME, 'src__Text-sc-154pg0p-0').text
            preco_elemento_produto = preco_elemento_produto.replace("R$", "").replace(" ", "").replace(".", "").replace(
                ",", ".")
            try:
                preco_elemento_produto = float(preco_elemento_produto)
            except:
                pass

            # Verificação do preço se está entre o max e o min
            if preco_min <= preco_elemento_produto <= preco_max:
                # link para o produto na loja
                elemento_filho = elemento.find_element(By.CLASS_NAME, 'image-info__Wrapper-sc-1xptwuk-0')
                elemento_pai = elemento_filho.find_element(By.XPATH, '..')
                link_elemento_produto = elemento_pai.get_attribute('href')

                # mandando o resultado para a lista
                lista_de_ofertas.append((nome_elemento_produto, preco_elemento_produto, link_elemento_produto))
    browser.close()
    return lista_de_ofertas