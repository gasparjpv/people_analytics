import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import circlify
import matplotlib.pyplot as plt
import matplotlib
from dash.exceptions import PreventUpdate
matplotlib.use('Agg')
import io
import base64
import dash_bootstrap_components as dbc

# Carregar os dados
df = pd.read_csv('dados_selecionados-app3.csv')

# Estados a serem usados no DIV
UF = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás',
      'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco',
      'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina',
      'São Paulo', 'Sergipe', 'Tocantins']

UF2 = ['Distrito Federal','Rio de Janeiro','Santa Catarina', 'São Paulo']

df['Idade'] = df['Idade'].astype(int)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout do aplicativo com bordas nas caixas de filtro
app.layout = html.Div([
    html.Div([
        html.Img(src='assets/ft.png',style={'width': '100px', 'height': '100px', 'display': 'inline-block', 'margin-left': '10px'}),
        html.Img(src='assets/unicamp.png',style={'width': '100px', 'height': '100px', 'display': 'inline-block', 'position': 'absolute', 'right': '10px'}),

    ]),
    html.H1('Dashboard gênero e raça'),
    html.P('Análise de indicadores relacionados ao responsável pela unidade familiar'),

    html.Div([
        html.Label('Unidade Federativa:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.Dropdown(
            id='filter-estado',
            options=[{'label': estado, 'value': estado} for estado in UF],
            multi=True,
            value=UF2,  # Valores padrão
            style={'display': 'block', 'height': '10%', 'margin-top': '20px', 'margin-bottom': '20px'}
        )
    ]),

    # Filtro de idade
    html.Div([
        html.Label('Idade:', style={'font-weight': 'bold', 'font-size': '16px'}),
        dcc.RangeSlider(
            id='age-slider',
            min=0,
            max=107,
            step=1,
            value=[0, 110],  # Valor padrão (intervalo completo)
            marks={i: str(i) if i % 10 == 0 else '' for i in range(0, 110)},

        ),
    ], style={'width': '95%', 'margin': 'auto', 'padding': '20px', 'margin-top': '20px', 'margin-bottom': '20px'}),

    # Gráfico
    html.Div(id='graph-container', style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'wrap'})
])

# Callback para atualizar os gráficos com base nos estados selecionados
@app.callback(
    Output('graph-container', 'children'),
    [Input('filter-estado', 'value'),
     Input('age-slider', 'value')]
)
def update_graphs(selected_estado, selected_age):
    # Se nenhum estado estiver selecionado, retorna sem atualizar
    if not selected_estado:
        raise PreventUpdate  # Define os valores como 0 se nenhum estado estiver selecionado

    graphs = []
    pair = []
    row = []
    counter = 0
    
    for i, estado in enumerate(selected_estado):
        if i % 2 == 0 and i != 0:
            graphs.append(html.Div(row, className='row'))
            row = []
        
    for estado in selected_estado:
        filtered_df = df[(df['Estado'] == estado) & ((df['Idade'] >= selected_age[0]) & (df['Idade'] <= selected_age[1]))]

        count_homem = ((filtered_df['Sexo'] == 'Homem')).sum()
        count_mulher = ((filtered_df['Sexo'] == 'Mulher')).sum()
        count_mulher_raca = ((filtered_df['Sexo'] == 'Mulher') & (filtered_df['Raça'] == 'Branca')).sum()
        count_mulher_raca1 = ((filtered_df['Sexo'] == 'Mulher') & (filtered_df['Raça'] == 'Preta/Parda')).sum()
        count_mulher_raca2 = ((filtered_df['Sexo'] == 'Mulher') & (filtered_df['Raça'] == 'Outros')).sum()
        count_homem_raca = ((filtered_df['Sexo'] == 'Homem') & (filtered_df['Raça'] == 'Branca')).sum()
        count_homem_raca1 = ((filtered_df['Sexo'] == 'Homem') & (filtered_df['Raça'] == 'Preta/Parda')).sum()
        count_homem_raca2 = ((filtered_df['Sexo'] == 'Homem') & (filtered_df['Raça'] == 'Outros')).sum()

        total = count_homem + count_mulher
        total2 = count_mulher_raca + count_mulher_raca1 + count_mulher_raca2 + count_homem_raca + count_homem_raca1 + count_homem_raca2

        data = [
            {
                'id': estado, 'datum': total,
                'children': [
                    {'id': "Homem", 'datum': count_homem, 'children': [
                        {'id': 'Branca', 'datum': count_homem_raca},
                        {'id': 'Preta/Parda', 'datum': count_homem_raca1},
                        {'id': 'Outros', 'datum': count_homem_raca2}
                    ]},
                    {'id': "Mulher", 'datum': count_mulher, 'children': [
                        {'id': 'Branca', 'datum': count_mulher_raca},
                        {'id': 'Preta/Parda', 'datum': count_mulher_raca1},
                        {'id': 'Outros', 'datum': count_mulher_raca2}
                    ]}
                ]
            }
        ]

        circles = circlify.circlify(
            data,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )

        with io.BytesIO() as buf:
            fig, ax = plt.subplots(figsize=(6.5,5))  # Aumentar o tamanho da figura

            # Title
            #ax.set_title(f'Repartição por estado: {estado}')

            # Todos os estados 
            ax.axis('off')
            for circle in circles:
                if circle.r > 0:  # Verificação para garantir que o raio é maior que zero
                    if circle.level == 1:
                        x, y, r = circle
                        #label = circle.ex["id"]
                        ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=0.1, color="#8B0000"))
                        #plt.annotate(label, (x, y), ha='center', color="white")

            lim = max(
                max(
                    abs(circle.x) + circle.r,
                    abs(circle.y) + circle.r,
                )
                for circle in circles
            )
            plt.xlim(-lim, lim)
            plt.ylim(-lim, lim)

            #estado 
            for circle in circles:
                
                if circle.level == 1:
                    x, y, r = circle
                    label = circle.ex["id"]
                    
                if circle.level == 2:
                    x, y, r = circle
                    label = circle.ex["id"]
                    ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=0.1, color="#800080"))
                    bbox_props = dict(boxstyle="round,pad=0.1", fc="white", ec="black", lw=0.1)
                    ax.text(x, y, label, ha='center', va='center', color='black', bbox=bbox_props)
                    #plt.annotate(label, (x, y), ha='center', color="white", fontsize=10)

                if circle.level == 3:
                    x, y, r = circle
                    label = circle.ex["id"]
                    ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=0.1, color="#008080"))
                    #plt.annotate(label, (x, y), ha='center', color="white")
                    plt.annotate(label, (x, y), ha='center', color="white", fontsize=9, rotation=45,fontweight='bold')

                #Caso tenha mais um nivel, segue a seguinte logica 
                #if circle.level == 4:
                #    x, y, r = circle
                #    label = circle.ex["id"]
                #    ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=1, color="tomato"))
                #    #plt.annotate(label, (x, y), ha='center', color="white")
                #    #plt.annotate(label, (x, y - 1.5 * r), ha='center', color="white")

            # Salvar a figura
            plt.savefig(buf, format="png")
            buf.seek(0)
            data = base64.b64encode(buf.read()).decode()

            # Fechar a figura
            plt.close()

            # Adicionar gráfico à lista de gráficos
        
            graphs.append(html.Div([
            html.H2(f'{estado}'),
            html.Img(src='data:image/png;base64,{}'.format(data))
        ]))

    return graphs


# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=False, port=8070)
