# Aula 3

## Introdução a Teoria dos Tipos

**O que é:** De forma simplificada, é um sistema formal na matemática e na lógica que classifica "coisas" (termos) em "categorias" (tipos).

No C, você vê tipos como tamanhos de memória (```int``` é 4 bytes). Na Teoria dos Tipos, um tipo é muito mais do que isso: **é um modelo de comportamento e uma prova lógica.**

### 1. A Origem: Resolvendo o "Bug" da Matemática

A Teoria dos Tipos nasceu com **Bertrand Russell** no início do século XX. Ele descobriu que a Teoria dos Conjuntos tinha um erro lógico grave (o Paradoxo de Russell).

Para resolver, ele propôs: "Não podemos simplesmente colocar qualquer coisa em qualquer conjunto. Precisamos de uma **hierarquia**".

* Um "Tipo 0" são indivíduos.
* Um "Tipo 1" são conjuntos de indivíduos.
* Você não pode misturá-los sem regras estritas.

---

### 2. A Conexão com a Computação (Curry-Howard)

Aqui é onde o seu "Eureka" vai explodir. Existe algo chamado **Isomorfismo de Curry-Howard**. Ele prova que:

* Um **Tipo** é o equivalente a uma **Proposição Matemática**.
* Um **Programa** (o código) é o equivalente a uma **Prova**.

Quando você define um `Protocol` no Python ou uma `struct` no C, você está definindo um teorema. Quando o código compila ou passa pelo verificador de tipos (Mypy), o computador está dizendo: **"Eu provei matematicamente que esse programa é logicamente consistente"**.

---

### 3. Os Níveis de "Poder" dos Tipos

A Teoria dos Tipos classifica as linguagens em um espectro de poder (o famoso **Lambda Cubo**):

* **Tipos Simples:** Como o C. Você tem `int`, `char`, e é isso.
* **Polimorfismo (Generics):** A capacidade de uma função aceitar tipos variados (o que o `Protocol` ajuda a fazer).
* **Tipos Dependentes:** O nível "deus". O tipo pode depender de um valor. Ex: Um tipo que não é apenas `Lista`, mas `Lista de tamanho 5`. Se você tentar adicionar o 6º elemento, o código nem compila porque a "prova matemática" falha.

---

## Revisitando o conceito de Classes no Python

* ```Classes``` são fábricas de ```objetos```. Elas funcionam como moldes para gerar novas estruturas de dados na linguagem.
* **Por exemplo:** Ao criar a ```classe``` "Animal", o que você fez foi criar uma nova fábrica de ```objetos``` do tipo "Animal".
* Tudo o que foi definido em "Animal" (o molde), será passado para os ```objetos``` fabricados pela ```classe``` "Animal".
* Esses ```objetos``` agora são chamados de ```instâncias``` da ```classe``` "Animal".
* Um "Dog" criado por "Animal" é uma ```instância``` de "Animal". Assim como um "Cat".
* Dentro da ```classe```, podemos nos referir à ```instância``` que está sendo criada usando a palavra ```self```.
* **Resumo:** ```Classe``` → Molde (a fábrica) | ```Instância``` → O que foi fabricado pela classe.

## Exemplos

### Simples

```python
class Animal:
    def __init__(self, name: str) -> None:
        # Cria o atributo 'name' e inicializa com o valor passado
        self.name: str = name

    def set_name(self, name: str) -> None:
        # Atualiza o atributo 'name' com um novo valor
        self.name = name

if __name__ == "__main__":
    # Cria uma instância da classe Animal com nome "Dog"
    dog = Animal("Dog")
    # Chama o método set_name para alterar o nome para "Apolo"
    dog.set_name("Apolo")

    # Exibe o valor atual do atributo 'name'
    print(f"{dog.name = !r}")

```

* **Características:** direto e funcional, mas sem validação. Qualquer tipo pode ser atribuído a ```name```.

## Básico

```python
class Animal:
    def __init__(self, name: str) -> None:
        # Usa '_name' como atributo "privado" (convenção de underscore)
        self._name: str = name

    @property
    def name(self) -> str:
        # Getter: permite acessar '_name' como se fosse um atributo público
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        # Setter: valida o tipo antes de atualizar '_name'
        if not isinstance(value, str):
            raise TypeError("O nome deve ser uma string")
        self._name = value


if __name__ == "__main__":
    # Cria instância com nome inicial "Dog"
    dog = Animal("Dog")
    # Altera o nome usando a propriedade (parece um atributo, mas passa pelo setter)
    dog.name = "Apolo" 

    # Exibe o valor atualizado
    print(f"{dog.name = !r}")
```

* **Características:** encapsulamento com ```@property```, validação de tipo, interface mais limpa. Evita atribuições incorretas.

## Sofisticado

```python
from dataclasses import dataclass

@dataclass
class Animal:
    # Atributo tipado; o __init__ é gerado automaticamente pela dataclass
    name: str  

    def __post_init__(self):
        # Validação automática logo após a criação do objeto
        if not isinstance(self.name, str):
            raise TypeError("O nome deve ser uma string")

    @property
    def name(self) -> str:
        # Getter personalizado (sobrescreve o gerado pela dataclass)
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        # Setter com validação de tipo
        if not isinstance(value, str):
            raise TypeError("O nome deve ser uma string")
        self._name = value


if __name__ == "__main__":
    # Cria instância com nome inicial "Dog"
    dog = Animal("Dog")
    # Altera o nome usando a propriedade
    dog.name = "Apolo" 

    # Exibe o valor atualizado
    print(f"{dog.name = !r}")
```

* **Características:** uso de ```dataclass``` para reduzir _boilerplate_, validação com ```__post_init__```, propriedades para controle.
