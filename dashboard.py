"""
Dashboard Interativo - Otimização de Rotas de Entrega
======================================================
Dashboard completo para visualização e análise da rede de distribuição.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from otimizacao_rotas import RedeDistribuicao, criar_rede_exemplo


class DashboardRotas:
    """
    Classe para criar dashboard interativo de análise de rotas.
    """
    
    def __init__(self, rede):
        """
        Inicializa o dashboard com uma rede de distribuição.
        
        Args:
            rede: Objeto RedeDistribuicao
        """
        self.rede = rede
        self.fig = None
        self.pos = None
        
    def calcular_posicionamento(self):
        """Calcula o posicionamento dos nós do grafo."""
        self.pos = nx.spring_layout(self.rede.grafo, k=2, iterations=50, seed=42)
        return self.pos
    
    def criar_dashboard_completo(self):
        """
        Cria um dashboard completo com múltiplas visualizações.
        """
        # Criar figura com grid layout - mais espaçado
        self.fig = plt.figure(figsize=(20, 12), facecolor='#f8f9fa')
        gs = GridSpec(3, 3, figure=self.fig, hspace=0.35, wspace=0.35, 
                     left=0.05, right=0.95, top=0.93, bottom=0.07)
        
        # Calcular posicionamento uma vez
        self.calcular_posicionamento()
        
        # Painel 1: Visão geral da rede (grande, topo esquerda)
        ax1 = self.fig.add_subplot(gs[0:2, 0:2])
        ax1.set_facecolor('white')
        self._plotar_rede_completa(ax1)
        
        # Painel 2: Estatísticas da rede (topo direita)
        ax2 = self.fig.add_subplot(gs[0, 2])
        ax2.set_facecolor('#ffffff')
        self._plotar_estatisticas(ax2)
        
        # Painel 3: Caminhos mínimos (meio direita)
        ax3 = self.fig.add_subplot(gs[1, 2])
        ax3.set_facecolor('#ffffff')
        self._plotar_caminhos_minimos(ax3)
        
        # Painel 4: Análise de robustez (baixo esquerda)
        ax4 = self.fig.add_subplot(gs[2, 0])
        ax4.set_facecolor('#ffffff')
        self._plotar_robustez(ax4)
        
        # Painel 5: Distribuição de custos (baixo meio)
        ax5 = self.fig.add_subplot(gs[2, 1])
        ax5.set_facecolor('#ffffff')
        self._plotar_distribuicao_custos(ax5)
        
        # Painel 6: Centralidade das cidades (baixo direita)
        ax6 = self.fig.add_subplot(gs[2, 2])
        ax6.set_facecolor('#ffffff')
        self._plotar_centralidade(ax6)
        
        # Título geral - mais sutil
        self.fig.suptitle('Dashboard - Análise de Rotas de Entrega', 
                         fontsize=18, fontweight='bold', y=0.97,
                         color='#2c3e50')
        
        return self.fig
    
    def _plotar_rede_completa(self, ax):
        """Plota a rede completa no painel principal."""
        G = self.rede.grafo
        pos = self.pos
        
        # Desenhar arestas - mais suaves
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#bdc3c7', 
                              width=1.2, alpha=0.5, arrows=True, 
                              arrowsize=12, arrowstyle='->')
        
        # Labels das arestas (custos) - apenas valores, sem texto extra
        labels_arestas = {}
        for u, v in G.edges():
            custo = G[u][v]['custo']
            labels_arestas[(u, v)] = f'{custo}'
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_arestas, 
                                    ax=ax, font_size=8, font_color='#34495e',
                                    bbox=dict(boxstyle='round,pad=0.3', 
                                            facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Separar nós por tipo
        nos_armazem = [n for n in G.nodes() 
                      if G.nodes[n].get('tipo') == 'armazem']
        nos_clientes = [n for n in G.nodes() 
                       if G.nodes[n].get('tipo') == 'cliente']
        nos_outros = [n for n in G.nodes() 
                     if G.nodes[n].get('tipo') not in ['armazem', 'cliente']]
        
        # Desenhar nós - cores mais suaves
        if nos_armazem:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_armazem, ax=ax,
                                  node_color='#e74c3c', node_size=2200, 
                                  node_shape='s', alpha=0.85, 
                                  edgecolors='#c0392b', linewidths=2)
        if nos_clientes:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_clientes, ax=ax,
                                  node_color='#3498db', node_size=1600, 
                                  node_shape='o', alpha=0.85,
                                  edgecolors='#2980b9', linewidths=2)
        if nos_outros:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_outros, ax=ax,
                                  node_color='#95a5a6', node_size=1300, 
                                  node_shape='o', alpha=0.7,
                                  edgecolors='#7f8c8d', linewidths=1.5)
        
        # Labels dos nós - mais limpos
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight='bold',
                               font_color='#2c3e50')
        
        ax.set_title('Rede de Distribuição', fontsize=13, fontweight='bold', 
                    color='#2c3e50', pad=10)
        ax.axis('off')
    
    def _plotar_estatisticas(self, ax):
        """Plota estatísticas da rede."""
        G = self.rede.grafo
        
        # Calcular estatísticas
        num_nos = G.number_of_nodes()
        num_arestas = G.number_of_edges()
        densidade = nx.density(G)
        grau_medio = sum(dict(G.degree()).values()) / num_nos if num_nos > 0 else 0
        
        # Calcular custo total
        custos = [G[u][v]['custo'] for u, v in G.edges()]
        custo_total = sum(custos)
        custo_medio = custo_total / num_arestas if num_arestas > 0 else 0
        
        # Visualização mais limpa - cards de informação
        info_text = f"""
        Cidades: {num_nos}
        Estradas: {num_arestas}
        Densidade: {densidade:.3f}
        Grau Médio: {grau_medio:.2f}
        
        Custo Total: {custo_total:.0f}
        Custo Médio: {custo_medio:.0f}
        """
        
        ax.text(0.5, 0.5, info_text, fontsize=10, verticalalignment='center',
               horizontalalignment='center', family='sans-serif',
               transform=ax.transAxes, color='#2c3e50',
               bbox=dict(boxstyle='round,pad=1', facecolor='#ecf0f1', 
                        alpha=0.8, edgecolor='#bdc3c7', linewidth=1))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Estatísticas', fontsize=12, fontweight='bold', 
                    color='#2c3e50', pad=8)
    
    def _plotar_caminhos_minimos(self, ax):
        """Plota informações sobre caminhos mínimos."""
        if not self.rede.armazem:
            ax.text(0.5, 0.5, 'Nenhum armazém\ndefinido', 
                   ha='center', va='center', fontsize=11, color='#7f8c8d')
            ax.axis('off')
            return
        
        caminhos_info = []
        for cliente in self.rede.clientes:
            caminho, custo = self.rede.calcular_caminho_minimo_manual(
                self.rede.armazem, cliente)
            if caminho:
                caminhos_info.append({
                    'cliente': cliente,
                    'custo': custo
                })
        
        if not caminhos_info:
            ax.axis('off')
            return
        
        # Gráfico de barras com custos
        clientes = [info['cliente'] for info in caminhos_info]
        custos = [info['custo'] for info in caminhos_info]
        
        y_pos = np.arange(len(clientes))
        cores = plt.cm.Greens(np.linspace(0.4, 0.8, len(clientes)))
        bars = ax.barh(y_pos, custos, color=cores, alpha=0.7, 
                      edgecolor='white', linewidth=1.5)
        
        # Adicionar valores nas barras
        for i, (cliente, custo) in enumerate(zip(clientes, custos)):
            ax.text(custo, i, f'  {custo:.0f}', va='center', 
                   fontsize=9, fontweight='bold', color='#2c3e50')
            ax.text(-max(custos)*0.05, i, cliente[:12], va='center', ha='right',
                   fontsize=9, color='#34495e')
        
        ax.set_yticks([])
        ax.set_xlabel('Custo', fontsize=9, color='#7f8c8d')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(True, alpha=0.2, axis='x', linestyle='--')
        ax.set_title('Caminhos Mínimos', fontsize=12, fontweight='bold', 
                    color='#2c3e50', pad=8)
    
    def _plotar_robustez(self, ax):
        """Plota análise de robustez."""
        # Fazer análise rápida
        estradas_criticas = []
        estradas = list(self.rede.grafo.edges())
        
        for origem, destino in estradas[:5]:  # Limitar para performance
            # Salvar custo ANTES de remover a aresta
            custo_original = self.rede.grafo[origem][destino]['custo']
            self.rede.grafo.remove_edge(origem, destino)
            
            rotas_impossiveis = 0
            for cliente in self.rede.clientes:
                if self.rede.armazem:
                    caminho, _ = self.rede.calcular_caminho_minimo_manual(
                        self.rede.armazem, cliente)
                    if caminho is None:
                        rotas_impossiveis += 1
            
            # Restaurar aresta com o custo salvo
            self.rede.grafo.add_edge(origem, destino, peso=custo_original, 
                                    custo=custo_original)
            
            if rotas_impossiveis > 0:
                estradas_criticas.append((origem, destino, rotas_impossiveis))
        
        # Visualização mais limpa
        if estradas_criticas:
            nomes = [f"{o[:6]}→{d[:6]}" for o, d, _ in estradas_criticas[:4]]
            impactos = [i for _, _, i in estradas_criticas[:4]]
            
            y_pos = np.arange(len(nomes))
            cores = ['#e74c3c' if i > 0 else '#f39c12' for i in impactos]
            bars = ax.barh(y_pos, impactos, color=cores, alpha=0.7,
                          edgecolor='white', linewidth=1.5)
            
            for i, (nome, impacto) in enumerate(zip(nomes, impactos)):
                ax.text(impacto, i, f'  {impacto}', va='center',
                       fontsize=9, fontweight='bold', color='white')
                ax.text(-max(impactos)*0.1, i, nome, va='center', ha='right',
                       fontsize=8, color='#34495e')
            
            ax.set_yticks([])
            ax.set_xlabel('Rotas Afetadas', fontsize=9, color='#7f8c8d')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.grid(True, alpha=0.2, axis='x', linestyle='--')
        else:
            ax.text(0.5, 0.5, 'Nenhuma estrada\ncrítica encontrada',
                   ha='center', va='center', fontsize=10, color='#27ae60',
                   bbox=dict(boxstyle='round', facecolor='#d5f4e6', 
                           alpha=0.7, edgecolor='none'))
            ax.axis('off')
        
        ax.set_title('Robustez', fontsize=12, fontweight='bold', 
                    color='#2c3e50', pad=8)
    
    def _plotar_distribuicao_custos(self, ax):
        """Plota distribuição de custos das estradas."""
        custos = [self.rede.grafo[u][v]['custo'] for u, v in self.rede.grafo.edges()]
        
        ax.hist(custos, bins=min(8, len(custos)), edgecolor='white', 
               color='#3498db', alpha=0.7, linewidth=1.5)
        ax.set_xlabel('Custo', fontsize=9, color='#7f8c8d')
        ax.set_ylabel('Frequência', fontsize=9, color='#7f8c8d')
        ax.set_title('Distribuição de Custos', fontsize=12, fontweight='bold',
                    color='#2c3e50', pad=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.2, linestyle='--')
    
    def _plotar_centralidade(self, ax):
        """Plota centralidade das cidades."""
        G = self.rede.grafo
        
        # Calcular centralidade de grau
        centralidade = nx.degree_centrality(G)
        
        # Ordenar por centralidade
        cidades_ordenadas = sorted(centralidade.items(), 
                                  key=lambda x: x[1], reverse=True)
        
        # Pegar top 5
        top_cidades = cidades_ordenadas[:5]
        nomes = [c[0] for c in top_cidades]
        valores = [c[1] for c in top_cidades]
        
        # Criar gráfico de barras horizontal - mais limpo
        y_pos = np.arange(len(nomes))
        cores = plt.cm.Purples(np.linspace(0.5, 0.9, len(nomes)))
        bars = ax.barh(y_pos, valores, color=cores, alpha=0.7,
                      edgecolor='white', linewidth=1.5)
        
        # Adicionar valores
        for i, (nome, valor) in enumerate(zip(nomes, valores)):
            ax.text(valor, i, f'  {valor:.2f}', va='center',
                   fontsize=8, fontweight='bold', color='#2c3e50')
            ax.text(-max(valores)*0.05, i, nome[:10], va='center', ha='right',
                   fontsize=8, color='#34495e')
        
        ax.set_yticks([])
        ax.set_xlabel('Centralidade', fontsize=9, color='#7f8c8d')
        ax.set_title('Top 5 Cidades', fontsize=12, fontweight='bold',
                    color='#2c3e50', pad=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(True, alpha=0.2, axis='x', linestyle='--')
    
    def salvar_dashboard(self, nome_arquivo='dashboard_completo.png'):
        """Salva o dashboard em um arquivo."""
        if self.fig:
            self.fig.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
            print(f"✓ Dashboard salvo em: {nome_arquivo}")
        else:
            print("⚠️  Dashboard não foi criado ainda. Execute criar_dashboard_completo() primeiro.")
    
    def mostrar_dashboard(self):
        """Exibe o dashboard."""
        if self.fig:
            plt.show()
        else:
            print("⚠️  Dashboard não foi criado ainda. Execute criar_dashboard_completo() primeiro.")


def criar_dashboard_interativo():
    """
    Função principal para criar e exibir o dashboard.
    """
    print("="*60)
    print("CRIANDO DASHBOARD INTERATIVO")
    print("="*60)
    
    # Criar rede de exemplo
    print("\n📊 Carregando rede de distribuição...")
    rede = criar_rede_exemplo()
    
    # Criar dashboard
    print("🎨 Criando visualizações...")
    dashboard = DashboardRotas(rede)
    dashboard.criar_dashboard_completo()
    
    # Salvar
    print("💾 Salvando dashboard...")
    dashboard.salvar_dashboard()
    
    # Mostrar
    print("📺 Exibindo dashboard...")
    dashboard.mostrar_dashboard()
    
    print("\n✓ Dashboard criado com sucesso!")


if __name__ == "__main__":
    criar_dashboard_interativo()

