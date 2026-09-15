"""Resolucao do problema das N-rainhas usando BuscaProfundidade da biblioteca aigyminsper."""

from __future__ import annotations

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import BuscaProfundidade


class QueensState(State):
    """Estado do tabuleiro NxN.
    Representacao: uma rainha por linha, ja posicionada. `rainhas[i]` guarda a
    coluna onde a rainha da linha `i` foi colocada. Como so existe uma rainha
    por linha, rainhas na mesma linha nunca sao um problema; falta so checar
    coluna e diagonais. """

    def __init__( self, n: int, rainhas: list[int] | None = None, operator: str = "raiz",) -> None:
        super().__init__(operator)
        self.n = n
        if rainhas is None:
            rainhas = []
        self.rainhas: list[int] = rainhas

    def _coluna_segura(self, coluna: int) -> bool:
        """Verifica se colocar uma rainha nesta coluna (na proxima linha livre) e seguro.

        So compara com as rainhas que JA estao no tabuleiro (uma por linha 
        anterior); nao precisa olhar o tabuleiro inteiro de novo a cada vez.
        Duas casas estao na mesma diagonal quando a diferenca de linhas e
        igual a diferenca de colunas entre elas. Se achar qualquer conflito
        (mesma coluna ou mesma diagonal) com alguma rainha ja colocada, a
        posicao nao e segura.
        """
        proxima_linha = len(self.rainhas)

        # self.rainhas tem TODAS as rainhas ja colocadas (linha 0, 1, 2...
        # ate a anterior a esta) -- nao so a ultima. Esse for compara a
        # coluna nova contra cada uma delas, uma de cada vez.
        for linha, coluna_ocupada in enumerate(self.rainhas):
            if coluna_ocupada == coluna:
                mesma_coluna = True
            else:
                mesma_coluna = False

            diferenca_de_colunas = abs(coluna_ocupada - coluna)
            diferenca_de_linhas = abs(linha - proxima_linha)
            if diferenca_de_colunas == diferenca_de_linhas:
                mesma_diagonal = True
            else:
                mesma_diagonal = False

            if mesma_coluna or mesma_diagonal:
                return False
        # Chegou aqui so se o for terminou sem achar conflito com NENHUMA
        # das rainhas anteriores -- por isso a coluna e considerada segura.
        return True

    def successors(self) -> list[QueensState]:
        """Gera um estado filho para cada coluna segura na proxima linha.

        successors() representa "quais tabuleiros eu posso alcancar a partir
        deste?". Aqui isso significa: tentar colocar a proxima rainha (linha
        de baixo) em cada uma das N colunas, e manter so as tentativas que
        nao dao conflito com as rainhas anteriores. Cada estado devolvido e
        um "filho" na arvore de busca; a BuscaProfundidade da lib usa esse
        metodo pra saber pra onde ir a partir do estado atual. Se a proxima
        linha ja passou de N, o tabuleiro esta completo e nao ha filhos.
        """
        proxima_linha = len(self.rainhas)
        if proxima_linha >= self.n:
            return []

        estados_filhos = []
        for coluna in range(self.n):
            if not self._coluna_segura(coluna):
                continue

            # [*self.rainhas, coluna]: pega a lista INTEIRA de rainhas ja
            # colocadas e adiciona a nova no final -- o filho carrega o
            # historico completo, nao so a rainha que acabou de entrar.
            novas_rainhas = [*self.rainhas, coluna]
            operador = f"linha {proxima_linha} -> coluna {coluna}"
            estado_filho = QueensState(self.n, novas_rainhas, operador)
            estados_filhos.append(estado_filho)

        return estados_filhos

    def is_goal(self) -> bool:
        """Objetivo: uma rainha posicionada em cada linha do tabuleiro."""
        if len(self.rainhas) == self.n:
            return True
        else:
            return False

    def cost(self) -> int:
        """Custo de dar este passo. Todas as jogadas valem o mesmo, entao e sempre 1."""
        return 1

    def env(self) -> str:
        """Assinatura do estado, usada pela lib pra identificar/comparar estados."""
        return str(self.rainhas)

    def description(self) -> str:
        """Exigido pela classe abstrata State da lib; nada no codigo chama isso."""
        return f"Problema das {self.n}-rainhas"


def solve_all(n: int) -> list[list[int]]:
    """Enumera todas as solucoes percorrendo a arvore de estados de QueensState.

    BuscaProfundidade (aigyminsper) retorna apenas a primeira solucao encontrada;
    para navegar entre todas as solucoes (pygame), percorremos a mesma arvore de
    successors()/is_goal() ate o fim em vez de parar no primeiro goal.
    """
    solucoes: list[list[int]] = []

    def visitar(estado: QueensState) -> None:
        """Percorre a arvore de estados por backtracking: tenta uma escolha,
        segue em frente como se estivesse certa, e volta pra tentar outra
        se travar."""
        if estado.is_goal():
            # Tabuleiro completo: guarda essa solucao e nao desce mais a partir daqui.
            solucoes.append(estado.rainhas)
            return

        for filho in estado.successors():
            # Tenta esse filho como se fosse a escolha certa, chamando
            # visitar() de novo pra completar o resto a partir dele. Se
            # successors() tiver vindo vazio (nenhuma coluna segura), esse
            # for nem executa e a funcao ja termina aqui embaixo.
            visitar(filho)
        # Cada filho e um tabuleiro novo (successors() faz [*self.rainhas,
        # coluna], sem mexer no estado atual), entao nao precisa desfazer
        # nada: quando visitar(filho) termina, o for so segue pro proximo
        # filho da lista -- essa é a "volta" do backtracking.

    estado_inicial = QueensState(n)
    visitar(estado_inicial)
    return solucoes


def imprimir_tabuleiro(rainhas: list[int]) -> None:
    """Desenha o tabuleiro em texto: 'Q' onde tem rainha, '.' onde nao tem."""
    n = len(rainhas)

    for linha in range(n):
        casas_da_linha = []
        for coluna in range(n):
            # rainhas[linha] e a coluna da rainha dessa linha (a
            # representacao usada em QueensState); so bate com "coluna"
            # numa posicao por linha, que e onde a rainha esta
            if rainhas[linha] == coluna:
                casas_da_linha.append("Q")
            else:
                casas_da_linha.append(".")
        print(" ".join(casas_da_linha))

    print()


def main() -> None:
    """ Para cada N, acha uma solucao com BuscaProfundidade"""
    tamanhos_de_tabuleiro = (4, 5, 6, 7, 8)

    for n in tamanhos_de_tabuleiro:
        algoritmo = BuscaProfundidade()
        estado_inicial = QueensState(n)
        
        # m=n: limite de profundidade da busca. 
        # A solucao completa tem exatamente N rainhas (uma por linha), entao
        # nao precisa procurar mais fundo que isso.
        resultado = algoritmo.search(estado_inicial, m=n)

        print(f"N = {n}")
        if resultado is None:
            print("Nenhuma solucao encontrada.")
        else:
            # resultado e um Node da lib (nao um QueensState); o tabuleiro
            # em si esta em resultado.state.rainhas.
            print(f"Caminho: {resultado.show_path()}")
            imprimir_tabuleiro(resultado.state.rainhas)


if __name__ == "__main__":
    main()
