# Criando uma API com FastAPI v1.0

O objetivo deste projeto é criar uma API com FastAPI para servir como base para outros projetos.
Ela será uma API básica, com o objetivo de apresentar como criar uma API com FastAPI. Ela será deployada em um container Docker.

## Requisitos

- Python 3.8
- FastAPI
- Uvicorn
- Docker

## Recomendação de Leitura

- [Tutorial de FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Concurrency and async](https://fastapi.tiangolo.com/async/#in-a-hurry)

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
C:\Users\usuario\Documents\criando-uma-api-fastapi-basic\Scripts\python.exe
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

Como apresentado na [documentação](https://fastapi.tiangolo.com/), para criar uma API com FastAPI, é necessário criar um arquivo para ser o ponto de entrada para a aplicação. Sugere-se a criação de um arquivo ***main.py***, com o seguinte conteúdo:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

O que está acontecendo aqui é o seguinte:
- Importamos a classe FastAPI do pacote fastapi
- Criamos uma instância da classe FastAPI
- Criamos uma rota para a aplicação, que é a rota raiz, ou seja, a rota que será acessada quando a aplicação for executada
- A rota criada é do tipo GET, ou seja, ela é acessada quando o método GET é executado
- A rota criada é assíncrona, ou seja, ela é executada de forma assíncrona
- A rota criada retorna uma mensagem em formato JSON

Para executar a aplicação, execute o comando abaixo:

```bash
uvicorn main:app --reload
```

Desta forma, quando a aplicação estiver rodando, vamos ter a seguinte saída:

```bash	
INFO:     Will watch for changes in these directories: ['<Onde você clonou a aplicação>\\Templates-Desenvolvimento\\criando-uma-api-fastapi-basic']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [18584] using StatReload
INFO:     Started server process [13460]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Para acessar a aplicação, basta acessar o endereço http://127.0.0.1:8000. A saída esperada é a seguinte:

```json
{"message":"Hello World"}
```

É possível acessar a documentação da API, acessando o endereço http://127.0.0.1:8000/docs. A saída esperada é a seguinte:

<img src="./media/saida_docs.png" alt="Documentação da API" style="height: 100%; width:100%; flex:1"/>

Para controlar a execução da aplicação, podemos enviar alguns parâmetros para a execução da aplicação. Por exemplo, para executar a aplicação em modo de produção, podemos executar o comando abaixo:

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

Assim, controlamos a execução da aplicação, e podemos executar a aplicação em modo de produção, por exemplo.
Vamos adicionar agora mais rotas para a aplicação, para exemplificar como criar rotas com parâmetros. O arquivo ***main.py*** ficará da seguinte forma:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/somar/{numero1}/{numero2}")
async def somar(numero1: int, numero2: int):
    return {"resultado": numero1 + numero2}

@app.get("/subtrair/{numero1}/{numero2}")
async def subtrair(numero1: int, numero2: int):
    return {"resultado": numero1 - numero2}

@app.get("/multiplicar/{numero1}/{numero2}")
async def multiplicar(numero1: int, numero2: int):
    return {"resultado": numero1 * numero2}

@app.get("/dividir/{numero1}/{numero2}")
async def dividir(numero1: int, numero2: int):
    try:
        return {"resultado": numero1 / numero2}
    except:
        return {"resultado": "Não é possível dividir por zero."}
```

Para testar a aplicação, vamos utilizar o plugin Thunder Client, do VSCode. Para instalar, basta acessar o menu de extensões do VSCode, e pesquisar por ***Thunder Client***. A saída esperada é a seguinte:


