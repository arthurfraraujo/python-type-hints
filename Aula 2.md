# Aula 2

> É crucial tipar todo o cabeçalho de qualquer função.

## O que são genéricos e variantes no contexto de tipos do Python?

Genéricos e Variantes são conceitos que permitem criar funções e classes flexíveis que mantêm a segurança de tipos sem "engessar" o código.

### 1. Genéricos

Genéricos permitem que você escreva uma estrutura (como uma lista ou uma classe) que pode lidar com qualquer tipo, mas que "lembra" qual tipo foi usado nela.

Antes dos genéricos, se você definisse uma lista, o Python não sabia se ela continha apenas inteiros ou uma mistura de coisas. Com Genéricos, usamos o objeto TypeVar para criar um "espaço reservado".

```python
from typing import TypeVar, Generic

T = TypeVar('T')  # T pode ser qualquer coisa

def obter_primeiro(lista: list[T]) -> T:
    return lista[0]

# Se eu passar uma lista de int, o Python sabe que o retorno é int
# Se eu passar uma lista de str, o Python sabe que o retorno é str
```

### 2. Variância (Covariância e Contravariância)

A variância descreve como a relação entre tipos base (como `Animal` e `Cachorro`) se traduz para a relação entre tipos genéricos que os utilizam (como `Lista[Animal]` e `Lista[Cachorro]`).

**A) Invariância (Padrão)**

Por padrão, a maioria das classes no Python é **invariante**.
Se `Cachorro` herda de `Animal`, uma `Lista[Cachorro]` **não** é considerada uma `Lista[Animal]` pelo verificador de tipos (como o Mypy).

* **Por que?** Porque se você tratar uma lista de cachorros como uma lista de animais, você poderia tentar inserir um `Gato` nela, o que quebraria a lógica da lista original.

**B) Covariância (`covariant=True`)**

Um tipo é covariante quando a relação de subtipo é mantida. Se `Cachorro` é um `Animal`, então `Caixa[Cachorro]` é um subtipo de `Caixa[Animal]`.

* **Onde usar:** Geralmente em estruturas de **leitura apenas** (imutáveis), como tuplas.

**C) Contravariância (`contravariant=True`)**

É o oposto. A relação de subtipo é invertida. Se `Cachorro` é um `Animal`, um `Processador[Animal]` é considerado um subtipo de `Processador[Cachorro]`.

* **Onde usar:** Geralmente em **argumentos de funções** ou classes que apenas "recebem" dados. Se algo sabe processar qualquer animal, certamente sabe processar um cachorro.

---

### Resumo Comparativo

| Conceito | O que define | Uso comum |
| --- | --- | --- |
| **Genérico** | Define um componente que aceita tipos variados com segurança. | `list[T]`, `dict[K, V]` |
| **Invariante** | O tipo genérico deve ser exato; não aceita pais nem filhos. | `list[int]` |
| **Covariante** | Aceita o tipo definido ou qualquer **subtipo** (filho). | `Sequence[Animal]` |
| **Contravariante** | Aceita o tipo definido ou qualquer **supertipo** (pai). | `Callable[[Animal], None]` |

---

### O que é segurança de tipos?

A segurança de tipos (ou _type safety_) é um conceito na ciência da computação que define o quanto uma linguagem de programação evita ou previne erros relacionados aos tipos de dados.

Em termos simples: é o conjunto de regras que garante que o seu código não tente tratar um número como um texto, ou um arquivo como uma função, o que geralmente causaria um travamento ou comportamentos imprevisíveis.