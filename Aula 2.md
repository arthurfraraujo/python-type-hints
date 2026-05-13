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

---

## O que é o _Callable_?

No Python, "Callable" significa, literalmente, algo que pode ser chamado (como uma função ou um método). Quando você usa Callable nos Type Hints, você está dizendo: _"Eu não quero apenas um dado (como um número ou texto), eu quero receber uma função como argumento"_.

### Código de exemplo:

```python
def with_callback(x: float, y: float, callback: Callable[[...], None]) -> float:
    result = x + y
    callback(f"{result = }", 1, 2, 3, 4, 5)
    return x + y
```

### 1. A Anatomia do `Callable[[...], None]`

O `Callable` geralmente recebe dois grupos de informações dentro dos colchetes:

1. **O que vem primeiro (entre colchetes):** São os tipos dos argumentos que a função deve receber.
2. **O que vem depois da vírgula:** É o tipo do que a função retorna.

No seu print, aparece assim: `Callable[..., None]`

* **As reticências (`...`):** Significam "não me importa quantos ou quais argumentos essa função recebe". É um jeito de ser flexível.
* **O `None`:** Significa que a função que for passada **não deve retornar nada** (ou retornar `None`). Ela é usada apenas para executar uma ação, como um `print`.

### 2. Na prática: O que o `with_callback` faz?

Imagine que o `with_callback` é um chefe de obra.

* Ele recebe dois números (`x` e `y`).
* Ele faz o cálculo: `result = x + y`.
* Mas ele tem um assistente (o `callback`). O chefe não quer saber como o assistente trabalha, ele só dá uma ordem: *"Ei, assistente, tome aqui o resultado e esses números extras e faça o seu trabalho!"*.

```python
callback(f"{result = }", 1, 2, 3, 4, 5)

```

O `with_callback` não sabe se o `callback` vai imprimir isso na tela, salvar num arquivo ou mandar um e-mail. Ele só sabe que **pode chamar** aquela variável como se fosse uma função.

### 3. Por que isso é útil? (A funcionalidade)

Isso serve para criar códigos **genéricos** e **reutilizáveis**.

Se você não usasse `Callable`, você teria que escrever o `print` direto dentro da função. Com o `Callable`, você permite que quem usar a sua função decida o que fazer com o resultado.

---

## Limitação do Callable

Apesar de ser ótimo para tipar argumentos posicionais, o Callable falha quando tem que tipar argumentos nomeados. **Callable é posicional por natureza.**

### Exemplo de erro:

```python
from typing import Callable

# Esta função EXIGE argumentos nomeados
def minha_funcao(*, nome: str, idade: int) -> None:
    print(nome, idade)

# Se eu tentar tipar um callback para ela:
def executor(callback: Callable[[str, int], None]):
    # O Callable acha que vai chamar assim: callback("João", 30)
    # Mas a função exige: callback(nome="João", idade=30)
    callback("João", 30)
```

O verificador de tipos vai reclamar. O ```Callable``` não consegue garantir que o nome do parâmetro seja ```nome``` ou ```idade```. Ele só garante que o primeiro é ```str``` e o segundo é ```int```.

### A solução: ```Protocol```(Tipagem Estrutural)

Quando o ```Callable``` fica curto demais para o que você precisa, o Python oferece o ```Protocol```. Ele é como uma "interface" que permite descrever a assinatura completa da função, incluindo os nomes dos argumentos.

> Será abordado com mais detalhes nas próximas aulas e por isso não aprofundarei os estudos no ```Protocol``` por enquanto.

---

## Dunder Methods (abreviação de Double Underscore)

São os **protocolos internos do Python**. Eles permitem que suas próprias classes se comportem como objetos nativos da linguagem.

- O que são: São nomes reservados que o Python chama "por baixo dos panos" em situações específicas.

- **Exemplos comuns:**

    - ```__init__```: Chamado quando você cria uma instância (```Classe()```).
    - ```__str__```: Chamado quando você dá um ```print(objeto)```.
    - ```__len__```: Chamado quando você faz ```len(objeto)```.
    - ```__call__```: Chamado quando você trata o objeto como uma função (```objeto()```).

> Para ter acesso aos outros protocolos internos do Python, acesse ()[]