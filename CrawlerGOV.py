from datetime import date
import HTMLHandler
import mechanicalsoup
import json

class CrawlerGOV():
	def __init__(self, dados):
		userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'   
		self.browser = mechanicalsoup.StatefulBrowser( user_agent=userAgent )
		self.dados = dados
		#self.source = browser.open("https://www.governotransparente.com.br/" + codigoCidade).text
	
	def __gerarLink(self):
		consultas = {
			"empenho" : "empenho",
			"liquidacoesDespesaOrcamentaria" : "liqdesporc",
			"liquidacoesRestoPagar" : "liqrestpag",
			"pagamentoDespesasOrcamentarias" : "pagdesporc",
			"pagamentoRestoPagar" : "pagrestpag",
			"pagamentoDespesasExtraorcamentarias" : "pagdespextraorc"
		}
		dataFim = date.today()
		diaFim = "0" + str(dataFim.day) if dataFim.day < 10 else str(dataFim.day)
		mesFim = "0" + str(dataFim.month) if dataFim.month < 10 else str(dataFim.month)
		
		dataInicio = date.fromordinal(dataFim.toordinal()- int(self.dados["dias"]) )
		diaInicio = "0" + str(dataInicio.day) if dataInicio.day < 10 else str(dataInicio.day)
		mesInicio = "0" + str(dataInicio.month) if dataInicio.month < 10 else str(dataInicio.month)
		
		if self.dados["opcaoMenuPrincipal"] == "despesasGerais":
			links = [ "https://www.governotransparente.com.br/transparencia/" + self.dados["codigoCidade"] + "/consultar" + consultas[ self.dados["despesa"] ] + "/resultado?ano=" + str(anoExercicio) + "&inicio=" + diaInicio + "%2F" + mesInicio + "%2F" + str(dataInicio.year) + "&fim=" + diaFim + "%2F" + mesFim + "%2F" + str(dataFim.year) for anoExercicio in range(1, 20) ]
			
		elif self.dados["opcaoMenuPrincipal"] == "diarias":
			links = [ "https://www.governotransparente.com.br/acessoinfo/" + self.dados["codigoCidade"] + "/consultar" + consultas[ self.dados["despesa"] ] + "diarias/resultado?ano=" + str(anoExercicio) + "&inicio=" + diaInicio + "%2F" + mesInicio + "%2F" + str(dataInicio.year) + "&fim=" + diaFim + "%2F" + mesFim + "%2F" + str(dataFim.year) for anoExercicio in range(1, 20) ]
		#print( links )
		
		return links
	
	# remove todos os caracteres nao alfabeticos e retornar a expressao em camel case
	def __tratar(self, expressao):
		novaExpressao, componentes = "", expressao.split(' ')
		
		for expressao in componentes:
			auxiliar = ""
			for caractere in expressao:
				if caractere.isalpha():
					auxiliar += caractere.lower()
			
			if novaExpressao:
				novaExpressao += auxiliar[0].upper() + auxiliar[1:]
			else:
				novaExpressao += auxiliar
		
		return novaExpressao
	
	def __obterElementos(self, html, tag, camelCase, quantidade=-1, ignorar=[], removerTags=True):
		titulos, idTitulo = dict(), 0
		while True:
			try:
				indice = html.index( tag )
			except:
				break
			
			if quantidade == 0:
				break
			
			tratar = True
			elemento = HTMLHandler.getScopeTag( indice, html ).replace("\n", "").replace("\r", ""). replace("\t", "")
			html = html[indice+len(elemento):]
			
			#print( indice, html[indice:indice+10] )
			if not idTitulo in ignorar:
				
				# se houver um link no elemento em questao, os mesmo sera capturado
				if 'href="' in elemento:
					#print("temos um link")
					link = "https://www.governotransparente.com.br" + HTMLHandler.extractLink( elemento )
					#print( link )
					novoCodigo = self.browser.open( link ).text.replace("<!-- ", "").replace("-->", "")
					
					if "<ul>" in novoCodigo:
						indice = novoCodigo.index("<ul>")
						novoCodigo = HTMLHandler.getScopeTag( indice, novoCodigo )
						
						novosElementos = self.__obterElementos( novoCodigo, "<li>", camelCase=False, removerTags=True)
				
					informacoes = dict()
					elemento = HTMLHandler.stripTags(elemento)
					informacoes[elemento] = novosElementos
					elemento = informacoes
					
					tratar = False
				
				if camelCase and tratar:
					elemento = HTMLHandler.stripTags( elemento )
					titulos[ idTitulo ] = self.__tratar( elemento )
				elif removerTags:
					titulos[ idTitulo ] = HTMLHandler.stripTags( elemento )
				else:
					titulos[ idTitulo ] = elemento
				
			
			idTitulo += 1
			quantidade -= 1
			tratar = True
		
		return titulos
	
	def __construirTabela(self, quantidade=-1):
		links = self.__gerarLink()
		
		quantidadeAuxiliar = quantidade
		tabelaGeral = dict()
		for link in links:
			if "ano=8" in link:
				print( link )
			quantidade = quantidadeAuxiliar
			print("Obtendo informacoes do site...")
			codigo = self.browser.open( link ).text.replace("<!-- ", "").replace("-->", "")
			
			if "Erro interno no servidor" in codigo:
				continue
			anoExercicio = codigo[codigo.find("Exercício de ") + 13: codigo.find("Exercício de ") + 17]
			print("Ano exercicio:", anoExercicio)
			try:
				indice = codigo.index("<thead>")
			except:
				tabelaGeral[ anoExercicio ] = "Nenhum registro encontrado"	
				continue
				
			escopoTitulos = HTMLHandler.getScopeTag( indice, codigo )
			titulos = self.__obterElementos( html=escopoTitulos, tag="<th>", camelCase=True )
			
			# cria a tabela final
			tabela, indices, idTabela = dict(), [], 0
			for chave in titulos:
				indices.append( titulos[chave] )
			
			# atualizacao necessaria para a obtencao das linhas
			indice = codigo.index("<tbody>")
			codigo = codigo[indice+len("<tbody>"):]
			
			# obtem os elementos
			while True:
				if (not "<td" in codigo) or quantidade == 0:
					break
				
				# tags a ignorar - Motivo: Algumas sao apenas comentarios no codigo
				if self.dados["despesa"] == "empenho":
					ignorar = [1]
				else:
					ignorar = []
					
				elemento = self.__obterElementos( html=codigo, tag="<td", camelCase=False, quantidade=len(titulos)+len(ignorar), ignorar=ignorar )
				
				# atualiza a tabela
				tabela[idTabela], idIndices = dict(), 0
				for chave in elemento:
					tabela[idTabela][ indices[ idIndices ] ] = elemento[chave]
					idIndices += 1
				
				print("Faltando analisar:", len(codigo), "bytes" )
				codigo = codigo[ codigo.index("</tr>")+1: ]
				idTabela += 1
				quantidade -= 1
			
			print("tabela do ano", anoExercicio, len(tabela))
			tabelaGeral[ anoExercicio ] = tabela
			
		return tabelaGeral
		
	# extrai as informacoes desejadas
	def extrair(self):
		
		print("Organizando...")
		base = self.__construirTabela()
		print("Informacoes organizadas.")
		
		return base