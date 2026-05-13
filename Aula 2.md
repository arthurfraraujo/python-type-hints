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

Segura esse ímpeto de cientista, porque vamos transformar essas anotações em um verdadeiro manual de engenharia reversa do Python.

Para aprofundar, você precisa entender que os **Dunder Methods** não são apenas "nomes reservados"; eles são a **interface de baixo nível** que o Python usa para tudo. No C, você teria que manipular ponteiros de estrutura; no Python, você implementa um Dunder.

Aqui está uma versão "turbinada" das suas anotações, categorizada por funcionalidade para facilitar seu próximo surto de produtividade:

---

## Dunder Methods

Os Dunder Methods (ou *Magic Methods*) são a implementação do **Python Data Model**. Eles permitem o **Operator Overloading** (Sobrecarga de Operadores), fazendo com que suas classes customizadas integrem-se perfeitamente à sintaxe da linguagem.

### 1. Ciclo de Vida do Objeto

Controlam como um objeto nasce e morre.

* **`__new__`**: O verdadeiro construtor. Ele cria a instância na memória. (Raro de usar, mas essencial para entender como objetos surgem).
* **`__init__`**: O inicializador. Ele recebe a instância já criada e define os atributos iniciais.
* **`__del__`**: O finalizador. Chamado quando o objeto é coletado pelo Garbage Collector.

### 2. Representação e Depuração (Debug)

Como o seu objeto se mostra para o mundo.

* **`__str__`**: Focado no usuário final. O que aparece no `print()` ou `str()`. Deve ser legível.
* **`__repr__`**: Focado no desenvolvedor. Deve ser "não ambíguo". Idealmente, se você copiar o que o `__repr__` retorna e colar no terminal, você recria o objeto.
* *Dica de Ouro:* Se você não definir `__str__`, o Python usa o `__repr__` como reserva.



### 3. Protocolos de Coleção e Sequência

Faz sua classe fingir que é uma lista, dicionário ou tupla.

* **`__len__`**: Chamado por `len(obj)`. Deve retornar um inteiro.
* **`__getitem__`**: Permite acesso por colchetes `obj[index]`. Você pode fazer um objeto que busca no banco de dados fingindo ser uma lista!
* **`__iter__`** e **`__next__`**: Permitem que seu objeto seja usado em um laço `for`.

### 4. Operações Matemáticas e Comparação

Dão significado a símbolos como `+`, `-`, `==`, `<`.

* **`__add__`**: Define o que o sinal de `+` faz. (Ex: Somar dois vetores ou concatenar dois relatórios).
* **`__eq__`**: Define o que `==` significa para o seu objeto. Sem ele, o Python compara apenas o endereço de memória.
* **`__lt__`**, **`__gt__`**: Permitem usar `<` e `>` (essenciais para que o `sort()` funcione automaticamente na sua classe).

### 5. O Protocolo de Chamada (Callable)

* **`__call__`**: Permite que a instância seja "chamada" como uma função: `obj()`.
* *Por que usar?* É útil para manter estado entre chamadas (uma função que "lembra" quantas vezes foi usada, por exemplo).



---

### Exemplo

Olha como esses métodos transformam uma classe simples em algo que parece nativo:

```python
class Playlist:
    def __init__(self, musicas):
        self.musicas = musicas

    def __len__(self):
        return len(self.musicas)

    def __getitem__(self, posicao):
        return self.musicas[posicao]

rock = Playlist(['Bohemian Rhapsody', 'Stairway to Heaven'])

print(len(rock))    # Usa __len__ -> 2
print(rock[0])      # Usa __getitem__ -> 'Bohemian Rhapsody'
for m in rock:      # O Python entende como iterar usando o __getitem__!
    print(m)

```

---

### Importante: Diferença entre ```def``` e ```lambda```.

- ```def```: Define um objeto do tipo ```function```, que possui nativamente o método ```__call__``` herdado da classe ```function```. Esse objeto é o que chamamos de função nomeada.

    - **Características:** Requer obrigatoriamente um **nome** (identificador) e o uso da palavra-chave **return** para devolver um valor (caso contrário, retorna None por padrão).

    - **Sintaxe:** Possui um bloco de código identado, permitindo múltiplas instruções e lógica complexa.

    - **Exemplo:**

    ```python
    def my_function(x: int, y:int) -> int:
        return x + y
    ```

- ```lambda```: Também define um objeto do tipo ```function``` com o método ```__call__```, contudo, ele é **anônimo** (não possui nome próprio no momento da criação).

    - **Características:** Possui sintaxe minimalista para execuções rápidas. Não utiliza a palavra-chave ```return```; o resultado da expressão após os dois-pontos é **retornado implicitamente**.

    - **Limitação:** É restrito a uma única expressão (apenas uma linha de lógica).

    - **Sintaxe:** ```lambda argumentos: expressão```

    - **Exemplo:**

    ```python
    soma = lambda x, y: x + y
    print(f"Resultado da soma: {soma(5, 5)}")

    # Ou chamada direta (Immediately Invoked Function Expression):
    print(f"Soma direta: {(lambda x, y: x + y)(5, 5)}")
    ```
---

## Static Duck Typing (Tipagem de Pato Estática)

O **Static Duck Typing** é a evolução do "Duck Typing" tradicional do Python. Ele permite que o código mantenha a liberdade do Python (comportamento > herança) com a segurança de linguagens estáticas (checagem antes de rodar).

### 1. O Conceito (Filosofia)

> *"Se ele caminha como um pato e grasna como um pato, então é um pato."*

Diferente de C ou Java, o Python não foca na **Identidade** do objeto (quem ele é/de quem ele herda), mas sim no seu **Comportamento** (o que ele sabe fazer).

* **Tipagem Nominal (C++/Java):** O objeto só é aceito se herdar explicitamente da classe pai exigida. (Relação de "Sangue").
* **Tipagem Estrutural/Duck Typing (Python):** O objeto é aceito se possuir os métodos e atributos necessários. (Relação de "Capacidade").

---

### 2. O Instrumento: `typing.Protocol`

Para que essa forma de trabalhar não cause erros em tempo de execução, usamos o `Protocol` para criar um **Contrato de Comportamento**.

* **Contrato Implícito:** Você define o `Protocol`, mas as classes que o "seguem" **não precisam herdar dele**.
* **Checagem Estática:** Ferramentas como o Mypy ou o VS Code analisam se a classe possui os métodos definidos no `Protocol`. Se tiver, ela é considerada compatível.

#### Exemplo Prático:

```python
from typing import Protocol

# 1. Defino o molde (O contrato)
class Instrumento(Protocol):
    def fazer_som(self) -> None: ...

# 2. Crio classes independentes (Sem herança!)
class Violao:
    def fazer_som(self): print("Som de cordas")

class Piano:
    def fazer_som(self): print("Som de teclas")

# 3. A função exige o protocolo, não a classe
def tocar_musica(i: Instrumento):
    i.fazer_som()

# Funciona! O Python checa a estrutura, não o nome.
tocar_musica(Violao()) 

```

---

### 3. Por que isso é Disruptivo? (A visão do "Ex-C")

* **Desacoplamento Total:** Você pode criar uma função que aceita objetos de bibliotecas que nem foram escritas ainda.
* **Inversão de Dependência:** A função define o que ela precisa (o Protocolo), e o mundo externo se vira para entregar algo que encaixe.
* **Dunder Methods como Cola:** O uso do `__call__` dentro de um `Protocol` permite que você trate objetos complexos como se fossem funções simples, unificando o comportamento de classes e funções.

---

### 4. Resumo

* **Sem Protocolo:** É o "Duck Typing" puro. Se o método não existir na hora de rodar, o programa quebra.
* **Com Protocolo:** É o "Static Duck Typing". O editor avisa se o "pato" é de mentira **antes** de você tentar fazê-lo grasnar.
* **Herança vs. Protocolo:** Use **Herança** quando quiser herdar código pronto. Use **Protocolo** quando quiser apenas exigir um comportamento.
