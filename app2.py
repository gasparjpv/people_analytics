import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


# Carregar os dados
df = pd.read_csv('dados_selecionados-app2.csv')

# Estados a ser usados no DIV
UF = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás', 
           'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 
           'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 
           'São Paulo', 'Sergipe', 'Tocantins']

#df['Idade'] = df['Idade'].astype(int)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout do aplicativo com bordas nas caixas de filtro
app.layout = html.Div([
    html.Div([
        html.Img(src='assets/ft.png',style={'width': '100px', 'height': '100px', 'display': 'inline-block', 'margin-left': '10px'}),
        html.Img(src='assets/unicamp.png',style={'width': '100px', 'height': '100px', 'display': 'inline-block', 'position': 'absolute', 'right': '10px'}),

    ]),
    
    
    html.H1('Dashboard dados educação'),
    html.P('Analise de indicadores relacionados a nucleo familiar e educação.'),
    

    html.Div([
        html.Label('Unidade Federativa:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Dropdown(
            id='filter-estado',
            options=[{'label': estado, 'value': estado} for estado in UF],
            multi=True,
            value=UF,  # Valores padrão
            style={'display': 'block','height': '10%', 'margin-top':'20px', 'margin-bottom':'20px'}
        )
    ]),
    
    
    # Filtro de tipo de domicilio 
    html.Div([
        html.Label('Rede Escolar:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Checklist(
            id='filter-domicilio',
            options=[
                {'label': 'Não aplicável', 'value': 'Não aplicável'},
                {'label': 'Rede privada', 'value': 'Rede privada'},
                {'label': 'Rede pública', 'value': 'Rede pública'},

                # Adicione mais opções de raça conforme necessário
            ],
            value=['Rede pública', 'Rede privada','Não aplicável'],  # Valores padrão
            labelStyle={'display': 'block'}
        ),
    ], style={'display': 'inline-block', 'width': '10%', 'border': '1px solid #000', 'padding': '10px','margin-right': '10px'}),
    
    
    # Filtro de Sexo com borda
    html.Div([
        html.Label('Sexo:', style={'font-weight': 'bold', 'font-size': '16px'}),
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
        html.Label('Raça:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Checklist(
            id='filter-race',
            options=[
                {'label': 'Branca', 'value': 'Branca'},
                {'label': 'Preta', 'value': 'Preta'},
                {'label': 'Parda', 'value': 'Parda'},
                {'label': 'Amarela', 'value': 'Amarela'},
                {'label': 'Indígena', 'value': 'Indígena'},
                {'label': 'Ignorado', 'value': 'Ignorado'},
                
            ],
            value=['Branca', 'Preta', 'Parda','Amarela', 'Indígena', 'Ignorado'],  
            labelStyle={'display': 'block'}
        ),
    ], style={'display': 'inline-block', 'width': '10%', 'border': '1px solid #000', 'padding': '10px','margin-right': '10px'}),
    
    # Filtro de idade
    html.Div([
        html.Label('Idade:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.RangeSlider(
            id='age-slider',
            min=0,
            max=107,
            step=1,
            value=[0, 110], 
            marks={i: str(i) if i % 10 == 0 else '' for i in range(0, 110)},
            
        ),
    ], style={'width': '95%', 'margin': 'auto', 'padding': '20px','margin-top':'20px', 'margin-bottom':'20px'}),
    
    
    # Caixas com somatorio da familia, media de pessoas por familia e numero maximo de pessoas
    html.Div([
        html.Label('NAF', style={'font-weight': 'bold', 'font-size': '20px', 'word-break': 'break-word'}),
        html.P('Número de Agrupamentos Familiares', style={'font-weight': 'bold', 'font-size': '10px', 'word-break': 'break-word'}),
        html.Div(id='output-agrupamentos', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'width': '160px', 'height': '160px', 'border': '1px solid black', 'font-size': '50px',  'margin-top': '10px'})
    ], style={'display': 'inline-block', 'margin-right': '15px'}),
    
    html.Div([
    html.Label('NMPF', style={'font-weight': 'bold', 'font-size': '20px', 'word-break': 'break-word'}),
    html.P('Número médio de pessoas por familia', style={'font-weight': 'bold', 'font-size': '10px', 'word-break': 'break-word'}),
    html.Div(id='output-agrupamentos2', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'width': '160px', 'height': '160px', 'border': '1px solid black', 'font-size': '50px',  'margin-top': '10px'})
        ], style={'display': 'inline-block','margin-right': '15px'}), 
    
    html.Div([
    html.Label('VMPF:', style={'font-weight': 'bold', 'font-size': '20px', 'word-break': 'break-word'}),
    html.P('Valor máximo de pessoas por familia', style={'font-weight': 'bold', 'font-size': '10px', 'word-break': 'break-word'}),
    html.Div(id='output-agrupamentos3', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'width': '160px', 'height': '160px', 'border': '1px solid black', 'font-size': '50px',  'margin-top': '10px'})
        ], style={'display': 'inline-block','margin-right': '15px'}),


    # Gráfico
    dcc.Graph(
    id='bar-plot',
    style={'height': '700px'}  # Ajuste a altura conforme necessário
    )

])

# Callback das mudanças de filtros 

@app.callback(
    [Output('output-agrupamentos', 'children'),
    Output('output-agrupamentos2', 'children'),
    Output('output-agrupamentos3', 'children'),
    Output('bar-plot', 'figure')],
   [Input('filter-estado', 'value'),
     Input('filter-sex', 'value'),
     Input('filter-race', 'value'),
     Input('filter-domicilio', 'value'),
     Input('age-slider', 'value')]
)


def update_box(selected_estado, selected_sex, selected_race, selected_domicilio, selected_age):
    if not selected_estado:  # Verifica se a lista de estados selecionados está vazia
        calculated_value1 = 0  # Define os valores como 0 se nenhum estado estiver selecionado
        calculated_value2 = 0
        calculated_value3 = 0
    else:
        filtered_df = df[df['Estado'].isin(selected_estado) & df['Sexo'].isin(selected_sex) & df['Raça'].isin(selected_race) & df['Rede Escolar'].isin(selected_domicilio) & ((df['Idade'] >= selected_age[0]) & (df['Idade'] <= selected_age[1]))]
        calculated_value1 = filtered_df['Identificação por domicilio'].nunique()
        calculated_value2 = round(filtered_df['N. Pessoas por domicilio'].mean())  # Coloque aqui a média das pessoas por família
        calculated_value3 = filtered_df['N. Pessoas por domicilio'].max()  # Coloque aqui o valor máximo de pessoas por família

    counts_sex = filtered_df['Sexo'].value_counts()
    male_count = counts_sex.get('Homem', 0)
    female_count = counts_sex.get('Mulher', 0)
    
    counts_race = filtered_df['Raça'].value_counts()
    parda_count = counts_race.get('Parda', 0)
    branca_count = counts_race.get('Branca', 0)
    preta_count = counts_race.get('Preta', 0)
    amarela_count = counts_race.get('Amarela', 0)
    indigena_count = counts_race.get('Indígena', 0)
    ignorado_count = counts_race.get('Ignorado', 0)
    
    counts_sabe_ler = filtered_df['Rede Escolar'].value_counts()
    sim_count = counts_sabe_ler.get('Rede privada', 0)
    nao_count = counts_sabe_ler.get('Rede pública', 0)
    naoaplica_count = counts_sabe_ler.get('Não aplicável', 0)

    counts_escola = filtered_df['Frequenta escola'].value_counts()
    esc_sim_count = counts_escola.get('Sim', 0)
    esc_nao_count = counts_escola.get('Não', 0)
    esc_naoaplica_count = counts_escola.get('Não aplicável', 0)
    
    
    fig = go.Figure(data=[
        go.Bar(
            name='Homens',
            x=['Sexo'],
            y=[male_count],
            marker=dict(color='SteelBlue')
        ),
        go.Bar(
            name='Mulheres',
            x=['Sexo'],
            y=[female_count],
            marker=dict(color='DarkViolet')
        ),
        
        go.Bar(
            name='Preta',
            x=['Raça'],
            y=[preta_count],
            marker=dict(color='GoldenRod')
        ),
        go.Bar(
            name='Parda',
            x=['Raça'],
            y=[parda_count],
            marker=dict(color='Indigo')
        ),  
        go.Bar(
            name='Branca',
            x=['Raça'],
            y=[branca_count],
            marker=dict(color='DarkMagenta')
        ),
        go.Bar(
            name='Amarela',
            x=['Raça'],
            y=[amarela_count],
            marker=dict(color='DarkOliveGreen')
        ),  
        go.Bar(
            name='Indígena',
            x=['Raça'],
            y=[indigena_count],
            marker=dict(color='DarkOrange')
        ),
        go.Bar(
            name='Ignorado',
            x=['Raça'],
            y=[ignorado_count],
            marker=dict(color='FireBrick')
        ),        
        go.Bar(
            name= 'Rede privada',
            x=['Rede Escolar'],
            y=[sim_count],
            marker=dict(color='LightSeaGreen')
        ),  
        go.Bar(
            name='Rede pública',
            x=['Rede Escolar'],
            y=[nao_count],
            marker=dict(color='Olive')
        ),
        go.Bar(
            name='Não aplicável',
            x=['Rede Escolar'],
            y=[naoaplica_count],
            marker=dict(color='RoyalBlue')
        ),
        go.Bar(
            name='Sim',
            x=['Frequenta escola'],
            y=[esc_sim_count],
            marker=dict(color='SaddleBrown')
        ),  
        go.Bar(
            name='Não',
            x=['Frequenta escola'],
            y=[esc_nao_count],
            marker=dict(color='Sienna')
        ),
        go.Bar(
            name='Não aplicável',
            x=['Frequenta escola'],
            y=[esc_naoaplica_count],
            marker=dict(color='DarkTurquoise')
        )
    ])
    # Atualizar caracteristicas do grafico apresentado
    fig.update_layout(
        barmode='stack',
        xaxis_title='Categorias',
        yaxis_title='Contagem',
        showlegend=True,
        legend=dict(
            font=dict(
                size=16,
            ),
        ),
        xaxis=dict(
            title='Categorias',
            title_font=dict(size=18),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title='Contagem',
            title_font=dict(size=18),
            tickfont=dict(size=16)
        )
    )

    
    return f"{calculated_value1}", f"{calculated_value2}", f"{calculated_value3}", fig 

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, port=8060)
