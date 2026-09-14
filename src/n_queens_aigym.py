"""Resolucao do problema das N-rainhas usando BuscaProfundidade da biblioteca aigyminsper."""

from __future__ import annotations

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import BuscaProfundidade


class QueensState(State):
    """Estado do tabuleiro NxN: uma rainha por linha ja posicionada em `columns`."""

    def __init__(self, n: int, columns: list[int] | None = None, operator: str = "raiz") -> None:
        super().__init__(operator)
        self.n = n
        self.columns: list[int] = columns if columns is not None else []

    def _is_safe(self, col: int) -> bool:
        row = len(self.columns)
        for r, c in enumerate(self.columns):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def successors(self) -> list[QueensState]:
        row = len(self.columns)
        if row >= self.n:
            return []
        return [
            QueensState(self.n, [*self.columns, col], f"linha {row} -> coluna {col}")
            for col in range(self.n)
            if self._is_safe(col)
        ]

    def is_goal(self) -> bool:
        return len(self.columns) == self.n

    def cost(self) -> int:
        return 1

    def env(self) -> str:
        return str(self.columns)

    def description(self) -> str:
        return f"Problema das {self.n}-rainhas"


def solve_all(n: int) -> list[list[int]]:
    """Enumera todas as solucoes percorrendo a arvore de estados de QueensState.

    BuscaProfundidade (aigyminsper) retorna apenas a primeira solucao encontrada;
    para navegar entre todas as solucoes (pygame), percorremos a mesma arvore de
    successors()/is_goal() ate o fim em vez de parar no primeiro goal.
    """
    solutions: list[list[int]] = []

    def visit(state: QueensState) -> None:
        if state.is_goal():
            solutions.append(state.columns)
            return
        for successor in state.successors():
            visit(successor)

    visit(QueensState(n))
    return solutions


def print_board(columns: list[int]) -> None:
    n = len(columns)
    for row in range(n):
        line = ["Q" if columns[row] == col else "." for col in range(n)]
        print(" ".join(line))
    print()


def main() -> None:
    for n in (4, 5, 6, 7, 8):
        algoritmo = BuscaProfundidade()
        resultado = algoritmo.search(QueensState(n), m=n)
        print(f"N = {n}")
        if resultado is None:
            print("Nenhuma solucao encontrada.")
        else:
            print(f"Caminho: {resultado.show_path()}")
            print_board(resultado.state.columns)


if __name__ == "__main__":
    main()
