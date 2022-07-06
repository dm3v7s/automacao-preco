from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def busca_google(produto, palavras_banidas, preco_max, preco_min):
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
    browser.get("https://www.google.com.br/")

    # Selecionando a barra de pesquisa do google e pesquisando
    barra_de_pesquisa = browser.find_element(By.XPATH,
                                             '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    barra_de_pesquisa.send_keys(produto)
    barra_de_pesquisa.send_keys(Keys.ENTER)

    # Capturando a barra de elementos
    time.sleep(3)
    barra_de_elementos = browser.find_elements(By.CLASS_NAME, 'hdtb-mitem')

    # Percorrendo a barra para encontrar o elemento Shopping
    for elemento_shopping in barra_de_elementos:
        if "Shopping" in elemento_shopping.text:
            elemento_shopping.click()
            break

    # Selecionando o resultado do shopping
    selecao_do_resultado = browser.find_elements(By.CLASS_NAME, 'sh-dgr__gr-auto')

    # lista de ofertas
    lista_de_ofertas = []

    # Percorrendo os elementos dentro da selecao do resultado
    for elemento in selecao_do_resultado:
        # Nomes dos produtos
        nome_elemento_produto = elemento.find_element(By.CLASS_NAME, 'Xjkr3b').text
        nome_elemento_produto = nome_elemento_produto.lower()
        print(nome_elemento_produto)

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
            preco_elemento_produto = elemento.find_element(By.CLASS_NAME, 'a8Pemb').text
            preco_elemento_produto = preco_elemento_produto.replace("R$", "").replace(" ", "").replace(".", "").replace(
                ",", ".")
            try:
                preco_elemento_produto = float(preco_elemento_produto)
            except:
                pass
            print(preco_elemento_produto)

            # Verificação do preço se está entre o max e o min
            if preco_min <= preco_elemento_produto <= preco_max:
                # link para o produto na loja
                elemento_filho = elemento.find_element(By.CLASS_NAME, 'bONr3b')
                elemento_pai = elemento_filho.find_element(By.XPATH, '..')
                link_elemento_produto = elemento_pai.get_attribute('href')
                print(link_elemento_produto)

                # mandando o resultado pra lista
                lista_de_ofertas.append((nome_elemento_produto, preco_elemento_produto, link_elemento_produto))

    browser.close()
    return lista_de_ofertas
