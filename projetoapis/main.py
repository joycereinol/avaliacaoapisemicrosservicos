from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime

# Criar a instância da aplicação FastAPI
app = FastAPI()

# Lista para armazenar os clientes da fila (como exemplo)
fila = []

# Função para gerar uma posição única
def get_next_position():
    return len(fila) + 1

# Endpoint GET /fila
@app.get("/fila")
async def get_fila():
    if len(fila) == 0:
        return []
    return [{"posicao": i+1, "nome": cliente["nome"], "data_chegada": cliente["data_chegada"]} for i, cliente in enumerate(fila)]

# Endpoint GET /fila/{id}
@app.get("/fila/{id}")
async def get_cliente(id: int):
    if id < 1 or id > len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    cliente = fila[id - 1]  # Ajustando o índice (começa de 0)
    return {"posicao": id, "nome": cliente["nome"], "data_chegada": cliente["data_chegada"]}

# Endpoint POST /fila
@app.post("/fila")
async def adicionar_cliente(nome: str, tipo_atendimento: str):
    if len(nome) > 20:
        raise HTTPException(status_code=400, detail="Nome deve ter no máximo 20 caracteres.")
    if tipo_atendimento not in ["N", "P"]:
        raise HTTPException(status_code=400, detail="Tipo de atendimento deve ser 'N' ou 'P'.")
    
    # Adicionar cliente à fila
    cliente = {
        "nome": nome,
        "tipo_atendimento": tipo_atendimento,
        "data_chegada": datetime.now().isoformat(),
        "atendido": False
    }
    
    fila.append(cliente)
    
    return {"message": f"Cliente {nome} adicionado à fila.", "posicao": get_next_position()}

# Endpoint PUT /fila
@app.put("/fila")
async def atualizar_fila():
    if len(fila) > 0:
        # Atualizar a posição dos clientes
        for i in range(len(fila)):
            if i == 0:
                fila[i]["atendido"] = True
        return {"message": "Fila atualizada."}
    else:
        raise HTTPException(status_code=404, detail="Não há clientes na fila para atualizar.")

# Endpoint DELETE /fila/{id}
@app.delete("/fila/{id}")
async def remover_cliente(id: int):
    if id < 1 or id > len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    # Remover cliente da fila
    fila.pop(id - 1)
    
    # Reorganizar a fila
    for i in range(len(fila)):
        fila[i]["posicao"] = i + 1
    
    return {"message": f"Cliente na posição {id} removido da fila."}
