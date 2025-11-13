"""
Programa de Otimização de Rotas de Entrega
===========================================
Este programa modela uma rede de distribuição de mercadorias entre cidades,
utilizando grafos para calcular rotas otimizadas e analisar a robustez da rede.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import combinations
import copy

class RedeDistribuicao:
    """
    Classe para modelar e analisar uma rede de distribuição de mercadorias.
    """
    
    def __init__(self):
        """Inicializa a rede de distribuição."""
        self.grafo = nx.DiGraph()
        self.armazem = None
        self.clientes = []
        
    def adicionar_cidade(self, nome, tipo='cliente'):
        """
        Adiciona uma cidade à rede.
        
        Args:
            nome: Nome da cidade
            tipo: 'armazem' ou 'cliente'
        """
        self.grafo.add_node(nome, tipo=tipo)
        if tipo == 'armazem':
            self.armazem = nome
        elif tipo == 'cliente':
            self.clientes.append(nome)
    
    def adicionar_estrada(self, cidade_origem, cidade_destino, custo):
        """
        Adiciona uma estrada (aresta) entre duas cidades.
        
        Args:
            cidade_origem: Cidade de origem
            cidade_destino: Cidade de destino
            custo: Custo da estrada (distância, tempo, combustível, etc.)
        """
        self.grafo.add_edge(cidade_origem, cidade_destino, peso=custo, custo=custo)
    
    def visualizar_grafo(self, titulo="Rede de Distribuição", caminho_minimo=None, 
                        aresta_removida=None, salvar_arquivo=None):
        """
        Visualiza o grafo da rede de distribuição.
        
        Args:
            titulo: Título do gráfico
            caminho_minimo: Lista de arestas do caminho mínimo a destacar
            aresta_removida: Tupla (origem, destino) da aresta removida
            salvar_arquivo: Nome do arquivo para salvar a imagem
        """
        plt.figure(figsize=(14, 10))
        
        # Posicionamento dos nós usando layout spring
        pos = nx.spring_layout(self.grafo, k=2, iterations=50, seed=42)
        
        # Desenhar todas as arestas em cinza claro
        arestas_normais = [(u, v) for u, v in self.grafo.edges() 
                          if caminho_minimo is None or (u, v) not in caminho_minimo]
        nx.draw_networkx_edges(self.grafo, pos, edgelist=arestas_normais, 
                              edge_color='lightgray', width=1, alpha=0.5, 
                              arrows=True, arrowsize=20, arrowstyle='->')
        
        # Destacar caminho mínimo se fornecido
        if caminho_minimo:
            nx.draw_networkx_edges(self.grafo, pos, edgelist=caminho_minimo, 
                                  edge_color='green', width=3, alpha=0.8,
                                  arrows=True, arrowsize=25, arrowstyle='->',
                                  style='dashed')
        
        # Destacar aresta removida se fornecida
        if aresta_removida:
            if aresta_removida in self.grafo.edges():
                nx.draw_networkx_edges(self.grafo, pos, edgelist=[aresta_removida], 
                                      edge_color='red', width=2, alpha=0.5,
                                      arrows=True, arrowsize=20, arrowstyle='->',
                                      style='dotted')
        
        # Desenhar nós
        nos_armazem = [n for n in self.grafo.nodes() 
                      if self.grafo.nodes[n].get('tipo') == 'armazem']
        nos_clientes = [n for n in self.grafo.nodes() 
                       if self.grafo.nodes[n].get('tipo') == 'cliente']
        nos_outros = [n for n in self.grafo.nodes() 
                     if self.grafo.nodes[n].get('tipo') not in ['armazem', 'cliente']]
        
        if nos_armazem:
            nx.draw_networkx_nodes(self.grafo, pos, nodelist=nos_armazem, 
                                  node_color='red', node_size=1500, 
                                  node_shape='s', alpha=0.9)
        if nos_clientes:
            nx.draw_networkx_nodes(self.grafo, pos, nodelist=nos_clientes, 
                                  node_color='blue', node_size=1000, 
                                  node_shape='o', alpha=0.9)
        if nos_outros:
            nx.draw_networkx_nodes(self.grafo, pos, nodelist=nos_outros, 
                                  node_color='lightblue', node_size=800, 
                                  node_shape='o', alpha=0.7)
        
        # Labels dos nós
        nx.draw_networkx_labels(self.grafo, pos, font_size=10, font_weight='bold')
        
        # Labels das arestas (custos)
        labels_arestas = {}
        for u, v in self.grafo.edges():
            custo = self.grafo[u][v]['custo']
            labels_arestas[(u, v)] = f'{custo}'
        
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels_arestas, 
                                    font_size=8, font_color='darkblue')
        
        # Legenda
        legenda = [
            mpatches.Patch(color='red', label='Armazém'),
            mpatches.Patch(color='blue', label='Cliente'),
            mpatches.Patch(color='lightblue', label='Cidade Intermediária'),
        ]
        if caminho_minimo:
            legenda.append(mpatches.Patch(color='green', label='Caminho Mínimo'))
        if aresta_removida:
            legenda.append(mpatches.Patch(color='red', label='Estrada Removida (Falha)'))
        
        plt.legend(handles=legenda, loc='upper left')
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if salvar_arquivo:
            plt.savefig(salvar_arquivo, dpi=300, bbox_inches='tight')
            print(f"Gráfico salvo em: {salvar_arquivo}")
        
        plt.show()
    
    def calcular_caminho_minimo_manual(self, origem, destino):
        """
        Calcula o caminho mínimo entre origem e destino usando método manual
        (sem algoritmos avançados como Dijkstra).
        
        Este método explora todos os caminhos possíveis e escolhe o de menor custo.
        
        Args:
            origem: Cidade de origem
            destino: Cidade de destino
            
        Returns:
            Tupla (caminho, custo_total) ou (None, None) se não houver caminho
        """
        if origem not in self.grafo or destino not in self.grafo:
            return None, None
        
        if origem == destino:
            return [origem], 0
        
        # Usar busca em profundidade para encontrar todos os caminhos
        caminhos_encontrados = []
        
        def dfs(atual, destino, caminho_atual, custo_atual, visitados):
            """Busca em profundidade para encontrar todos os caminhos."""
            if atual == destino:
                caminhos_encontrados.append((caminho_atual.copy(), custo_atual))
                return
            
            visitados.add(atual)
            
            for vizinho in self.grafo.successors(atual):
                if vizinho not in visitados:
                    custo_aresta = self.grafo[atual][vizinho]['custo']
                    caminho_atual.append(vizinho)
                    dfs(vizinho, destino, caminho_atual, custo_atual + custo_aresta, visitados)
                    caminho_atual.pop()
            
            visitados.remove(atual)
        
        dfs(origem, destino, [origem], 0, set())
        
        if not caminhos_encontrados:
            return None, None
        
        # Encontrar o caminho de menor custo
        caminho_minimo, custo_minimo = min(caminhos_encontrados, key=lambda x: x[1])
        
        return caminho_minimo, custo_minimo
    
    def obter_arestas_do_caminho(self, caminho):
        """
        Converte uma lista de nós em uma lista de arestas (tuplas).
        
        Args:
            caminho: Lista de nós do caminho
            
        Returns:
            Lista de tuplas (origem, destino)
        """
        if len(caminho) < 2:
            return []
        return [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
    
    def simular_falha_estrada(self, cidade_origem, cidade_destino):
        """
        Simula a falha de uma estrada removendo-a temporariamente do grafo.
        
        Args:
            cidade_origem: Cidade de origem da estrada
            cidade_destino: Cidade de destino da estrada
            
        Returns:
            Grafo modificado (cópia) sem a aresta removida
        """
        grafo_backup = copy.deepcopy(self.grafo)
        
        if self.grafo.has_edge(cidade_origem, cidade_destino):
            self.grafo.remove_edge(cidade_origem, cidade_destino)
            print(f"\n⚠️  FALHA SIMULADA: Estrada {cidade_origem} -> {cidade_destino} foi removida!")
            return grafo_backup
        else:
            print(f"⚠️  A estrada {cidade_origem} -> {cidade_destino} não existe no grafo.")
            return None
    
    def restaurar_grafo(self, grafo_backup):
        """
        Restaura o grafo ao estado anterior.
        
        Args:
            grafo_backup: Grafo a ser restaurado
        """
        if grafo_backup:
            self.grafo = grafo_backup
            print("✓ Grafo restaurado ao estado original.")
    
    def analisar_robustez(self):
        """
        Analisa a robustez da rede identificando estradas e cidades críticas.
        
        Returns:
            Dicionário com análise de robustez
        """
        print("\n" + "="*60)
        print("ANÁLISE DE ROBUSTEZ DA REDE")
        print("="*60)
        
        analise = {
            'estradas_criticas': [],
            'cidades_criticas': [],
            'impacto_falhas': {}
        }
        
        # Analisar cada estrada
        estradas = list(self.grafo.edges())
        print(f"\n📊 Total de estradas na rede: {len(estradas)}")
        
        for origem, destino in estradas:
            # Simular remoção da estrada
            custo_original = self.grafo[origem][destino]['custo']
            self.grafo.remove_edge(origem, destino)
            
            # Verificar impacto em cada rota armazém -> cliente
            impacto_total = 0
            rotas_afetadas = []
            rotas_impossiveis = []
            
            for cliente in self.clientes:
                if self.armazem:
                    caminho_original, custo_original_rota = self.calcular_caminho_minimo_manual(
                        self.armazem, cliente)
                    
                    caminho_novo, custo_novo = self.calcular_caminho_minimo_manual(
                        self.armazem, cliente)
                    
                    if caminho_novo is None:
                        rotas_impossiveis.append(cliente)
                        impacto_total = float('inf')
                    elif caminho_original:
                        diferenca = custo_novo - custo_original_rota
                        if diferenca > 0:
                            impacto_total += diferenca
                            rotas_afetadas.append((cliente, diferenca))
            
            # Restaurar aresta
            self.grafo.add_edge(origem, destino, peso=custo_original, custo=custo_original)
            
            # Classificar criticidade
            if rotas_impossiveis:
                analise['estradas_criticas'].append({
                    'estrada': (origem, destino),
                    'tipo': 'CRÍTICA - Torna rotas impossíveis',
                    'rotas_impossiveis': rotas_impossiveis
                })
            elif impacto_total > 0:
                analise['estradas_criticas'].append({
                    'estrada': (origem, destino),
                    'tipo': 'IMPORTANTE - Aumenta custos significativamente',
                    'impacto': impacto_total,
                    'rotas_afetadas': rotas_afetadas
                })
            
            analise['impacto_falhas'][(origem, destino)] = {
                'rotas_impossiveis': rotas_impossiveis,
                'rotas_afetadas': rotas_afetadas,
                'impacto_total': impacto_total
            }
        
        # Analisar cidades críticas (nós de corte)
        print(f"\n🏙️  Análise de Cidades:")
        for cidade in self.grafo.nodes():
            if cidade == self.armazem:
                continue
            
            # Verificar se a cidade é ponto de passagem obrigatório
            grau_entrada = self.grafo.in_degree(cidade)
            grau_saida = self.grafo.out_degree(cidade)
            
            if grau_entrada == 1 or grau_saida == 1:
                analise['cidades_criticas'].append({
                    'cidade': cidade,
                    'razao': 'Poucas conexões (ponto único de passagem)',
                    'grau_entrada': grau_entrada,
                    'grau_saida': grau_saida
                })
        
        # Exibir resultados
        print(f"\n🚨 Estradas Críticas encontradas: {len(analise['estradas_criticas'])}")
        for estrada_info in analise['estradas_criticas']:
            estrada = estrada_info['estrada']
            print(f"   • {estrada[0]} -> {estrada[1]}: {estrada_info['tipo']}")
            if 'rotas_impossiveis' in estrada_info:
                print(f"     Rotas impossíveis: {estrada_info['rotas_impossiveis']}")
            if 'impacto' in estrada_info:
                print(f"     Impacto total: +{estrada_info['impacto']:.2f} unidades de custo")
        
        print(f"\n🏙️  Cidades Críticas encontradas: {len(analise['cidades_criticas'])}")
        for cidade_info in analise['cidades_criticas']:
            print(f"   • {cidade_info['cidade']}: {cidade_info['razao']}")
            print(f"     Grau entrada: {cidade_info['grau_entrada']}, "
                  f"Grau saída: {cidade_info['grau_saida']}")
        
        return analise
    
    def comparar_rotas(self, origem, destino):
        """
        Compara diferentes rotas possíveis entre origem e destino.
        
        Args:
            origem: Cidade de origem
            destino: Cidade de destino
            
        Returns:
            Lista de todas as rotas possíveis ordenadas por custo
        """
        caminhos_encontrados = []
        
        def dfs(atual, destino, caminho_atual, custo_atual, visitados):
            if atual == destino:
                caminhos_encontrados.append((caminho_atual.copy(), custo_atual))
                return
            
            visitados.add(atual)
            
            for vizinho in self.grafo.successors(atual):
                if vizinho not in visitados:
                    custo_aresta = self.grafo[atual][vizinho]['custo']
                    caminho_atual.append(vizinho)
                    dfs(vizinho, destino, caminho_atual, custo_atual + custo_aresta, visitados)
                    caminho_atual.pop()
            
            visitados.remove(atual)
        
        dfs(origem, destino, [origem], 0, set())
        
        # Ordenar por custo
        caminhos_encontrados.sort(key=lambda x: x[1])
        
        return caminhos_encontrados


def criar_rede_exemplo():
    """
    Cria uma rede de distribuição de exemplo com cidades brasileiras.
    """
    rede = RedeDistribuicao()
    
    # Definir cidades
    # Armazém principal
    rede.adicionar_cidade("São Paulo", tipo='armazem')
    
    # Cidades intermediárias
    rede.adicionar_cidade("Campinas", tipo='intermediaria')
    rede.adicionar_cidade("Ribeirão Preto", tipo='intermediaria')
    rede.adicionar_cidade("Sorocaba", tipo='intermediaria')
    
    # Clientes
    rede.adicionar_cidade("Rio de Janeiro", tipo='cliente')
    rede.adicionar_cidade("Belo Horizonte", tipo='cliente')
    rede.adicionar_cidade("Curitiba", tipo='cliente')
    
    # Adicionar estradas com custos (em unidades de custo de transporte)
    # Custo pode representar: distância (km), tempo (horas), ou custo de combustível
    
    # Rotas do armazém (São Paulo)
    rede.adicionar_estrada("São Paulo", "Campinas", 100)
    rede.adicionar_estrada("São Paulo", "Sorocaba", 90)
    rede.adicionar_estrada("São Paulo", "Ribeirão Preto", 310)
    
    # Rotas de Campinas
    rede.adicionar_estrada("Campinas", "Rio de Janeiro", 350)
    rede.adicionar_estrada("Campinas", "Belo Horizonte", 580)
    rede.adicionar_estrada("Campinas", "Sorocaba", 120)
    
    # Rotas de Sorocaba
    rede.adicionar_estrada("Sorocaba", "Curitiba", 280)
    rede.adicionar_estrada("Sorocaba", "Campinas", 120)
    
    # Rotas de Ribeirão Preto
    rede.adicionar_estrada("Ribeirão Preto", "Belo Horizonte", 520)
    rede.adicionar_estrada("Ribeirão Preto", "Campinas", 220)
    
    # Rotas diretas para clientes
    rede.adicionar_estrada("São Paulo", "Rio de Janeiro", 430)
    rede.adicionar_estrada("São Paulo", "Curitiba", 410)
    
    # Rotas entre clientes (para flexibilidade)
    rede.adicionar_estrada("Rio de Janeiro", "Belo Horizonte", 440)
    rede.adicionar_estrada("Belo Horizonte", "Curitiba", 980)
    
    return rede


def executar_parte_1(rede):
    """Executa a Parte 1: Representação do Grafo."""
    print("\n" + "="*60)
    print("PARTE 1: REPRESENTAÇÃO DO GRAFO")
    print("="*60)
    
    print(f"\n📊 Informações da Rede:")
    print(f"   • Total de cidades: {rede.grafo.number_of_nodes()}")
    print(f"   • Total de estradas: {rede.grafo.number_of_edges()}")
    print(f"   • Armazém: {rede.armazem}")
    print(f"   • Clientes: {', '.join(rede.clientes)}")
    
    print(f"\n🛣️  Estradas e Custos:")
    for origem, destino in rede.grafo.edges():
        custo = rede.grafo[origem][destino]['custo']
        print(f"   • {origem} -> {destino}: {custo} unidades")
    
    rede.visualizar_grafo(
        titulo="Parte 1: Rede de Distribuição - Cidades e Estradas",
        salvar_arquivo="parte1_rede_distribuicao.png"
    )


def executar_parte_2(rede):
    """Executa a Parte 2: Cálculo de Caminho Mínimo."""
    print("\n" + "="*60)
    print("PARTE 2: CÁLCULO DE CAMINHO MÍNIMO (MÉTODO MANUAL)")
    print("="*60)
    
    if not rede.armazem:
        print("⚠️  Nenhum armazém definido!")
        return
    
    resultados = {}
    
    for cliente in rede.clientes:
        print(f"\n📍 Calculando rota: {rede.armazem} -> {cliente}")
        caminho, custo = rede.calcular_caminho_minimo_manual(rede.armazem, cliente)
        
        if caminho:
            print(f"   ✓ Caminho encontrado: {' -> '.join(caminho)}")
            print(f"   ✓ Custo total: {custo} unidades")
            resultados[cliente] = (caminho, custo)
        else:
            print(f"   ✗ Não há caminho disponível!")
            resultados[cliente] = (None, None)
    
    # Visualizar com caminho mínimo destacado
    if resultados:
        # Pegar o primeiro caminho para visualização
        primeiro_cliente = rede.clientes[0]
        if primeiro_cliente in resultados and resultados[primeiro_cliente][0]:
            caminho_min = resultados[primeiro_cliente][0]
            arestas_caminho = rede.obter_arestas_do_caminho(caminho_min)
            rede.visualizar_grafo(
                titulo=f"Parte 2: Caminho Mínimo {rede.armazem} -> {primeiro_cliente}",
                caminho_minimo=arestas_caminho,
                salvar_arquivo="parte2_caminho_minimo.png"
            )
    
    return resultados


def executar_parte_3(rede):
    """Executa a Parte 3: Caminhos Alternativos (Simulação de Falha)."""
    print("\n" + "="*60)
    print("PARTE 3: CAMINHOS ALTERNATIVOS (SIMULAÇÃO DE FALHA)")
    print("="*60)
    
    # Escolher uma estrada para simular falha
    # Vamos simular a falha de uma estrada importante
    estrada_falha = ("São Paulo", "Campinas")
    
    print(f"\n🔧 Simulando falha na estrada: {estrada_falha[0]} -> {estrada_falha[1]}")
    
    grafo_backup = rede.simular_falha_estrada(estrada_falha[0], estrada_falha[1])
    
    if grafo_backup:
        print(f"\n📊 Análise após falha:")
        
        rotas_alternativas = {}
        for cliente in rede.clientes:
            print(f"\n📍 Rota alternativa: {rede.armazem} -> {cliente}")
            caminho, custo = rede.calcular_caminho_minimo_manual(rede.armazem, cliente)
            
            if caminho:
                print(f"   ✓ Rota alternativa encontrada: {' -> '.join(caminho)}")
                print(f"   ✓ Novo custo: {custo} unidades")
                rotas_alternativas[cliente] = (caminho, custo)
            else:
                print(f"   ✗ Nenhuma rota alternativa disponível!")
                rotas_alternativas[cliente] = (None, None)
        
        # Visualizar com estrada removida
        arestas_caminho_alt = []
        if rotas_alternativas and rotas_alternativas[rede.clientes[0]][0]:
            caminho_alt = rotas_alternativas[rede.clientes[0]][0]
            arestas_caminho_alt = rede.obter_arestas_do_caminho(caminho_alt)
        
        rede.visualizar_grafo(
            titulo="Parte 3: Rotas Alternativas após Falha",
            caminho_minimo=arestas_caminho_alt,
            aresta_removida=estrada_falha,
            salvar_arquivo="parte3_rotas_alternativas.png"
        )
        
        # Restaurar grafo
        rede.restaurar_grafo(grafo_backup)
        
        return rotas_alternativas
    
    return None


def executar_parte_4(rede):
    """Executa a Parte 4: Análise de Robustez."""
    print("\n" + "="*60)
    print("PARTE 4: ANÁLISE DE ROBUSTEZ DA REDE")
    print("="*60)
    
    analise = rede.analisar_robustez()
    
    # Visualizar estradas críticas
    if analise['estradas_criticas']:
        primeira_critica = analise['estradas_criticas'][0]['estrada']
        grafo_backup = rede.simular_falha_estrada(primeira_critica[0], primeira_critica[1])
        
        if grafo_backup:
            rede.visualizar_grafo(
                titulo="Parte 4: Análise de Robustez - Estrada Crítica Removida",
                aresta_removida=primeira_critica,
                salvar_arquivo="parte4_analise_robustez.png"
            )
            rede.restaurar_grafo(grafo_backup)
    
    return analise


def executar_parte_5(rede):
    """Executa a Parte 5: Comparação de Resultados."""
    print("\n" + "="*60)
    print("PARTE 5: COMPARAÇÃO DE RESULTADOS")
    print("="*60)
    
    print("\n📊 Comparação de Rotas Alternativas:")
    
    if not rede.armazem or not rede.clientes:
        print("⚠️  Armazém ou clientes não definidos!")
        return
    
    for cliente in rede.clientes:
        print(f"\n📍 Todas as rotas possíveis: {rede.armazem} -> {cliente}")
        rotas = rede.comparar_rotas(rede.armazem, cliente)
        
        if rotas:
            print(f"   Total de rotas encontradas: {len(rotas)}")
            for i, (caminho, custo) in enumerate(rotas[:5], 1):  # Mostrar até 5 rotas
                print(f"   Rota {i}: {' -> '.join(caminho)} (Custo: {custo})")
            if len(rotas) > 5:
                print(f"   ... e mais {len(rotas) - 5} rotas")
        else:
            print(f"   ✗ Nenhuma rota encontrada")
    
    print("\n📈 Estatísticas da Rede:")
    print(f"   • Densidade da rede: {nx.density(rede.grafo):.3f}")
    print(f"   • Grau médio: {sum(dict(rede.grafo.degree()).values()) / rede.grafo.number_of_nodes():.2f}")
    
    # Calcular centralidade
    centralidade = nx.degree_centrality(rede.grafo)
    cidade_mais_central = max(centralidade, key=centralidade.get)
    print(f"   • Cidade mais central (mais conexões): {cidade_mais_central} "
          f"(centralidade: {centralidade[cidade_mais_central]:.3f})")


def gerar_relatorio(rede, resultados_parte2, rotas_alternativas, analise_robustez):
    """
    Gera um relatório em texto com os resultados do exercício.
    """
    relatorio = []
    relatorio.append("="*80)
    relatorio.append("RELATÓRIO: OTIMIZAÇÃO DE ROTAS DE ENTREGA")
    relatorio.append("="*80)
    relatorio.append("")
    
    relatorio.append("1. ESCOLHAS E MODELAGEM")
    relatorio.append("-"*80)
    relatorio.append(f"Cidades escolhidas: {', '.join(rede.grafo.nodes())}")
    relatorio.append(f"Armazém: {rede.armazem}")
    relatorio.append(f"Clientes: {', '.join(rede.clientes)}")
    relatorio.append(f"Total de estradas: {rede.grafo.number_of_edges()}")
    relatorio.append("")
    relatorio.append("Estradas e custos:")
    for origem, destino in rede.grafo.edges():
        custo = rede.grafo[origem][destino]['custo']
        relatorio.append(f"  • {origem} -> {destino}: {custo} unidades")
    relatorio.append("")
    
    relatorio.append("2. CAMINHOS MÍNIMOS")
    relatorio.append("-"*80)
    for cliente, (caminho, custo) in resultados_parte2.items():
        if caminho:
            relatorio.append(f"Rota {rede.armazem} -> {cliente}:")
            relatorio.append(f"  Caminho: {' -> '.join(caminho)}")
            relatorio.append(f"  Custo: {custo} unidades")
        else:
            relatorio.append(f"Rota {rede.armazem} -> {cliente}: Não disponível")
    relatorio.append("")
    
    relatorio.append("3. ROTAS ALTERNATIVAS (APÓS FALHA)")
    relatorio.append("-"*80)
    if rotas_alternativas:
        for cliente, (caminho, custo) in rotas_alternativas.items():
            if caminho:
                relatorio.append(f"Rota alternativa {rede.armazem} -> {cliente}:")
                relatorio.append(f"  Caminho: {' -> '.join(caminho)}")
                relatorio.append(f"  Custo: {custo} unidades")
            else:
                relatorio.append(f"Rota alternativa {rede.armazem} -> {cliente}: Não disponível")
    relatorio.append("")
    
    relatorio.append("4. ANÁLISE DE ROBUSTEZ")
    relatorio.append("-"*80)
    relatorio.append(f"Estradas críticas encontradas: {len(analise_robustez['estradas_criticas'])}")
    for estrada_info in analise_robustez['estradas_criticas']:
        estrada = estrada_info['estrada']
        relatorio.append(f"  • {estrada[0]} -> {estrada[1]}: {estrada_info['tipo']}")
    relatorio.append("")
    relatorio.append(f"Cidades críticas encontradas: {len(analise_robustez['cidades_criticas'])}")
    for cidade_info in analise_robustez['cidades_criticas']:
        relatorio.append(f"  • {cidade_info['cidade']}: {cidade_info['razao']}")
    relatorio.append("")
    
    relatorio.append("5. CONCLUSÕES")
    relatorio.append("-"*80)
    relatorio.append("• A rede de distribuição foi modelada com sucesso usando grafos direcionados.")
    relatorio.append("• Os caminhos mínimos foram calculados usando método manual (busca em profundidade).")
    relatorio.append("• A análise de robustez identificou estradas e cidades críticas na rede.")
    relatorio.append("• A simulação de falhas demonstrou a importância de ter rotas alternativas.")
    relatorio.append("")
    relatorio.append("="*80)
    
    conteudo = "\n".join(relatorio)
    
    with open("relatorio.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print("\n✓ Relatório salvo em: relatorio.txt")
    return conteudo


def main():
    """Função principal que executa todas as partes do exercício."""
    print("="*60)
    print("PROGRAMA DE OTIMIZAÇÃO DE ROTAS DE ENTREGA")
    print("="*60)
    
    # Criar rede de distribuição
    rede = criar_rede_exemplo()
    
    # Executar todas as partes
    executar_parte_1(rede)
    
    resultados_parte2 = executar_parte_2(rede)
    
    rotas_alternativas = executar_parte_3(rede)
    
    analise_robustez = executar_parte_4(rede)
    
    executar_parte_5(rede)
    
    # Gerar relatório
    print("\n" + "="*60)
    print("GERANDO RELATÓRIO")
    print("="*60)
    gerar_relatorio(rede, resultados_parte2, rotas_alternativas, analise_robustez)
    
    print("\n" + "="*60)
    print("✓ EXECUÇÃO CONCLUÍDA!")
    print("="*60)
    print("\nArquivos gerados:")
    print("  • parte1_rede_distribuicao.png")
    print("  • parte2_caminho_minimo.png")
    print("  • parte3_rotas_alternativas.png")
    print("  • parte4_analise_robustez.png")
    print("  • relatorio.txt")


if __name__ == "__main__":
    main()

