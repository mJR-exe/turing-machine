# -*- coding: utf-8 -*-

import optparse
from collections import defaultdict
from copy import deepcopy


def transicao(fitasQtd, estadoAtual):
    palavra = ''
    for estado, fitas, index in estadoAtual:
        palavra += estado+' - '
        for i in range(fitasQtd):
            tr = fitas[i][:]
            tr.insert(index[i]+1, ']')
            tr.insert(index[i], '[')
            palavra += ''.join(tr) + '\t\t'
        palavra += '\n'
    return palavra


def run(arquivo, palavra):
    tm, delta = open(arquivo), defaultdict(list)
    tm.readline()
    tm.readline()
    fitasQtd = len(tm.readline().split('-')[0].split())-1
    tm.seek(0)
    estado, final = tm.readline().split()[1], tm.readline().split()[1:]
    [delta[tuple(i.split()[:fitasQtd+1])].append(i.split()
                                                 [fitasQtd+2:]) for i in tm]
    fitas = [list(palavra)]
    for i in range(fitasQtd-1):
        fitas.append(['_'])
    index = [0 for i in range(fitasQtd)]
    shift = ['S' for i in range(fitasQtd)]
    estadoAtual = [(estado, fitas, index)]
    while(estadoAtual != []):
        newDescriptions = []
        for estado, fitas, index in estadoAtual:
            t = [estado]
            for i in range(fitasQtd):
                t.append(fitas[i][index[i]])
            for deltaOption in delta[tuple(t)]:
                newState = deltaOption[0]
                novaTransicao = deepcopy(fitas)
                newIndex = deepcopy(index)
                for i in range(fitasQtd):
                    novaTransicao[i][newIndex[i]] = deltaOption[i+1]
                    shift[i] = deltaOption[i+1+fitasQtd]

                for i in range(fitasQtd):
                    if newIndex[i] == 0:
                        novaTransicao[i].insert(0, '_')
                        newIndex[i] += 1
                    if newIndex[i] == len(novaTransicao[i])-1:
                        novaTransicao[i].append('_')

                    if shift[i] == 'L':
                        newIndex[i] -= 1
                    if shift[i] == 'R':
                        newIndex[i] += 1
                newDescriptions.append((newState, novaTransicao, newIndex))
        estadoAtual = newDescriptions
    return False


parser = optparse.OptionParser(
    "%prog -f nomeDoArquivo palavra1 palavra2 (opcional)")
parser.add_option("-f", "--file", dest="f", type="string")
(options, args) = parser.parse_args()

if len(args) < 1:
    parser.print_help()
for palavra in args:
    if run(options.f, palavra):
        print("Aceita.")
        print
    else:
        print("Não aceita.")
        print
