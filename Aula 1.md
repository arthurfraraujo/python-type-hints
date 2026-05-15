# Aula 1

## O que significa "_Type Hint_"?

No contexto geral, _Type Hint_ significa "fazer tipagem no código X", independente de como ela será feita.
Já em Python Moderno, chama-se _Type Annotations_, pois usa o sistema de _annotations_ do Python.

> Para possíveis dúvidas, verificar o [Glossário Relacionado](https://github.com/luizomf/typehints_python "Repositório de Type Hints do Otávio Miranda").

----

### Consideração importante

Acabei fazendo uma pequena confusão entre o _Ruff_ e o _Pyright_, assumindo que o ambos faziam a mesma coisa, mas não fazem. Abaixo detalho melhor a diferença dos dois.

- _**Ruff:**_ _linter_ e _formatter_. Responsável por corrigir (ou padronizar) o estilo do código e detectar problemas comuns, como imports errados e variáveis não utilizadas.

- _**Pyright:**_ _type checker_. Garante que as anotações de tipo sejam respeitadas e que valores errados não sejam aceitos (como em funções, por exemplo).

Dado o esclarecimento, podemos voltar ao fluxo normal da aula.

----

## Hierarquia dos tipos em Python

```Any
Any
├── Numéricos
│   ├── int
│   │   └── Literal[3], Literal[-1]
│   ├── float
│   │   └── Literal[3.14]
│   └── complex
│       └── Literal[1+2j]
│
├── Texto
│   └── str
│       └── Literal["ok"], Literal["cancel"]
│
├── Booleanos
│   └── bool
│       ├── Literal[True]
│       └── Literal[False]
│
├── Nulo
│   └── NoneType
│       └── Literal[None]
│
├── Sequências
│   ├── list[T]
│   ├── tuple[T1, T2, ...]
│   │   └── Literal[(1, "a")]
│   └── range
│
├── Binários
│   ├── bytes
│   ├── bytearray
│   └── memoryview
│
├── Conjuntos e Mapeamentos
│   ├── set[T]
│   ├── frozenset[T]
│   └── dict[K, V]
│
├── Tipos especiais (typing)
│   ├── Union[T1, T2]
│   ├── Optional[T]
│   ├── Literal[...]
│   ├── TypedDict
│   ├── Protocol
│   ├── NewType
│   └── Any
```

## Explicação

- **Tipos amplos**: `int`, `str`, `list`, `dict`, `bool`, `NoneType`.  
- **Subtipos**: `Literal` é sempre um **valor específico** dentro de um tipo amplo.  
  - `Literal[3]` ⊂ `int`  
  - `Literal["ok"]` ⊂ `str`  
  - `Literal[True]` ⊂ `bool`  
- **Tipos compostos**: `Union`, `Optional`, `TypedDict`, `Protocol` permitem criar estruturas mais complexas.  
- **Any**: o tipo mais genérico, aceita qualquer coisa.

----

## Dúvidas

### Pergunta

Por que no Python eu consigo fazer isso:

```tupla_varios_valores: tuple[str, ...] = ("Valor", "...")```

Mas não consigo fazer isso?

```tupla_varios_valores: tuple[str, int, float, ...] = ("Valor", 234, 3.14, "...")```

### Resposta

A anotação ```tuple[T, ...]``` significa: "uma tupla contendo zero ou mais elementos do tipo ```T```".

O ```...``` aqui não é o mesmo ```Ellipsis``` literal do Python, mas uma sintaxe especial usada apenas em type hints para indicar repetição indefinida de um único tipo.

Exemplo válido:

  ```python
  tupla_strings: tuple[str, ...] = ("a", "b", "c")
  ```

----

## O que é o ```Union``` e o ```Sequence``` e qual a diferença entre eles?

Ambos são **construtos de tipagem** usados em _type hints_ para descrever como os dados podem ser organizados ou quais tipos eles podem assumir.

- ```Union:``` Um _tipo composto_ que indica que um valor pode ser de **um tipo ou outro**.

- ```Sequence:``` Uma _interface de tipo abstrato_ que representa qualquer sequência ordenada (```list```, ```tuple```, ```range```, ```str```, etc.).

> **Nota:** Percebi que preciso estudar mais a fundo a documentação do Python sobre _type hints_. Segue _url_ para futuras buscas: [Documentação Python Type Hints](https://docs.python.org/3/library/typing.html "Acessa a documentação do módulo typing").
