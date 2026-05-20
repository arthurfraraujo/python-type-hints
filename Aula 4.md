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

* 
