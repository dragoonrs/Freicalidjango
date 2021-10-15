import json

from datetime import datetime

def read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data

def read_json(path):
    return json.loads(read_file(path))

def write_json(path, data):
     return write_file(path, json.dumps(data))

def write_file(path, data):
   file = open(path, "w")
   file.write(str(data))
   file.close()
   return data

def openJuroComposto(data):
    return json.loads(data)

def igpmAcumulado(inicio, fim):
    return 1.0

def meses(inicio, fim):
    d = ((fim.year - inicio.year) * 12) + (fim.month - inicio.month)
    if d < 0:
            d = 0
    return d

def calcLine(juroMes, multa, honorarios, dataCalculo, dataDivida, valorDevido):
        linha = [0,0,0,0,0,0]
        linha[0] = valorDevido*(multa/100);
        linha[1] = igpmAcumulado(dataDivida, dataCalculo);
        linha[2] = (valorDevido + linha[0])*linha[1]
        linha[3] = (valorDevido + linha[0]) * ((pow(1+(juroMes/100), meses(dataDivida, dataCalculo)))-1)
        linha[4] = (valorDevido + linha[0] + linha[3])*((honorarios/100))
        linha[5] = linha[0] + linha[2] + linha[3] + linha[4]
        return linha

