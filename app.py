import numpy as np
import streamlit as st
import math
from sklearn.linear_model import LinearRegression
from PIL import Image, ImageOps

# Carregar a imagem local e redimensioná-la
img = Image.open("tabela_furacao.png")
img = img.resize((300, 300))  # Reduzir o tamanho da imagem
img = ImageOps.expand(img, border=5, fill='#006494')  # Adicionar uma moldura com cor da paleta

# Dados da tabela (largura da mesa b/bf e gabarito usual na mesa g)
larguras_mesa = np.array([85, 88, 102, 104, 118, 122, 133, 136]).reshape(-1, 1)
gabarito_mesa = np.array([50, 50, 58, 58, 70, 70, 76, 76])

# Treinando o modelo de regressão linear
model = LinearRegression()
model.fit(larguras_mesa, gabarito_mesa)

# Função para prever o valor
def prever_gabarito(bf):
    bf = np.array([[bf]])
    previsao = model.predict(bf)
    g = math.ceil(previsao[0])
    return g, previsao[0] / 2

# Interface Streamlit
st.set_page_config(page_title='Interpolador de Gabarito', page_icon='📏', layout='wide', initial_sidebar_state='collapsed')

# Estilo personalizado com detecção de tema
st.markdown(
    """
    <style>
    .stApp {
        background-color: var(--background-color);
    }
    .stMarkdown h1, .css-1d391kg p {
        color: var(--text-color);
    }
    .css-18e3th9 {
        padding-top: 3rem;
    }
    .css-1d391kg p {
        font-size: 18px;
        color: #13293D;
    }
    .stButton button {
        background-color: #1B98E0;
        color: #000000;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #247BA0;
    }
    .highlight-result {
        font-size: 32px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #1B98E0;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        text-align: center;
    }
    .highlight-gabarito {
        font-size: 28px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #006494;
        padding: 10px;
        border-radius: 8px;
        margin-top: 20px;
        text-align: center;
    }
    .highlight-eixo {
        font-size: 28px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #1B98E0;
        padding: 10px;
        border-radius: 8px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
    <script>
    const darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (darkMode) {
        document.documentElement.style.setProperty('--background-color', '#13293D');
        document.documentElement.style.setProperty('--text-color', '#FFFFFF');
    } else {
        document.documentElement.style.setProperty('--background-color', '#E8F1F2');
        document.documentElement.style.setProperty('--text-color', '#000000');
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Título da página
st.title('Interpolador de Gabarito de Furação', help='')

# Layout com duas colunas
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    # Entrada do usuário para a largura da mesa (b ou bf)
    bf_input = st.number_input('Digite a largura da mesa (b ou bf) em mm:', min_value=1, step=1, key='largura_input')

    # Botão para calcular
    if st.button('Calcular Gabarito', key='calcular_button'):
        resultado, distancia_entre_eixos = prever_gabarito(bf_input)
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown(f'<div class="highlight-gabarito">Gabarito usual (g): <strong>{resultado} mm</strong></div>', unsafe_allow_html=True)
        with res_col2:
            st.markdown(f'<div class="highlight-eixo">Distância entre eixos: <strong>{distancia_entre_eixos:.1f} mm</strong></div>', unsafe_allow_html=True)

with col2:
    # Mostrar a imagem
    st.image(img, caption='Referência', use_column_width=True)