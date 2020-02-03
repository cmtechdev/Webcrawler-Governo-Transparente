# https://www.governotransparente.com.br/acessoinfo/1404490/consultarempenhodiarias/resultado?ano=9&inicio=16%2F11%2F2018&fim=16%2F11%2F2019
from CrawlerGOV import *
import json

# salva as informacoes em um arquivo
def salvarBase( base ):
	try:
		dumps = json.dumps(base)
		saida = open("resultado.json", "w")
		saida.write( dumps )
		saida.close()
	except:
		return False
		
	return True

def main():
	'''
	Observacoes:
	* codigoCidade -------> Acessar o site para capturar;
	* opcaoMenuPrincipal -> despesasGerais, diarias
	* despesa ------------> empenho, liquidacoesDespesaOrcamentaria, liquidacoesRestoPagar, pagamentoDespesasOrcamentarias, pagamentoRestoPagar;
	'''
	dados = {
		"codigoCidade" : "1409490", # 1409490 - Prefeitura Municipal de Russas; 1398489 - Prefeitura Municipal de Quixada; 1225490 - Prefeitura Municipal de Crateus
		"opcaoMenuPrincipal" : "despesasGerais",
		"despesa" : "empenho", # os dados sao capturados mas embaralhado 
		"dias" : 365 # ele vai buscar os registros dos ultimos dias informados
	}
	
	crawler = CrawlerGOV( dados ) 
	base = crawler.extrair()
	
	if base == None:
		print("Nenhum registro encontrado no(s) ultimo(s)", dados["dias"], "dia(s).")
	else:
		if salvarBase( base ):
			print("Resultado salvo com sucesso.")
		else:
			print("Algum problema ocorreu enquanto sua base estava sendo salva. Tente novamente.")

main()
