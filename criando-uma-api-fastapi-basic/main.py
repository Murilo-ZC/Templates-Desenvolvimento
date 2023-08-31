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