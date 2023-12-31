import streamlit as st
import numpy as np
from pyngrok import ngrok

class Caso:
  def __init__(self, descricao, atributos, pesos, recomendacao):
      self.descricao = descricao
      self.atributos = np.array(atributos)
      self.pesos = np.array(pesos)
      self.recomendacao = recomendacao

def similaridade_local(caso1, caso2):
  return np.sum(caso1.atributos[:-3] != caso2.atributos[:-2])

def similaridade_global(caso1, caso2):
  similaridades_locais = np.array([similaridade_local(caso1, caso2)])
  similaridade_ponderada = np.sum(similaridades_locais * caso1.pesos) / np.sum(caso1.pesos)
  return similaridade_ponderada

class SistemaRecomendacaoSRJ:
  def __init__(self):
      self.base_de_dados = []

  def adicionar_caso(self, caso):
      self.base_de_dados.append(caso)

  def recuperar_caso(self, novo_caso, medida_similaridade):
      similaridades = [medida_similaridade(novo_caso, caso) for caso in self.base_de_dados]
      indice_mais_similar = np.argmin(similaridades)
      return self.base_de_dados[indice_mais_similar]

categorias = {
    'Ação': {'Não Gosto': 0, 'Gosto': 1},
    'Corrida': {'Não Gosto': 0, 'Gosto': 1},
    'RPG': {'Não Gosto': 0, 'Gosto': 1},
    'Luta': {'Não Gosto': 0, 'Gosto': 1},
    'Aventura': {'Não Gosto': 0, 'Gosto': 1},
    'Simulação': {'Não Gosto': 0, 'Gosto': 1},
    'Multiplayer':{'Não Gosto': 0, 'Gosto': 1},
    'Recomendação': {'Contra': 0, 'The Legend Of Zelda': 1, 'Chrono Trigger': 2, 'Command&Conquer': 3, 'SimCity': 4, 'Street Fighter': 5, 'Super Mario Kart': 6, 'SuperMetroid': 7, 'Super Mario World': 8}
}

pesos_atributos = np.array([5, 1, 1, 1, 2, 1, 3, 1]).reshape(1, -1)

caso1 = Caso("Caso 1", [0, 0, 1, 0, 1, 0, 0, 0], pesos_atributos, 'Chrono Trigger')
caso2 = Caso("Caso 2", [1, 1, 0, 0, 0, 0, 1, 0], pesos_atributos, 'Super Mario Kart')
caso3 = Caso("Caso 3", [1, 0, 0, 1, 0, 0, 1, 0], pesos_atributos, 'Street Fighter')
caso4 = Caso("Caso 4", [1, 0, 0, 0, 1, 0, 0, 0], pesos_atributos, 'The Legend Of Zelda')
caso5 = Caso("Caso 5", [0, 0, 1, 0, 0, 1, 1, 0], pesos_atributos, 'SimCity')
caso6 = Caso("Caso 6", [0, 0, 0, 0, 1, 1, 0, 0], pesos_atributos, 'Command&Conquer')
caso7 = Caso("Caso 7", [1, 0, 0, 0, 0, 0, 0, 0], pesos_atributos, 'SuperMetroid ou Contra III')
caso8 = Caso("Caso 8", [1, 0, 0, 0, 1, 0, 0, 0], pesos_atributos, 'Super Mario World')


sistema = SistemaRecomendacaoSRJ()
sistema.adicionar_caso(caso1)
sistema.adicionar_caso(caso2)
sistema.adicionar_caso(caso3)
sistema.adicionar_caso(caso4)
sistema.adicionar_caso(caso5)
sistema.adicionar_caso(caso6)
sistema.adicionar_caso(caso7)
sistema.adicionar_caso(caso8)


st.title("SRJ - Sistema de Recomendação de Jogos Retrô")

st.header("Informe suas preferencias:")
acao = st.radio("Ação", ['Não Gosto', 'Gosto'])
corrida = st.radio("Corrida", ['Não Gosto', 'Gosto'])
rpg = st.radio("RPG", ['Não Gosto', 'Gosto'])
luta = st.radio("Luta", ['Não Gosto', 'Gosto'])
aventura = st.radio("Aventura", ['Não Gosto', 'Gosto'])
simulacao = st.radio("Simulação", ['Não Gosto', 'Gosto'])
multiplayer = st.radio("Multiplayer", ['Não Gosto', 'Gosto'])

novo_caso = Caso("Novo Caso",
                 [categorias['Ação'][acao],
                  categorias['Corrida'][corrida],
                  categorias['RPG'][rpg],
                  categorias['Luta'][luta],
                  categorias['Aventura'][aventura],
                  categorias['Simulação'][simulacao],
                  categorias['Multiplayer'][multiplayer],
                  0, 0],
                 pesos_atributos,
                 None)

caso_recuperado_global = sistema.recuperar_caso(novo_caso, similaridade_global)

st.header("Resultado:")
st.write(f"Acho que você vai se dar bem com: {caso_recuperado_global.recomendacao}")




