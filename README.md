# Computacao Distribuida 2016-1

Este e' um conjunto de exemplos para a disciplina de Computacao Distribuida da UFFS de 2016-1.
Os exemplos estao escritos usando python, o framework web bottle e o pacote requests.

## Rodando

Para rodar os exemplos e' necessario o python3, o pacote bottle, o pacote json e o pacote requests.
Todos os pacotes estao disponiveis atraves do pip.

```bash
# pip3 install bottle requests
```

Apos, basta entrar na pasta do exemplo e roda'-los:

```bash
$ cd t2
$ python3 dht.py
```

Para testar, pode ser usado o browser ou entao a ferramenta de linha de comando ***curl***

```bash
$ curl -X GET "http://localhost:8080/dht/abcd1234
$ curl -X PUT "http://localhost:8080/dht/abcd1234/1234
$ curl -X GET "http://localhost:8080/dht/abcd1234
```
