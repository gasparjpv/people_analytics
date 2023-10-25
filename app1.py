import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Carregar os dados
df = pd.read_csv('dados_selecionados-app1.csv')
df = df[df['V2005'] == 'Pessoa responsável']

# Definir faixas etárias para as gerações
geracoes = {
    'Geração Z': (0, 24),
    'Geração Y (Millennials)': (25, 44),
    'Geração X': (45, 64),
    'Baby Boomers': (65, 74),
    'Geração Silenciosa': (75, 107)  # ou o valor máximo de idade que você considerar adequado
}

# Função para atribuir a geração com base na idade
def atribuir_geracao(idade):
    for geracao, (limite_inferior, limite_superior) in geracoes.items():
        if limite_inferior <= idade <= limite_superior:
            return geracao
    return 'Outra'  # Para idades fora das faixas especificadas

# Criar uma nova coluna 'Geração' com base na idade

df['Geração'] = df['V2009'].apply(atribuir_geracao)

# Estados a ser usados no DIV

estados = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás', 
           'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 
           'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 
           'São Paulo', 'Sergipe', 'Tocantins']

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo com bordas nas caixas de filtro
app.layout = html.Div([
    html.Div([
        html.Img(src='assets/ft.png',style={'width': '100px', 'height': '100px', 'display': 'inline-block', 'margin-left': '10px'}),
        html.Img(src='assets/unicamp.png',style={'width': '100px', 'height': '100px', 'display': 'inline-block', 'position': 'absolute', 'right': '10px'}),

    ]),


    html.H1('Dashboard dados demográficos'),
    html.P('Análise demográfica baseada no responsável pelo domicílio entrevistado.'),



    html.Div([
        html.Label('Unidade Federativa:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Dropdown(
            id='filter-estado',
            options=[{'label': estado, 'value': estado} for estado in estados],
            multi=True,
            value=estados,  # Valores padrão
            style={'display': 'block','height': '10%', 'margin-top':'20px', 'margin-bottom':'20px'}
        )
    ]),
    
    # Filtro de Sexo com borda
    html.Div([
        html.Label('Filtro de Sexo:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Checklist(
            id='filter-sex',
            options=[
                {'label': 'Masculino', 'value': 'Homem'},
                {'label': 'Feminino', 'value': 'Mulher'},
            ],
            value=['Homem', 'Mulher'],
            labelStyle={'display': 'block'}
        ),
    ], style={'display': 'inline-block', 'width': '10%', 'border': '1px solid #000', 'padding': '10px','margin-right': '10px',}),
    
    # Filtro de Raça com borda
    html.Div([
        html.Label('Filtro de Raça:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Checklist(
            id='filter-race',
            options=[
                {'label': 'Branca', 'value': 'Branca'},
                {'label': 'Preta/Parda', 'value': 'Preta/Parda'},
                {'label': 'Outros', 'value': 'Outros'},
                {'label': 'Ignorado', 'value': 'Ignorado'},
                
            ],
            value=['Branca', 'Preta/Parda', 'Outros', 'Ignorado'],  # Valores padrão
            labelStyle={'display': 'block'}
        ),
    ], style={'display': 'inline-block', 'width': '10%', 'border': '1px solid #000', 'padding': '10px','margin-right': '10px'}),
    


    
    # Filtro de Geração com borda
    html.Div([
        html.Label('Filtro de Geração:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Checklist(
            id='filter-generation',
            options=[
                {'label': 'Geração Z - (0, 24)' , 'value': 'Geração Z'},
                {'label': 'Geração Y (Millennials) - (25, 44)', 'value': 'Geração Y (Millennials)'},
                {'label': 'Geração X - (45, 64)', 'value': 'Geração X'},
                {'label': 'Baby Boomers - (65, 74)', 'value': 'Baby Boomers'},
                {'label': 'Geração Silenciosa - (75, 107)', 'value': 'Geração Silenciosa'},
            ],
            value=['Geração Z', 'Geração Y (Millennials)', 'Geração X', 'Baby Boomers', 'Geração Silenciosa'],
            labelStyle={'display': 'block'}
        ),
    ], style={'display': 'inline-block', 'width': '20%', 'border': '1px solid #000', 'padding': '10px','margin-right': '10px'}),
    


    # Filtro de Rendimento com borda
    html.Div([
        html.Label('Filtro de Rendimento:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Checklist(
            id='filter-income',
            options=[
                    {'label':'0,5 +1 a 1k', 'value':'0,5 +1 a 1k'},
                    {'label':'1k+1 a 2k', 'value':'1k+1 a 2k'},
                    {'label':'2k+1 a 3k', 'value':'2k+1 a 3k'},
                    {'label':'3k+1 a 5k', 'value':'3k+1 a 5k'},
                    {'label':'5k+1 a 10k', 'value':'5k+1 a 10k'},
                    {'label':'10k+1 a 20k', 'value':'10k+1 a 20k'},
                    {'label':'mais de 20k', 'value':'mais de 20k'},
                    {'label' : 'Não aplicável','value':'Não aplicável'},
            ],
            value=['0,5 +1 a 1k', '1k+1 a 2k',  '2k+1 a 3k', '3k+1 a 5k', '5k+1 a 10k', '10k+1 a 20k', 'mais de 20k', 'Não aplicável'],  # Valores padrão
            labelStyle={'display': 'block'}
        ),
    ], style={'display': 'inline-block', 'width': '10%', 'border': '1px solid #000', 'padding': '10px','margin-right': '10px'}),
    
    # Gráfico
    dcc.Graph(
    id='parallel-categories-plot',
    style={'height': '700px'}  # Ajuste a altura conforme necessário
)
])

   
# Callback para atualizar o gráfico com base nas seleções
@app.callback(
    Output('parallel-categories-plot', 'figure'),
    Input('filter-sex', 'value'),
    Input('filter-race', 'value'),
    Input('filter-generation', 'value'),
    Input('filter-income', 'value'), 
    Input('filter-estado', 'value')
)
def update_parallel_categories(selected_sex, selected_race, selected_generation, selected_income, selected_estado):
    filtered_df = df[df['V2007'].isin(selected_sex) & df['Geração'].isin(selected_generation) & df['V403311'].isin(selected_income) & df['V2010'].isin(selected_race) & df['UF'].isin(selected_estado)]
    
    fig = px.parallel_categories(filtered_df, dimensions=['V2007', 'V2010', 'V403311'],
                color="V2009", color_continuous_scale=px.colors.sequential.Inferno,
                labels={'V2007':'Sexo', 'V2010': 'Raça', 'V403311':'Faixa rendimento', 'V2009':'Idade'}
                )
    
    
    return fig

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=False, port=8050)