# Aula 4

## Recursos de tipagem moderna que serão explorados

* dataclasses;
* classes abstratas (```ABC```);
* métodos abstratos;
* padrão de projeto _Singleton_ (com variação via cache);
* ```@override```, ```@final```, ```ClassVar```, ```Self```;
* ```TypeAlias``` moderno com ```type```.

## Etapas do código

* Criar a ```dataclass``` ```Person```;
* Criar a classe ```Address``` e compor com a classe ```Person```
* Em ```Person```, ```Address``` será um dict indexado, vamos usar ```TypeAlias``` com ```type```;
Criar um ```BaseAdress``` como ```ABC``` com pelo menos um ```@abstractmethod```;
* Crair ```Address``` que herda de ```BaseAddress``` e implementa o método abstrato;
Usar ```@override``` para garantir a assinatura correta;
* Criar ```CacheAdress``` com padrão ```Singleton``` por cache;
* Usar ```@final```, ```ClassVar``` e ```Self``` para tipagem correta.

> Antes de mais nada, vou buscar explorar o que é cada conceito exposto aqui pelo Otávio, entender melhor e depois aplicar no código.

### O que são ```dataclasses```?

* Recurso introduzido no Python 3.7 (através do módulo ```dataclasses```) que serve para automatizar a criação de classes cujo objetivo principal é **armazenar dados**.

### 1. O problema que ela resolve

Se fossemos criar uma classe para armazenar os dados de um arquivo PDF usando a estrutura tracional, o código seria assim:

```python
class PDFComum:
    def __init__(self, pdf_name: str, pdf_path: str):
        self.pdf_name: str = pdf_name
        self.pdf_path: str = pdf_path

    def __repr__(self):
        return f"PDFComum(pdf_name={self.pdf_name!r}, pdf_path={self.pdf_path!r})"

    def __eq__(self, other):
        if not isinstance(other, PDFComum):
            return NotImplemented
        return self.pdf_name == other.pdf_name and self.pdf_path == other.pdf_path
```

Note que é necessário escrever o ```__init__``` para receber os dados, o ```__repr__``` para o ```print(object)``` não mostrar um endereço de memória, e o ```__eq__``` para conseguir comparar se dois PDFs são iguais usando ```==```.

### 2. A Solução com Dataclass

Utilizando o decorador ```@dataclass```, você só precisa ddeclarar os atributos e seus respectivos tipos (_Type Hints_). O Python se encarrega do resto:

```python
from dataclasses import dataclass

@dataclass
class PDFDados:
    pdf_name: str
    pdf_path: str
```

Apenas com essas quatro linhas, o Python gera automaticamente:

* O método ```__init__``` adequado.
* Uma representação visual limpa via ```__repr__``` (ex: ```PDFDados(pdf_name='contrato.pdf', pdf_path='files/contrato.pdf')```).
* A lógica da comparação via ```__eq__``` baseada nos valores dos atributos.

### 3. Recursos Extrordinários das Dataclasses

Além de economizar linhas de código, as dataclasses trazem parâmetros poderosos no decorador para modificar o comportamento da classe:

* ```frozen=True``` **(Imutabilidade):** Se for definido ```@dataclass(frozen=True)```, os objetos se tornam "congelados". Ninguém pode alterar o valor de uma tributo após o objeto ser criado. Isso impede efeitos colaterais indesejados no sistema.

* ```order=True``` **(Ordenação):** Gera automaticamente os _dunder methods_ de comparação (```__lt__```, ```__gt__```, etc). Isso permite que você coloque seus objetos em uma lista e use o método ```lista.sort()``` para oderná-los automaticamente com base nos valores dos atributos.

### 4. A Integração com o ```__post_init__```

Como o ```__init__``` é gerado automaticamente pelo Python, você perde o lugar onde normalmente faria as validações dos dados recebidos. O ```__post_init__``` foi criado para resolver isso: o Python gera o ```__init__```, guarda os dados nos atributos e, **imediatamente depois**, chama o seu ```__post_init__``` para você rodar validações ou disparar exceções (como o ```FileNotFoundError```).

---

> Nota: Considerei importante me aprofundar um pouco mais no conceito de _dunder methods_ de comparação.

## _Dunder Methods_ de Comparação (ou _Rich Coimparison Methods_)

São as engrenagens que dão significado aos operadores lógicos estruturais do Python, como maior, menor ou igual.

Em linguagens como C, se você quer comparar duas ```structs```, você precisa criar uma função externa (como ```comparar_clientes(c1, c2)```). No Python, você ensina o próprio objeto a se comparar com outro usando esses métodos.

### 1. O Mapeamento dos Operadores

Cada operador lógico possui um par correspondente no modelo de dados do Python:

| Operador | Método Dunder | Significado |
| --- | --- | --- |
| `==` | `__eq__(self, other)` | _Equal_ (Igual a) |
| `!=` | `__ne__(self, other)` | _Not Equal_ (Diferente de) |
| `<` | `__lt__(self, other)` | _Less Than_ (Menor que) |
| `<=` | `__le__(self, other)` | _Less or Equal_ (Menor ou igual a) |
| `>` | `__gt__(self, other)` | _Greater Than_ (Maior que) |
| `>=` | `__ge__(self, other)` | _Greater or Equal_ (Maior ou igual a) |

### 2. Como a Lógica Funciona por Baixo dos Panos

Quando você escreve uma expressão como `objeto_a < objeto_b`, o interpretador do Python traduz essa linha silenciosamente para:

`objeto_a.__lt__(objeto_b)`

O método sempre recebe dois argumentos: `self` (o objeto da esquerda) e `other` (o objeto da direita). Ele deve analisar os critérios que você definir e retornar obrigatoriamente um valor booleano (`True` ou `False`).

### 3. A Mecânica de Inversão (Fallback)

O Python possui uma inteligência interna para evitar que o código quebre caso você implemente apenas "metade" dos operadores.

Se você tentar rodar `objeto_a > objeto_b` (que chama `__gt__`), mas a classe do `objeto_a` não tiver o método `__gt__` implementado, o Python não desiste imediatamente. Ele inverte a operação e tenta chamar o método espelho no segundo objeto:

`objeto_b.__lt__(objeto_a)` (Menor que)

Se nenhum dos dois objetos souber responder à pergunta, o Python lança um erro de tipo (`TypeError`).

### 4. O Retorno `NotImplemented`

Ao construir métodos de comparação manuais, é uma boa prática validar se o objeto que está vindo no argumento `other` é do mesmo tipo (ou de um tipo compatível).

Se alguém tentar comparar a sua classe de dados com uma string aleatória, por exemplo, o seu método deve retornar a constante nativa `NotImplemented`. Isso avisa ao interpretador do Python: _"Eu não sei comparar minha classe com esse tipo de dado, tente ver se o outro objeto sabe se comparar comigo"_.

### 5. O Atalho do `@total_ordering`

Escrever manualmente os seis métodos de comparação para cada classe é um trabalho repetitivo e propenso a erros. Para resolver isso, o Python oferece um decorador chamado `total_ordering` dentro do módulo `functools`.

Se você implementar apenas o `__eq__` (obrigatoriamente) e **qualquer um** dos outros cinco (como o `__lt__`), esse decorador preenche e constrói de forma matemática todos os quatro métodos restantes para você.

Isso garante que sua classe ganhe suporte completo a todas as operações relacionais do Python escrevendo apenas uma fração do código.

---

### Dúvidas

### 1. Usar `dataclasses` em qualquer classe para economizar código é má prática?

**Sim, é considerada uma má prática.** A tentação é grande porque ela elimina o `__init__`, mas o propósito de uma ferramenta importa mais do que a economia de linhas de linha de código.

As `dataclasses` foram desenhadas especificamente para o padrão de projeto chamado **Anêmico** ou **DTO (Data Transfer Object)**. Se você usa uma dataclass em uma classe que gerencia conexões de banco de dados, renderiza interfaces gráficas ou controla fluxos de rede, você está forçando o Python a gerar estruturas (como métodos de comparação e representação de strings focadas em atributos) que não fazem o menor sentido para aquele contexto.

---

### 2. O que significa uma classe "guardar dados" vs. "não guardar dados"?

Ter uma variável dentro da classe não a torna automaticamente uma classe de dados. A diferença crucial está no **propósito principal** da existência dela: **Estado vs. Comportamento**.

#### Classe que GUARDA dados (Foco no Estado)

Ela funciona como uma "sacola" estruturada. Ela serve apenas para transportar informações juntas pelo sistema. Quase não possui lógica de negócios complexa, apenas validações ou formatações simples dos próprios atributos.

* _Exemplo:_ Uma classe `Cliente` (guarda nome, email, telefone) ou uma classe `Pedido` (guarda ID, itens, valor total).

#### Classe que NÃO guarda dados (Foco no Comportamento)

O objetivo dela não é armazenar informações sobre uma entidade do mundo real, mas sim **executar ações, gerenciar recursos ou coordenar processos**. Elas até podem ter variáveis internas, mas essas variáveis geralmente guardam _configurações_ ou _conexões_, e não dados brutos de negócios.

* _Exemplo:_ Uma classe `EnviadorDeEmail`. Ela pode ter internamente uma variável com a conexão do servidor SMTP, mas o propósito dela é o método `.enviar(mensagem)`. Você não cria instâncias dela para salvar no banco de dados; você a usa como uma ferramenta de execução.

### 3. Qual a diferença entre `order=True` e `@total_ordering`?

Ambos servem para o mesmo objetivo final (permitir que seus objetos usem `<`, `>`, `<=`, `>=`), mas eles atuam em camadas diferentes do Python:

#### `order=True` (Exclusivo de Dataclasses)

É um parâmetro do próprio decorador `@dataclass`. Quando você ativa `@dataclass(order=True)`, o Python analisa automaticamente todos os campos que você declarou na dataclass e gera os métodos de comparação para você.

* **Critério automático:** Ele compara os atributos na ordem em que foram escritos. Se a classe tem `nome` e `idade`, ele vai comparar pelo `nome`. Se os nomes forem iguais, ele usa a `idade` como desempate. Você não precisa escrever nenhuma lógica.

#### `@total_ordering` (Para qualquer classe)

É um decorador geral do módulo `functools` usado em **classes comuns** (não dataclasses). Ele exige que você escreva manualmente o critério de igualdade (`__eq__`) e escolha **um** critério de magnitude (como o menor que, `__lt__`).

* **Critério manual:** Você escreve a regra exata no código do método escolhido. O `@total_ordering` então lê o seu método e deduz matematicamente como os outros quatro operadores devem se comportar.
