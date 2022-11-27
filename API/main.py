from fastapi import FastAPI, Request
import datetime
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


lst = []


class Item(BaseModel):
    nome: str
    data: datetime.datetime
    local: int = 0
    tipo: str
    cli: bool

    def __init__(self, **args):
        super().__init__(
            local=0 if len(lst) == 0 else lst[len(lst) - 1].local + 1, **args
        )


#

persona0 = Item(nome="hector", cli=False, data=datetime.datetime.now(), tipo="N")

lst.append(persona0)


persona1 = Item(nome="zito", cli=False, data=datetime.datetime.now(), tipo="P")

lst.append(persona1)


persona2 = Item(nome="martinez", cli=False, data=datetime.datetime.now(), tipo="N")

lst.append(persona2)

#


def pegPer(local):
    persona = None
    for i in lst:
        if i.local == local:
            persona = i
    return persona


def lstNew(inicio):
    for i in range(inicio, len(lst)):
        lst[i].local = lst[i].local - 1
        if lst[i].local == 0:
            lst[i].cli == True


# endpoints


@app.get("/fila")
async def get_lista():
    return [{"nome": se.nome, "data": se.data, "local": se.local} for se in lst]


@app.get("/fila/{id}")
async def aux(id):
    persona = pegPer(int(id))
    if persona == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma pessoa na posição especificada",
            headers={"X-Error": "There goes my error"},
        )
    persona1 = {"nome": persona.nome, "data": persona.data, "local": persona.local}
    return persona1


@app.post("/fila")
async def agrPost(dados: Item):
    print(dados)
    if dados.nome != None and len(dados.nome) > 20:
        return "O campo nome é obrigatório e deve ter no máximo 20 caracteres"
    if dados.tipo not in ["N", "n", "P", "p"]:
        return "O campo tipo de atendimento só aceita 1 caractere (N ou P)"
    lst.append(dados)
    return dados


@app.put("/fila")
async def new():
    lstNew(0)
    return "Atualizado"


@app.delete("/fila/{id}")
async def retirar(id):
    persona = pegPer(int(id))
    print(persona)
    if persona == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não localizado na posição especificada",
        )
    index = lst.index(persona)
    lst.remove(persona)
    lstNew(index)
    return " ### OK ### "
