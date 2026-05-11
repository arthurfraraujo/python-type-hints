from typing import Final


def main() -> None:
    nome: str = "Arthur"
    x: int = 22
    y: float = 3.14
    c: complex = 1 + 2j
    is_valid: bool = True
    data: bytes = b"Hello, World!"

    constante: Final[str] = "Valor constante"

    lista_numeros: list[int] = [1, 2, 3, 4, 5]
    tupla_dois_valores: tuple[str, int] = ("Valor", 234)
    tupla_varios_valores: tuple[str, ...] = ("Valor", "...", "A", "B", "C")
    conjunto_numeros: set[int] = {1, 2, 3, 4, 5}
    conjunto_imutavel: frozenset[int] = frozenset({1, 2, 3, 4, 5})
    dicionario: dict[str, int] = {"um": 1, "dois": 2, "três": 3}
    numeros = range(1, 11)

    nada: None = None
    qualquer_coisa: object = "Pode ser qualquer coisa"
    tipo: type[int] = int

    print(
        f"""
        Nome: {nome},
        Número inteiro: {x},
        Número de ponto flutuante: {y},
        Número complexo: {c},
        Booleano: {is_valid},
        Bytes: {data}
        Constante: {constante},
        Lista de números: {lista_numeros},
        Tupla de dois valores: {tupla_dois_valores},
        Tupla de vários valores: {tupla_varios_valores},
        Conjunto de números: {conjunto_numeros},
        Conjunto imutável: {conjunto_imutavel},
        Dicionário: {dicionario},
        Range de números: {list(numeros)},
        Valor None: {nada},
        Qualquer coisa: {qualquer_coisa},
        Tipo: {tipo}
        """
    )


if __name__ == "__main__":
    main()
