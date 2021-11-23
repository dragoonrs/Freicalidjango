from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from .models import igpm
from django.template import loader
from django.shortcuts import get_object_or_404,render
from django.http import Http404
from django.urls import reverse
from decimal import Decimal
from django.views import generic
import json
from juroComposto.uteis import openJuroComposto, calcLine, gerarJsonVazio
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from datetime import datetime
from dateutil import parser

def list(request):
    latest_igpm_list = igpm.objects.order_by('-data')[:5]
    output = ', <BR>'.join([q.data.strftime("%B %Y") for q in latest_igpm_list])
    return HttpResponse(output)

#def index(request):
#    latest_igpm_list = igpm.objects.order_by('-data')[:5]
#    context = {'latest_igpm_list': latest_igpm_list,}
#    return render(request, 'juroComposto/index.html', context)

class IndexView(generic.ListView):
    template_name = 'juroComposto/index.html'
    context_object_name = 'latest_igpm_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return igpm.objects.order_by('-data')

def atualizacao(request):
    if 'upload' in request.FILES:
        tempo = request.FILES['upload']
        jct = openJuroComposto(tempo.read())
        juroMes = float(jct['juroMes'])
        multa = float(jct['multa'])
        hono = float(jct['honorarios'])
        dc = parser.parse(jct['dataCalculo'])

        for linha in jct['Linhas']:
            try:
                valorD = float(linha['valorDevido'])
                dataD = parser.parse(linha['dataDivida'])
                cdo = calcLine(juroMes, multa, hono, dc, dataD, valorD)
                linha['multa'] = cdo[0]
                linha['igpmAcumulado'] = cdo[1]
                linha['correcao'] = cdo[2]
                linha['juros'] = cdo[3]
                linha['honorarios'] = cdo[4]
                linha['total'] = cdo[5]
            except:
                del (jct['Linhas'][jct['Linhas'].index(linha)])
    elif request.POST.get('upload'):
        tempo = request.POST.get('upload')
        jct = openJuroComposto(tempo)
        juroMes = float(jct['juroMes'])
        multa = float(jct['multa'])
        hono = float(jct['honorarios'])
        dc = parser.parse(jct['dataCalculo'])
        for linha in jct['Linhas']:
            try:
                valorD = float(linha['valorDevido'])
                dataD = parser.parse(linha['dataDivida'])
                cdo = calcLine(juroMes, multa, hono, dc, dataD, valorD)
                linha['multa'] = cdo[0]
                linha['igpmAcumulado'] = cdo[1]
                linha['correcao'] = cdo[2]
                linha['juros'] = cdo[3]
                linha['honorarios'] = cdo[4]
                linha['total'] = cdo[5]
            except:
                del (jct['Linhas'][jct['Linhas'].index(linha)])
    else:
        jct = gerarJsonVazio()
    return render(request, 'juroComposto/atualizacao.html', {'jct':jct})


class DetailView(generic.DetailView):
    model = igpm
    template_name = 'juroComposto/detail.html'

def updateIgpm(request, igpm_id):
    igpmt = get_object_or_404(igpm, pk=igpm_id)
    try:
        newTaxa = Decimal(request.POST['taxa'])
        print(request.POST['taxa'])
        print(newTaxa)
    except Exception as e:
        # Redisplay the question voting form.
        return render(request, 'juroComposto/detail.html', {
            'igpm': igpmt,
            'error_message': "Valor nao numerico",
        })
    else:
        igpmt.taxa = newTaxa
        igpmt.multiplicadorAbsoluto = 1 + (newTaxa/100)
        igpmt.save()
        return HttpResponseRedirect(reverse('juroComposto:index'))

def juroCompostoTable(request):
    tempo = request.FILES['upload']
    jct = openJuroComposto(tempo.read())
    juroMes = jct['juroMes']
    multa = jct['multa']
    hono = jct['honorarios']
    dc = parser.parse(jct['dataCalculo'])
    for linha in jct['Linhas']:
        valorD = linha['valorDevido']
        dataD = parser.parse(linha['dataDivida'])
        cdo = calcLine(juroMes, multa, hono, dc, dataD, valorD)
        linha['multa'] = cdo[0]
        linha['igpmAcumulado'] = cdo[1]
        linha['correcao'] = cdo[2]
        linha['juros'] = cdo[3]
        linha['honorarios'] = cdo[4]
        linha['total'] = cdo[5]
    return JsonResponse(jct)

def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        #fss = FileSystemStorage()
        #file = fss.save(upload.name, upload)
        #file_url = fss.url(file)
        return render(request, 'atualizacao/', {'data': upload})
    return render(request, 'juroComposto/upload.html')

def imprimir(request):
    if request.POST.get('uploadp'):
        tempo = request.POST.get('uploadp')
        jct = openJuroComposto(tempo)
        juroMes = float(jct['juroMes'])
        multa = float(jct['multa'])
        hono = float(jct['honorarios'])
        dc = parser.parse(jct['dataCalculo'])
        for linha in jct['Linhas']:
            try:
                valorD = float(linha['valorDevido'])
                dataD = parser.parse(linha['dataDivida'])
                cdo = calcLine(juroMes, multa, hono, dc, dataD, valorD)
                linha['multa'] = cdo[0]
                linha['igpmAcumulado'] = cdo[1]*100
                linha['correcao'] = cdo[2]
                linha['juros'] = cdo[3]
                linha['honorarios'] = cdo[4]
                linha['total'] = cdo[5]
            except:
                del (jct['Linhas'][jct['Linhas'].index(linha)])
    else:
        jct = gerarJsonVazio()
    return render(request, 'juroComposto/imprimir.html', {'jct':jct})

def main(request):
    return render(request, 'juroComposto/main.html')

def splash(request):
    return render(request, 'juroComposto/splash.html')