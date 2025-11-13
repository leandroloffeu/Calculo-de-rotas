"""
Dashboard Avançado - Análise Detalhada de Rotas
================================================
Dashboard com análises mais detalhadas e interativas.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from otimizacao_rotas import RedeDistribuicao, criar_rede_exemplo


class DashboardAvancado:
    """
    Dashboard avançado com análises detalhadas.
    """
    
    def __init__(self, rede):
        self.rede = rede
        self.fig = None
        self.pos = None
        
    def calcular_posicionamento(self):
        """Calcula posicionamento otimizado dos nós."""
        self.pos = nx.spring_layout(self.rede.grafo, k=2.5, iterations=100, seed=42)
        return self.pos
    
    def criar_dashboard(self):
        """Cria dashboard avançado completo."""
        self.fig = plt.figure(figsize=(22, 14))
        gs = GridSpec(4, 4, figure=self.fig, hspace=0.35, wspace=0.35)
        
        self.calcular_posicionamento()
        
        # Painel 1: Rede completa com caminhos mínimos destacados
        ax1 = self.fig.add_subplot(gs[0:2, 0:2])
        self._plotar_rede_com_caminhos(ax1)
        
        # Painel 2: Tabela de rotas
        ax2 = self.fig.add_subplot(gs[0, 2:4])
        self._plotar_tabela_rotas(ax2)
        
        # Painel 3: Matriz de custos
        ax3 = self.fig.add_subplot(gs[1, 2:4])
        self._plotar_matriz_custos(ax3)
        
        # Painel 4: Análise de falhas
        ax4 = self.fig.add_subplot(gs[2, 0:2])
        self._plotar_analise_falhas(ax4)
        
        # Painel 5: Comparação de rotas
        ax5 = self.fig.add_subplot(gs[2, 2])
        self._plotar_comparacao_rotas(ax5)
        
        # Painel 6: Topologia da rede
        ax6 = self.fig.add_subplot(gs[2, 3])
        self._plotar_topologia(ax6)
        
        # Painel 7: Métricas de performance
        ax7 = self.fig.add_subplot(gs[3, 0])
        self._plotar_metricas(ax7)
        
        # Painel 8: Cidades críticas
        ax8 = self.fig.add_subplot(gs[3, 1])
        self._plotar_cidades_criticas(ax8)
        
        # Painel 9: Análise de custos
        ax9 = self.fig.add_subplot(gs[3, 2:4])
        self._plotar_analise_custos(ax9)
        
        self.fig.suptitle('DASHBOARD AVANÇADO - ANÁLISE DETALHADA DE ROTAS', 
                         fontsize=22, fontweight='bold', y=0.99)
        
        plt.tight_layout(rect=[0, 0, 1, 0.98])
        return self.fig
    
    def _plotar_rede_com_caminhos(self, ax):
        """Plota rede com todos os caminhos mínimos destacados."""
        G = self.rede.grafo
        pos = self.pos
        
        # Desenhar todas as arestas
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='lightgray', 
                              width=1, alpha=0.4, arrows=True, 
                              arrowsize=12, arrowstyle='->')
        
        # Destacar caminhos mínimos
        if self.rede.armazem:
            cores_caminhos = plt.cm.Set3(np.linspace(0, 1, len(self.rede.clientes)))
            for i, cliente in enumerate(self.rede.clientes):
                caminho, _ = self.rede.calcular_caminho_minimo_manual(
                    self.rede.armazem, cliente)
                if caminho and len(caminho) > 1:
                    arestas_caminho = [(caminho[j], caminho[j+1]) 
                                      for j in range(len(caminho)-1)]
                    nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, ax=ax,
                                          edge_color=cores_caminhos[i], width=2.5, 
                                          alpha=0.7, arrows=True, arrowsize=15,
                                          arrowstyle='->', style='dashed')
        
        # Nós
        nos_armazem = [n for n in G.nodes() if G.nodes[n].get('tipo') == 'armazem']
        nos_clientes = [n for n in G.nodes() if G.nodes[n].get('tipo') == 'cliente']
        nos_outros = [n for n in G.nodes() 
                     if G.nodes[n].get('tipo') not in ['armazem', 'cliente']]
        
        if nos_armazem:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_armazem, ax=ax,
                                  node_color='red', node_size=2500, 
                                  node_shape='s', alpha=0.9, edgecolors='black', linewidths=2)
        if nos_clientes:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_clientes, ax=ax,
                                  node_color='blue', node_size=1800, 
                                  node_shape='o', alpha=0.9, edgecolors='black', linewidths=2)
        if nos_outros:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_outros, ax=ax,
                                  node_color='lightblue', node_size=1400, 
                                  node_shape='o', alpha=0.7, edgecolors='black', linewidths=1)
        
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
        
        ax.set_title('Rede com Caminhos Mínimos Destacados', 
                    fontsize=13, fontweight='bold', pad=10)
        ax.axis('off')
    
    def _plotar_tabela_rotas(self, ax):
        """Plota tabela com todas as rotas e custos."""
        if not self.rede.armazem:
            ax.text(0.5, 0.5, 'Nenhum armazém definido', 
                   ha='center', va='center', fontsize=12)
            ax.axis('off')
            return
        
        # Preparar dados da tabela
        dados = []
        for cliente in self.rede.clientes:
            caminho, custo = self.rede.calcular_caminho_minimo_manual(
                self.rede.armazem, cliente)
            if caminho:
                rota_curta = ' → '.join(caminho[:3])
                if len(caminho) > 3:
                    rota_curta += '...'
                dados.append([cliente, rota_curta, f'{custo:.0f}'])
        
        # Criar tabela
        if dados:
            tabela = ax.table(cellText=dados,
                            colLabels=['Cliente', 'Rota', 'Custo'],
                            cellLoc='left',
                            loc='center',
                            colWidths=[0.25, 0.5, 0.25])
            tabela.auto_set_font_size(False)
            tabela.set_fontsize(9)
            tabela.scale(1, 2)
            
            # Estilizar cabeçalho
            for i in range(3):
                tabela[(0, i)].set_facecolor('#4CAF50')
                tabela[(0, i)].set_text_props(weight='bold', color='white')
        
        ax.axis('off')
        ax.set_title('Tabela de Rotas Mínimas', fontsize=12, fontweight='bold')
    
    def _plotar_matriz_custos(self, ax):
        """Plota matriz de custos entre cidades."""
        cidades = list(self.rede.grafo.nodes())
        n = len(cidades)
        matriz = np.full((n, n), np.nan)
        
        for i, origem in enumerate(cidades):
            for j, destino in enumerate(cidades):
                if self.rede.grafo.has_edge(origem, destino):
                    matriz[i][j] = self.rede.grafo[origem][destino]['custo']
        
        im = ax.imshow(matriz, cmap='YlOrRd', aspect='auto')
        
        # Configurar ticks
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels([c[:8] for c in cidades], rotation=45, ha='right', fontsize=8)
        ax.set_yticklabels([c[:8] for c in cidades], fontsize=8)
        
        # Adicionar valores na matriz
        for i in range(n):
            for j in range(n):
                if not np.isnan(matriz[i][j]):
                    ax.text(j, i, f'{int(matriz[i][j])}', 
                           ha='center', va='center', fontsize=7, 
                           color='white' if matriz[i][j] > matriz[~np.isnan(matriz)].mean() else 'black')
        
        plt.colorbar(im, ax=ax, label='Custo')
        ax.set_title('Matriz de Custos entre Cidades', fontsize=12, fontweight='bold')
    
    def _plotar_analise_falhas(self, ax):
        """Plota análise de impacto de falhas."""
        estradas = list(self.rede.grafo.edges())
        impactos = []
        
        for origem, destino in estradas[:8]:  # Limitar para performance
            # Salvar custo ANTES de remover a aresta
            custo_aresta = self.rede.grafo[origem][destino]['custo']
            self.rede.grafo.remove_edge(origem, destino)
            
            rotas_impossiveis = 0
            aumento_custo_total = 0
            
            for cliente in self.rede.clientes:
                if self.rede.armazem:
                    caminho_original, custo_original = self.rede.calcular_caminho_minimo_manual(
                        self.rede.armazem, cliente)
                    caminho_novo, custo_novo = self.rede.calcular_caminho_minimo_manual(
                        self.rede.armazem, cliente)
                    
                    if caminho_novo is None:
                        rotas_impossiveis += 1
                    elif caminho_original:
                        aumento_custo_total += max(0, custo_novo - custo_original)
            
            # Restaurar aresta com o custo salvo
            self.rede.grafo.add_edge(origem, destino, peso=custo_aresta, 
                                    custo=custo_aresta)
            
            nome_estrada = f"{origem[:6]}→{destino[:6]}"
            impactos.append((nome_estrada, rotas_impossiveis, aumento_custo_total))
        
        # Ordenar por impacto
        impactos.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        # Gráfico de barras
        if impactos:
            nomes = [i[0] for i in impactos]
            rotas_imp = [i[1] for i in impactos]
            custos = [i[2] for i in impactos]
            
            x = np.arange(len(nomes))
            width = 0.35
            
            ax.bar(x - width/2, rotas_imp, width, label='Rotas Impossíveis', 
                  color='red', alpha=0.7)
            ax2 = ax.twinx()
            ax2.bar(x + width/2, custos, width, label='Aumento Custo', 
                   color='orange', alpha=0.7)
            
            ax.set_xlabel('Estradas', fontsize=10)
            ax.set_ylabel('Rotas Impossíveis', fontsize=10, color='red')
            ax2.set_ylabel('Aumento de Custo', fontsize=10, color='orange')
            ax.set_xticks(x)
            ax.set_xticklabels(nomes, rotation=45, ha='right', fontsize=8)
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')
            ax.grid(True, alpha=0.3, axis='y')
        
        ax.set_title('Análise de Impacto de Falhas', fontsize=12, fontweight='bold')
    
    def _plotar_comparacao_rotas(self, ax):
        """Plota comparação de diferentes rotas."""
        if not self.rede.armazem or not self.rede.clientes:
            ax.axis('off')
            return
        
        cliente = self.rede.clientes[0]
        rotas = self.rede.comparar_rotas(self.rede.armazem, cliente)
        
        if rotas:
            # Pegar top 5 rotas
            top_rotas = rotas[:5]
            custos = [r[1] for r in top_rotas]
            indices = [f"Rota {i+1}" for i in range(len(top_rotas))]
            
            cores = plt.cm.viridis(np.linspace(0, 1, len(top_rotas)))
            ax.barh(indices, custos, color=cores, alpha=0.7, edgecolor='black')
            
            # Adicionar valores
            for i, (idx, custo) in enumerate(zip(indices, custos)):
                ax.text(custo, i, f' {custo:.0f}', va='center', fontsize=9)
            
            ax.set_xlabel('Custo', fontsize=10)
            ax.set_title(f'Top 5 Rotas\n{self.rede.armazem} → {cliente}', 
                        fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
        else:
            ax.text(0.5, 0.5, 'Nenhuma rota\nencontrada', 
                   ha='center', va='center', fontsize=11)
            ax.axis('off')
    
    def _plotar_topologia(self, ax):
        """Plota informações sobre topologia da rede."""
        G = self.rede.grafo
        
        # Calcular métricas
        num_nos = G.number_of_nodes()
        num_arestas = G.number_of_edges()
        densidade = nx.density(G)
        
        # Componentes fortemente conectados
        componentes = list(nx.strongly_connected_components(G))
        maior_componente = max(componentes, key=len) if componentes else set()
        
        texto = f"""
TOPOLOGIA DA REDE

Cidades: {num_nos}
Estradas: {num_arestas}
Densidade: {densidade:.3f}

Componentes: {len(componentes)}
Maior componente: {len(maior_componente)} cidades

Grau médio entrada: {sum(dict(G.in_degree()).values())/num_nos:.2f}
Grau médio saída: {sum(dict(G.out_degree()).values())/num_nos:.2f}
        """
        
        ax.text(0.1, 0.5, texto, fontsize=9, verticalalignment='center',
               family='monospace', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Topologia', fontsize=11, fontweight='bold')
    
    def _plotar_metricas(self, ax):
        """Plota métricas de performance."""
        if not self.rede.armazem:
            ax.axis('off')
            return
        
        metricas = []
        valores = []
        
        # Calcular métricas
        custos_rotas = []
        for cliente in self.rede.clientes:
            _, custo = self.rede.calcular_caminho_minimo_manual(
                self.rede.armazem, cliente)
            if custo:
                custos_rotas.append(custo)
        
        if custos_rotas:
            metricas = ['Custo Médio', 'Custo Mín', 'Custo Máx']
            valores = [np.mean(custos_rotas), min(custos_rotas), max(custos_rotas)]
            
            cores = ['skyblue', 'lightgreen', 'lightcoral']
            ax.bar(metricas, valores, color=cores, alpha=0.7, edgecolor='black')
            
            # Adicionar valores
            for i, (metrica, valor) in enumerate(zip(metricas, valores)):
                ax.text(i, valor, f'\n{valor:.0f}', ha='center', va='bottom', fontsize=9)
            
            ax.set_ylabel('Custo', fontsize=10)
            ax.set_title('Métricas de Performance', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
        else:
            ax.axis('off')
    
    def _plotar_cidades_criticas(self, ax):
        """Plota análise de cidades críticas."""
        G = self.rede.grafo
        
        cidades_criticas = []
        for cidade in G.nodes():
            grau_entrada = G.in_degree(cidade)
            grau_saida = G.out_degree(cidade)
            if grau_entrada <= 1 or grau_saida <= 1:
                cidades_criticas.append((cidade, grau_entrada, grau_saida))
        
        if cidades_criticas:
            nomes = [c[0][:10] for c in cidades_criticas]
            entrada = [c[1] for c in cidades_criticas]
            saida = [c[2] for c in cidades_criticas]
            
            x = np.arange(len(nomes))
            width = 0.35
            
            ax.bar(x - width/2, entrada, width, label='Entrada', 
                  color='coral', alpha=0.7)
            ax.bar(x + width/2, saida, width, label='Saída', 
                  color='steelblue', alpha=0.7)
            
            ax.set_xlabel('Cidades', fontsize=10)
            ax.set_ylabel('Grau', fontsize=10)
            ax.set_xticks(x)
            ax.set_xticklabels(nomes, rotation=45, ha='right', fontsize=8)
            ax.legend(fontsize=8)
            ax.set_title('Cidades Críticas', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
        else:
            ax.text(0.5, 0.5, 'Nenhuma cidade\ncrítica encontrada', 
                   ha='center', va='center', fontsize=10)
            ax.axis('off')
    
    def _plotar_analise_custos(self, ax):
        """Plota análise detalhada de custos."""
        custos = [self.rede.grafo[u][v]['custo'] for u, v in self.rede.grafo.edges()]
        
        # Box plot e histograma lado a lado
        ax1 = ax
        ax2 = ax.twinx()
        
        # Histograma
        n, bins, patches = ax1.hist(custos, bins=min(12, len(custos)), 
                                   edgecolor='black', color='skyblue', 
                                   alpha=0.6, label='Distribuição')
        ax1.set_xlabel('Custo', fontsize=11)
        ax1.set_ylabel('Frequência', fontsize=11, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # Box plot (sobreposto)
        bp = ax2.boxplot([custos], positions=[len(custos)//2], widths=len(custos)*0.1,
                        patch_artist=True, vert=False)
        bp['boxes'][0].set_facecolor('red')
        bp['boxes'][0].set_alpha(0.3)
        ax2.set_ylabel('Box Plot', fontsize=11, color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        
        # Estatísticas
        stats_text = f"Média: {np.mean(custos):.1f}\nMediana: {np.median(custos):.1f}\nDesvio: {np.std(custos):.1f}"
        ax1.text(0.98, 0.98, stats_text, transform=ax1.transAxes,
                fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
        
        ax1.set_title('Análise Detalhada de Custos', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
    
    def salvar(self, nome='dashboard_avancado.png'):
        """Salva o dashboard."""
        if self.fig:
            self.fig.savefig(nome, dpi=300, bbox_inches='tight')
            print(f"✓ Dashboard avançado salvo em: {nome}")
    
    def mostrar(self):
        """Exibe o dashboard."""
        if self.fig:
            plt.show()


def main():
    """Função principal."""
    print("="*60)
    print("DASHBOARD AVANÇADO - ANÁLISE DETALHADA")
    print("="*60)
    
    rede = criar_rede_exemplo()
    dashboard = DashboardAvancado(rede)
    dashboard.criar_dashboard()
    dashboard.salvar()
    dashboard.mostrar()
    
    print("\n✓ Dashboard avançado criado!")


if __name__ == "__main__":
    main()

