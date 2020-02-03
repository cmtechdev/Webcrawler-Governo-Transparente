# Webcrawler Governo Transparente
A presente ferramenta foi implementada por necessidade encontrada em meio à participação no [Hackathon do TCE 2019](http://www.eventos.tce.ce.gov.br/hackathon-2019).
Com ela, você poderá obter dados diretos do site [Governo Transparente](https://www.governotransparente.com.br/).

## Antes de começar...
Antes de começar, é preciso garantir que o framework [MechanicalSoup](https://mechanicalsoup.readthedocs.io/en/stable/) está devidamente instalado no seu sistema. Para uma instalação rápida, você poderá utilizar o módulo `pip` do Python, seguindo o código abaixo:

  `python3 -m pip install mechanicalsoup`
  
## Coletando dados..
Para realizar a coleta dos dados, o único arquivo que irá precisar se preocupar em editar algo, será o **main.py**.
Nele, logo no início, após uma breve documentação (ótima, caso você não tenha lido o README), poderá se deparar com uma estrutura de dicionário do Python, atribuindo conteúdo à uma variável nomeada 'dados'. Por ela, você irá editar (conforme suas necessidades), os campos:

  - **codigoCidade** - Referente ao código da cidade gerado conforme entidade selecionada na página principal do site;
  - **opcaoMenuPrincipal** - Opção do menu principal encontrado após o informe da entidade desejada, tendo como possíveis valores: 'despesasGerais' ou 'diarias';
  - **despesa** - Tipo da despesa relacionada à busca, que podem conter os valores: 'empenho', 'liquidacoesDespesaOrcamentaria', 'liquidacoesRestoPagar', 'pagamentoDespesasOrcamentarias' ou 'pagamentoRestoPagar';
  - **dias** - Referente a quantidade de dias em que os registros devem ser buscados.
  
Ou seja, as chaves configuram uma busca comum na plataforma, tal como se estivesse manipulando a mesma de forma direta. Dessa forma, a chave **codigoCidade** deve ser notada com maior rigor, pois, é por ela que o webcrawler irá se situar. Para conseguir a mesma, basta seguir o passo a passo seguinte:

## Obtendo o código da cidade 
#### 1. Acessando o site
Utilizando o navegador de sua preferência (recomendo o Mozilla 
🦊), acesse o [site](https://www.governotransparente.com.br/) do Governo Transparente.
#### 2. Preenchendo os campos do formulário
Com a página carregada, será notado um formulário solicitando informações tais como 'Estado', 'Cidade' e 'Entidade'. Configure os mesmos conforme suas necesssidades e logo após, clique em 'Selecionar'.
#### 3. Agora é só prestar atenção
Sem mais necessidades em manipular algo na página, você deverá se ater ao link da mesma. Para fins demonstrativos, configurei a página anterior com os dados: 

  - Estado -> Ceará 
  - Cidade -> Russas 
  - Entidade -> Câmara Municipal de Russas
  
Que por sua vez, me gerou o link [https://www.governotransparente.com.br/1409589](https://www.governotransparente.com.br/1409589)
Ok, acredito que já tenha notado, porém, o **codigoCidade** que busca é esse exposto ao final da URL. (No caso exemplo, 1409589)

## Conclusões finais
Após executar o webcrawler, é possível que demande um pouco de tempo até que as informações estejam devidamente organizadas e salvas. Ao final, será gerado um arquivo nomeado por **resultado.json**, o qual conterá as informações resgatadas do sitema, estando prontas para seres analisadas, estudadas ou o que mais precisar.
