# Aula 1

## O que significa "_Type Hint_"?

No contexto geral, _Type Hint_ significa "fazer tipagem no código X", independente de como ela será feita.
Já em Python Moderno, chama-se _Type Annotations_, pois usa o sistema de _annotations_ do Python.

> Para possíveis dúvidas, verificar o [Glossário Relacionado](https://github.com/luizomf/typehints_python "Repositório de Type Hints do Otávio Miranda").

----

### Consideração importante

Acabei fazendo uma pequena confusão entre o _Ruff_ e o _Pyright_, assumindo que o ambos faziam a mesma coisa, mas não fazem. Abaixo detalho melhor a diferença dos dois.

- ***Ruff:*** _linter_ e _formatter_. Responsável por corrigir (ou padronizar) o estilo do código e detectar problemas comuns, como imports errados e variáveis não utilizadas.

- ***Pyright:*** _type checker_. Garante que as anotações de tipo sejam respeitadas e que valores errados não sejam aceitos (como em funções, por exemplo).

Dado o esclarecimento, podemos voltar ao fluxo normal da aula.

----

## Hierarquia dos tipos em Python

```
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

