# 📊 Criando visualizações de dados com o Streamlit v1.0

O objetivo deste projeto é criar e deployar uma aplicação web utilizando o Streamlit para realizar a visualização dos dados. O Streamlit é uma biblioteca que permite a criação de aplicações web de forma simples e rápida, utilizando apenas Python. Para mais informações, acesse o [link](https://streamlit.io/).
Os dados utilizados estão disponíveis nesse [link](https://www.kaggle.com/datasets/zernach/2018-airplane-flights).

<img src="./media/Streamlit_Logo_1.jpg" alt="Logo Streamlit" style="height: 100%; width:100%; flex:1"/>

## Requisitos

- Python >= 3.8
- Streamlit

## Recomendação de Leitura

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Streamlit - The fastest way to build custom ML tools](https://www.streamlit.io/)
- [Streamlit: Criando aplicações web | Live de Python #227](https://www.youtube.com/watch?v=Ie5ef_R_k6I)

## Instalação

As bibliotecas necessárias para a execução do projeto estão no arquivo `requirements.txt`. Para instalar, execute o comando abaixo:

```bash
python -m pip install -r requirements.txt
```

> ***ATENÇÃO:*** *É recomendado a utilização de um ambiente virtual para a instalação das bibliotecas. Para mais informações, acesse o [link](https://docs.python.org/pt-br/3/library/venv.html).*

Para criar um ambiente virtual, execute o comando abaixo (para Windows):

```bash
python -m venv .
cd Scripts
activate
```

O que vai acontecer com a sequencia de comandos acima, um ambiente virtual será criado na pasta atual. Em sequencia, navegamos para o diretório ***Scripts***, e ativamos o ambiente virtual executando o script ***activate***. Na sequencia, vamos avaliar se o ambiente virtual foi ativado corretamente, executando o comando abaixo:

```bash
where python
```

A saída esperada é a seguinte:

```bash
C:\Users\usuario\Documents\intro-streamlit\Scripts\python.exe
C:\Users\usuario\AppData\Local\Programs\Python\Python38\python.exe
```

Os diretórios que são criados para o ambiente virtual são:
- Include
- Lib
- Scripts

Esses diretórios e o arquivo ***pyvenv.cfg*** são criados na pasta onde o comando ***python -m venv .*** foi executado. Eles podem ser adicionados ao ***.gitignore***, pois se for necessário recriar esses diretórios, basta recriar o venv. Exemplo de gitignore:

```gitignore
Include
Lib
Scripts
pyvenv.cfg
```

Para desativar o ambiente virtual, execute o comando abaixo, dentro do diretório Scripts:

```bash
deactivate
```

## Desenvolvimento do Projeto

A criação da aplicação vai seguir o conceito de desenvolvimento do Streamlit, que é construir a aplicação uma linha de cada vez. Para isso, vamos criar um arquivo ***main.py*** na raiz do projeto, com o seguinte conteúdo:

```python
import streamlit as st

st.title('Hello World')

st.header("Visualização de Dados com Streamlit")
```

Agora para executar nossa aplicação, vamos utilizar o comando:

```bash
python -m streamlit run main.py
```

Quando a aplicação for executada pela primeira vez, a saída esperada é a seguinte:

```bash
python -m streamlit run main.py

      Welcome to Streamlit!

      If you’d like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank.

      Email:

  You can find our privacy policy at https://streamlit.io/privacy-policy

  Summary:
  - This open source library collects usage statistics.
  - We cannot see and do not store information contained inside Streamlit apps,
    such as text, charts, images, etc.
  - Telemetry data is stored in servers in the United States.
  - If you'd like to opt out, add the following to %userprofile%/.streamlit/config.toml,
    creating that file if necessary:

    [browser]
    gatherUsageStats = false


  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.68.117:8501
```

Se alterarmos agora o nosso código-fonte enquanto a aplicação estiver em execução, ela será atualizada automaticamente. Para isso, vamos adicionar mais algumas linhas de código ao nosso arquivo ***main.py***:

```python
import streamlit as st

st.title("Minha Aplicação com Streamlit")

st.header("Visualização de Dados com Streamlit")

st.subheader("Uma subseção")
```

O Steamlit permite que uma estrutura de páginas possa ser criada dentro da aplicação. Desta forma, é possível criar uma organização melhor para a aplicação. Para isso, vamos criar um diretório chamado ***pages*** na raiz do projeto. Dentro dele, vamos adicionar um arquivo chamado ***Removedor_de_Fundo.py***. Este arquivo foi inspirado na publicação do desenvolvedor [Eduardo Mendes (@Dunossauro)](https://www.youtube.com/@Dunossauro), em seu [vídeo](https://www.youtube.com/watch?v=Ie5ef_R_k6I) sobre o Streamlit. O conteúdo do arquivo é o seguinte:

```python
import streamlit as st
from PIL import Image
from rembg import remove


def remove_br(image, widget):
    bytes_data = Image.open(image)
    output = remove(bytes_data)
    widget.title("Imagem sem fundo")
    widget.image(output)


st.title("Carregando um arquivo")
image = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

# Cria duas colunas para a página
col_a, col_b = st.columns(2)

if image is not None:
    # Coloca a imagem na primeira coluna
    col_a.title("Imagem com fundo")
    col_a.image(image)

    st.button("Remover fundo", on_click=remove_br, args=(image, col_b))

# Código fonte utilizado para criar a imagem de fundo
with st.expander("Código fonte"):
    st.code(
    """
    import streamlit as st
    from PIL import Image
    from rembg import remove


    def remove_br(image, widget):
        bytes_data = Image.open(image)
        output = remove(bytes_data)
        widget.title("Imagem sem fundo")
        widget.image(output)


    st.title("Carregando um arquivo")
    image = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

    # Cria duas colunas para a página
    col_a, col_b = st.columns(2)

    if image is not None:
        # Coloca a imagem na primeira coluna
        col_a.title("Imagem com fundo")
        col_a.image(image)

        st.button("Remover fundo", on_click=remove_br, args=(image, col_b))
    """,
    language="python" 
    )
```

A seguinte saída será produzida:

<img src="./media/saida_removedor_fundo.png" alt="Logo Streamlit" style="height: 100%; width:100%; flex:1"/>

Agora vamos criar uma página para exibir nossos dados. Para isso, vamos criar um arquivo chamado ***Visualizacao_de_Dados.py*** dentro do diretório ***pages***. O conteúdo do arquivo é o seguinte:

```python
```

## Deploy

- TODO