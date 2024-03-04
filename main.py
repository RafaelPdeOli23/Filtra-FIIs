import requests
from bs4 import BeautifulSoup
import locale
import tabulate
from modelos import FundoImobiliario, Estrategia

#Tratamento dos numeros
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def trata_porcentagem(porcentagem_str):
    return  locale.atof(porcentagem_str.split('%')[0])

def trata_decimal(decimal_str):
    return locale.atof(decimal_str)

#Coleta dos Dados
headers = {'User-agent':'Mozilla/5.0'}
r = requests.get('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

soup = BeautifulSoup(r.text,'html.parser')

linhas = soup.find(id = "tabelaResultado").find('tbody').find_all('tr')

#Lista com todos os fundos filtrados
resultado  = []

#Estratégia de investimento definida de forma abritária
estrategia = Estrategia(
    segmento='',
    dividend_yield_minimo=8,
    p_pv_maximo=1,
    liquidez_minima=800000,
    vacancia_media_maxima=10
)

#Intera na lista com todos os fundos, colocando os devidos valores às variáveis abaixo
for linha in linhas:
    dados_fundo = linha.find_all('td')
    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao_atual = trata_decimal(dados_fundo[2].text)
    dividend_yield = trata_porcentagem(dados_fundo[4].text)
    p_pv = trata_decimal(dados_fundo[5].text)
    liquidez = trata_decimal(dados_fundo[7].text)
    vacancia_media = trata_porcentagem(dados_fundo[12].text)

    fundo_imobiliario = FundoImobiliario(codigo, segmento, cotacao_atual, dividend_yield,
                                         p_pv, liquidez, vacancia_media)

    #Filtro aplicado de acordo com a estratégia predefinida
    if estrategia.aplica_estrategia(fundo_imobiliario):
       resultado.append(fundo_imobiliario)

#Esqueleto da tabela
cabecalho = ['CÓDIGO', 'SEGMENTO', 'COTAÇÃO ATUAL', 'DIVIDEND YIELD', 'P/PV']
tabela = []

#Colocando os dados filtrados dentro da tabela
for elemento in resultado:
    tabela.append([
        elemento.codigo, elemento.segmento,
        locale.currency(elemento.cotacao_atual),
        f'{locale.str(elemento.dividend_yield)} %', elemento.p_pv
    ])

print(tabulate.tabulate(tabela, headers=cabecalho,showindex='always', tablefmt='fancy_grid'))
