import json
from .models import igpm
import decimal

import datetime

from dateutil import parser

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
    dataInicio = datetime.date(inicio.year, inicio.month, 1)
    dataFim = datetime.date(fim.year, fim.month, 2)
    taxaFinal = decimal.Decimal(1.0)
    for taxas in igpm.objects.order_by('data').filter(data__range=(dataInicio, dataFim)):
            taxaFinal = taxas.multiplicadorAbsoluto * taxaFinal
    return float(taxaFinal) - 1.0

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

def gerarJsonVazio():
    dados = {	"juroMes": 0,	"multa": 10,	"honorarios": 10,	"dataCalculo": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %z'), 'lihas':[]}
    return json.dumps(dados)