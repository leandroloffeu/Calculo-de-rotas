# Programa de Otimização de Rotas de Entrega

Este programa modela uma rede de distribuição de mercadorias entre cidades, utilizando grafos para calcular rotas otimizadas e analisar a robustez da rede.

## 📋 Descrição

O programa implementa um sistema completo de análise de rotas de entrega que:

- **Modela a rede** como um grafo direcionado usando NetworkX
- **Calcula caminhos mínimos** usando método manual (busca em profundidade)
- **Simula falhas** em estradas e encontra rotas alternativas
- **Analisa robustez** identificando estradas e cidades críticas
- **Visualiza resultados** com gráficos usando Matplotlib
- **Gera relatórios** com todas as análises

## 🚀 Instalação

1. Certifique-se de ter Python 3.7 ou superior instalado

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📦 Dependências

- `networkx`: Para criação e manipulação de grafos
- `matplotlib`: Para visualização dos grafos

## 🎯 Uso

### Programa Principal

Execute o programa principal:

```bash
python otimizacao_rotas.py
```

O programa irá:
1. Criar uma rede de distribuição de exemplo (com cidades brasileiras)
2. Executar todas as 5 partes do exercício
3. Gerar visualizações em PNG
4. Gerar um relatório em texto

### Dashboard Interativo

Execute o dashboard básico:

```bash
python dashboard.py
```

Este dashboard mostra:
- Visão geral da rede
- Estatísticas
- Caminhos mínimos
- Análise de robustez
- Distribuição de custos
- Centralidade das cidades

### Dashboard Avançado

Execute o dashboard avançado com análises detalhadas:

```bash
python dashboard_avancado.py
```

Este dashboard inclui:
- Rede com todos os caminhos mínimos destacados
- Tabela de rotas
- Matriz de custos
- Análise de falhas
- Comparação de rotas
- Topologia da rede
- Métricas de performance
- Cidades críticas
- Análise detalhada de custos

## 📊 Estrutura do Programa

### Parte 1: Representação do Grafo
- Cria o grafo com cidades e estradas
- Visualiza a rede completa

### Parte 2: Cálculo de Caminho Mínimo
- Calcula manualmente o caminho de menor custo entre armazém e clientes
- Destaca o caminho mínimo no gráfico

### Parte 3: Caminhos Alternativos
- Simula a falha de uma estrada
- Encontra rotas alternativas
- Visualiza o impacto da falha

### Parte 4: Análise de Robustez
- Identifica estradas críticas
- Identifica cidades críticas
- Analisa o impacto de falhas

### Parte 5: Comparação de Resultados
- Compara diferentes rotas possíveis
- Calcula estatísticas da rede
- Analisa centralidade das cidades

## 🏙️ Rede de Exemplo

A rede de exemplo inclui:
- **Armazém**: São Paulo
- **Cidades Intermediárias**: Campinas, Ribeirão Preto, Sorocaba
- **Clientes**: Rio de Janeiro, Belo Horizonte, Curitiba

## 📁 Arquivos Gerados

Após a execução, os seguintes arquivos serão criados:

- `parte1_rede_distribuicao.png` - Visualização da rede completa
- `parte2_caminho_minimo.png` - Caminho mínimo destacado
- `parte3_rotas_alternativas.png` - Rotas após falha
- `parte4_analise_robustez.png` - Análise de robustez
- `relatorio.txt` - Relatório completo em texto

## 🔧 Personalização

Para criar sua própria rede, modifique a função `criar_rede_exemplo()` ou crie uma nova função:

```python
def criar_sua_rede():
    rede = RedeDistribuicao()
    
    # Adicionar cidades
    rede.adicionar_cidade("SuaCidade1", tipo='armazem')
    rede.adicionar_cidade("SuaCidade2", tipo='cliente')
    
    # Adicionar estradas
    rede.adicionar_estrada("SuaCidade1", "SuaCidade2", custo=100)
    
    return rede
```

## 📝 Notas

- Os custos das estradas podem representar distância, tempo, custo de combustível, etc.
- O método de cálculo de caminho mínimo é manual (busca em profundidade), não usa algoritmos avançados como Dijkstra
- A análise de robustez identifica pontos críticos que podem afetar a operação da rede

## 👥 Autores

Desenvolvido para exercício acadêmico sobre otimização de rotas e análise de grafos.


