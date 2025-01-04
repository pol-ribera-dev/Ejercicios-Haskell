from __future__ import annotations
from antlr4 import *
from exprsLexer import exprsLexer
from exprsParser import exprsParser
from exprsVisitor import exprsVisitor
import streamlit as st
import graphviz
from dataclasses import dataclass
import pandas as pd
import string


@dataclass
class Var:
    var: str
    tipe: str


@dataclass
class Appl:
    t1: Terme
    t2: Terme
    tipe: str


@dataclass
class Abst:
    cap: str
    cos: Terme
    tipe: str


Terme = Var | Appl | Abst


class TreeVisitor(exprsVisitor):
    def __init__(self):
        self.dic = {}

    def visitParentesis(self, ctx):
        [_, term, _] = list(ctx.getChildren())
        return self.visit(term)

    def visitDefinicions(self, ctx):
        [term, _] = list(ctx.getChildren())
        return self.visit(term), 0

    def visitTipos(self, ctx):
        lista = list(ctx.getChildren())
        lista_filtrada = [elem.getText()
                          for i, elem in enumerate(lista) if i % 2 == 0]
        return lista_filtrada

    def visitExpresions(self, ctx):
        [term, _] = list(ctx.getChildren())
        return self.visit(term), 1

    def visitAbstraccio(self, ctx: exprsParser.AbstraccioContext):
        [_, cap, _, cos] = list(ctx.getChildren())
        ca = Var(cap.getText(), "undef")
        co = self.visit(cos)
        ret = Abst(ca, co, "undef")
        return ret

    def visitAplicacio(self, ctx: exprsParser.AplicacioContext):
        [t1, t2] = list(ctx.getChildren())
        return Appl(self.visit(t1), self.visit(t2), "undef")

    def visitNumero(self, ctx: exprsParser.NumeroContext):
        [numero] = list(ctx.getChildren())
        return Var(numero.getText(), "undef")

    def visitId(self, ctx: exprsParser.IdContext):
        [ident] = list(ctx.getChildren())
        return Var(ident.getText(), "undef")

    def visitOperador(self, ctx: exprsParser.OperadorContext):
        [oper] = list(ctx.getChildren())
        return Var(oper.getText(), "undef")


def calcular_tipo(t, data, variables, tv):
    match t:
        case Var(s, tipe):
            try:
                return data[s]
            except KeyError:
                try:
                    return tv[variables[s]]
                except KeyError:
                    return None
        case Appl(b, c, tipe):
            tb = calcular_tipo(b, data, variables, tv)
            tc = calcular_tipo(c, data, variables, tv)
            if (tc == None or not (tipe in tv)) and tb == None:
                st.error('Falta definir tipus o és ambiguo', icon="🚨")
            elif tb != None:
                valor_c = tb[1]
                valor_a = tb[6:len(tb)-1]
                if tc != None:
                    if valor_c != tc:
                        st.error('Els tipus ' + valor_c + ' i ' +
                                 tc + ' son incompatibles', icon="🚨")
                else:
                    tv[c.tipe] = valor_c
                    calcular_tipo(c, data, variables, tv)
                if tipe in tv:
                    if valor_a != tv[tipe]:
                        st.error('Els tipus ' + valor_a + ' i ' +
                                 tv[tipe] + ' son incompatibles', icon="🚨")
                else:
                    tv[tipe] = valor_a
            else:
                valor_b = f"({tc} -> {tv[tipe]})"
                tv[b.tipe] = valor_b
                calcular_tipo(b, data, variables, tv)
            try:
                return tv[tipe]
            except KeyError:
                return None
        case Abst(b, c, tipe):
            tc = calcular_tipo(c, data, variables, tv)
            tb = calcular_tipo(b, data, variables, tv)
            if (tc == None or tb == None) and not (tipe in tv):
                st.error('Falta definir tipus o és ambiguo', icon="🚨")
            elif tipe in tv:
                valor_b = tv[tipe][1]
                valor_c = tv[tipe][6:len(tb)-1]
                if tc != None:
                    if valor_c != tc:
                        st.error('Els tipus ' + valor_c + ' i ' +
                                 tc + ' son incompatibles', icon="🚨")
                else:
                    tv[c.tipe] = valor_c
                    calcular_tipo(c, data, variables, tv)
                if tb != None:
                    if valor_b != tb:
                        st.error('Els tipus ' + valor_b + ' i ' +
                                 tb + ' son incompatibles', icon="🚨")
                else:
                    tv[b.tipe] = valor_b
                    calcular_tipo(b, data, variables, tv)
            else:
                valor_a = f"({tb} -> {tc})"
                tv[tipe] = valor_a
            try:
                return tv[tipe]
            except KeyError:
                return None


def arbol(t, graph, tv, node_id=0):
    match t:
        case Var(s, tipe):
            try:
                node_label = s + "\\n" + tv[variables[s]]
            except KeyError:
                node_label = s + "\\n" + tipe
            graph.node(str(node_id), label=node_label)
            return str(node_id), node_id + 1

        case Appl(a, b, tipe):
            try:
                node_label = '@' "\\n" + tv[tipe]
            except KeyError:
                node_label = '@' "\\n" + tipe
            graph.node(str(node_id), label=node_label)
            left_label, new_id = arbol(a, graph, tv, node_id + 1)
            right_label, new_id = arbol(b, graph, tv, new_id)
            graph.edge(str(node_id), left_label)
            graph.edge(str(node_id), right_label)
            return str(node_id), new_id

        case Abst(a, b, tipe):
            try:
                node_label = 'λ' "\\n" + tv[tipe]
            except KeyError:
                node_label = 'λ' "\\n" + tipe
            graph.node(str(node_id), label=node_label)
            left_label, new_id = arbol(a, graph, tv, node_id + 1)
            right_label, new_id = arbol(b, graph, tv, new_id)
            graph.edge(str(node_id), left_label)
            graph.edge(str(node_id), right_label)
            return str(node_id), new_id

    st.error('Error de representación de término!', icon="🚨")
    return "ERROR"


def posar_tipos(t: Terme, data, variables):
    letras_minusculas = string.ascii_lowercase
    global var
    match t:
        case Var(s, tipe):
            try:
                t.tipe = data[s]
            except KeyError:
                try:
                    t.tipe = variables[s]
                except:
                    variables[s] = letras_minusculas[var]
                    t.tipe = letras_minusculas[var]
                    var += 1
            return
        case Appl(a, b, tipe):
            t.tipe = letras_minusculas[var]
            var += 1
            posar_tipos(a, data, variables)
            posar_tipos(b, data, variables)
            return
        case Abst(a, b, tipe):
            t.tipe = letras_minusculas[var]
            var += 1
            posar_tipos(a, data, variables)
            posar_tipos(b, data, variables)
            return


def convert(res):
    result = res[-1]
    for element in reversed(res[:-1]):
        result = f"({element} -> {result})"
    return result


st.title('Practica LP')
error = "nice"
data = {}
variables = {}
tipus_variables = {}
var = 0
user_input = st.text_area("Pon tus expresiones aquí:")
if user_input:
    for linea in user_input.split('\n'):
        input_stream = InputStream(linea)
        lexer = exprsLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = exprsParser(token_stream)
        tree = parser.root()

        if parser.getNumberOfSyntaxErrors() == 0:
            visitor = TreeVisitor()
            result, t = visitor.visit(tree)
            if t:
                posar_tipos(result, data, variables)
                graph = graphviz.Digraph()
                error = arbol(result, graph, tipus_variables)
                if error != "ERROR":
                    st.graphviz_chart(graph)
                    calcular_tipo(result, data, variables, tipus_variables)
                    graph = graphviz.Digraph()
                    error = arbol(result, graph, tipus_variables)
                    if error != "ERROR":
                        st.graphviz_chart(graph)
                        df = pd.DataFrame(list(tipus_variables.items()),
                                          columns=['Var', 'Tipo'])
                        df.index = [""] * len(df.index)
                        st.table(df)
            else:
                r = convert(result[1:])
                data[result[0]] = r

        else:
            st.error(str(parser.getNumberOfSyntaxErrors()) +
                     'errors de sintaxi.', icon="🚨")
            error = "ERROR"
    if error != "ERROR":
        df = pd.DataFrame(list(data.items()), columns=['ID', 'Tipo'])
        df.index = [""] * len(df.index)
        st.table(df)
