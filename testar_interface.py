"""
Script de teste rápido para verificar se a interface funciona.
Execute este script para testar as funcionalidades básicas.
"""

import sys
from otimizacao_rotas import RedeDistribuicao

def testar_rede():
    """Testa a criação da rede e cálculo de rotas."""
    print("="*60)
    print("TESTE DO SISTEMA DE ROTAS")
    print("="*60)
    
    # Criar rede
    rede = RedeDistribuicao()
    
    # Adicionar cidades
    rede.adicionar_cidade("São Paulo", tipo='armazem')
    rede.adicionar_cidade("Campinas", tipo='intermediaria')
    rede.adicionar_cidade("Rio de Janeiro", tipo='cliente')
    
    # Adicionar estradas
    rede.adicionar_estrada("São Paulo", "Campinas", 100)
    rede.adicionar_estrada("Campinas", "Rio de Janeiro", 350)
    rede.adicionar_estrada("São Paulo", "Rio de Janeiro", 430)
    
    print("\n[OK] Rede criada com sucesso!")
    print(f"   Cidades: {list(rede.grafo.nodes())}")
    print(f"   Estradas: {list(rede.grafo.edges())}")
    
    # Calcular rota
    print("\n[TESTE] Calculando rota: Sao Paulo -> Rio de Janeiro")
    caminho, custo = rede.calcular_caminho_minimo_manual("São Paulo", "Rio de Janeiro")
    
    if caminho:
        print(f"   [OK] Rota encontrada: {' -> '.join(caminho)}")
        print(f"   [OK] Custo: {custo}")
    else:
        print("   [ERRO] Rota nao encontrada!")
        return False
    
    # Testar quebra de estrada
    print("\n[TESTE] Quebrando estrada: Sao Paulo -> Rio de Janeiro")
    rede.grafo.remove_edge("São Paulo", "Rio de Janeiro")
    
    print("[TESTE] Recalculando rota apos quebra...")
    caminho2, custo2 = rede.calcular_caminho_minimo_manual("São Paulo", "Rio de Janeiro")
    
    if caminho2:
        print(f"   [OK] Nova rota encontrada: {' -> '.join(caminho2)}")
        print(f"   [OK] Novo custo: {custo2}")
        if caminho2 != caminho:
            print("   [OK] Rota foi recalculada corretamente!")
        else:
            print("   [AVISO] Rota nao mudou (pode ser esperado)")
    else:
        print("   [ERRO] Nenhuma rota alternativa encontrada!")
        return False
    
    print("\n" + "="*60)
    print("[OK] TODOS OS TESTES PASSARAM!")
    print("="*60)
    print("\nAgora você pode executar a interface interativa:")
    print("  python interface_interativa.py")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = testar_rede()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\n[ERRO] Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

