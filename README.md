# people_analytics

Estes notebooks foram criados com o intuito de criar três dashboards usando três técnicas de análise multivariada interativa diferentes, para a Disciplina: FT045 – Tópicos em Tecnologia para Informação II: Visualização de Informação
Turma A da Faculdade de tecnologia da Unicamp em Limeira. 

Para executar na ordem indicada, recomendamos que baixem e guardem na mesma pasta onde baixarem os notebooks, o arquivo PNAD correspondente ao 2 trimestre de 2023. 

Acesse o site de micro dados da PNAD Contínua: https://www.ibge.gov.br/estatisticas/sociais/trabalho/17270-pnad-continua.html?=&t=downloads
  a. Nele estão os microdados a serem consultados: Trimestral -> Microdados -> 2023-> PNADC_022023.zip (2º. trimestre de 2023).

Vamos executar os notebooks na seguinte ordem. 

1. TCT-Convertion.ipynb
  Este notebook converte o formato txt com recurso a um index que possui o mapa das variáveis, num formato de dataframe pandas para facilitar o tratamento posterior.
  Decorrente deste notebook é criado um csv pnead_dividido2.csv

2. Seguinte, vamos rodar os 3 notebooks seguintes que irão iterar entre si (no caso do 2 e 3) para criar 3 novos csv com dados reduzidos a ser usados nos apps que criam os dashboards
   csv-creation-app1.csv
   csv-creation-app2.csv
   csv-creation-app3.csv
3. agora podemos rodar qualquer um dos dashboards, apenas acessando a terminal (dentro da pasta aberta) e executando o comando abaixo.
   python3 app1.py

4. Será possível visualizar as visualizações de cada dashboard, e até reaproveitar o código (peço desculpa pela manta de retalhos, mas estou aprendendo) para outros projetos. 
  app1 - http://127.0.0.1:8050
  app2 - http://127.0.0.1:8060
  app3 - http://127.0.0.1:8070

Obrigado 
João Gaspar

