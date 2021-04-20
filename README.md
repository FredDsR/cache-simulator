# cache-simulator
Projeto para automatizar a execução de diversas simulações de cache e comparação entre suas estatísticas.

## Instalação

### Pré-requisitos
Para instalar é necessário ter uma versão do *Python* instalada (sugiro utilizar [pyenv](https://github.com/pyenv/pyenv)), assim como a ferramenta [*pipenv*](https://pypi.org/project/pipenv/). Além disso, é necessário ter a versão 3.0 da ferramenta [*sim-cache*](http://www.simplescalar.com/) devidamente configurada na sua pasta $HOME assim como os benchmarks que irá utilizar.

### Comandos
Depois dos pré-requisitos devidamente instalados, é necessário clonar este projeto na sua máquina, que pode ser feito rodando o comando `git clone https://github.com/FredDsR/cache-simulator.git`.

Tendo o repositório clonado, basta rodar os comandos `pipenv install` e `pipenv run python simcache.py`

## Utilização
Para rodar basta adicionar a configuração desejada à pasta **experiments/** atravéz de um arquivo *.json* e executar o comando `python simcache.py`. Depois disso o script gerará os resultados na pasta **results/**.

## Configuração
O arquivo de configuração tem a seguinte estrutura:

```
[
    { # First simuation
        "il1": {
            "nsets": "64",
            "bsize": "64",
            "assoc": "1",
            "repl": "l"
        },
        "il2": null,
        "dl1": {
            "nsets": "64",
            "bsize": "64",
            "assoc": "1",
            "repl": "l"
        },
        "dl2": null,
        "benchmarks": [
            "Benchmarks/gcc/cc1.ss",
            "Benchmarks/gcc/gcc.i"
        ]
    },
    { # Second simulation
        "il1": {
            "nsets": "32",
            "bsize": "32",
            "assoc": "1",
            "repl": "l"
        },
        "il2": null,
        "dl1": {
            "nsets": "32",
            "bsize": "32",
            "assoc": "1",
            "repl": "l"
        },
        "dl2": null,
        "benchmarks": [
            "Benchmarks/gcc/cc1.ss",
            "Benchmarks/gcc/gcc.i"
        ]
    }
]
```

Onde cada dicionário dentro da lista é uma simulação diferente e cada chave corresponde à uma cache dentro do sistema a ser simulado.

Caso queira utilizar uma cache com algum nível unificado basta utilizar a seguinte configuração:

```
[
    { # First simulation
        "ul1": {
            "nsets": "128",
            "bsize": "64",
            "assoc": "1",
            "repl": "l"
        },
        "il2": null,
        "dl2": null,
        "benchmarks": [
            "Benchmarks/gcc/cc1.ss",
            "Benchmarks/gcc/gcc.i"
        ]
    },
    { # Second simulation
        "ul1": {
            "nsets": "64",
            "bsize": "32",
            "assoc": "1",
            "repl": "l"
        },
        "il2": null,
        "dl2": null,
        "benchmarks": [
            "Benchmarks/gcc/cc1.ss",
            "Benchmarks/gcc/gcc.i"
        ]
    }
]
```

**Importante: A lista benchmarks em cada simulação deve seguir a ordem que seria utilizada na execução do programa *sim-cache* na linha de comando**

## Saída experada

Para o primeiro exemplo de experimento, a saída esperada é um arquivo *.csv* que deve seguir este padrão:

```
type, nsets, bsize, assoc, repl, benchmark,    accesses, hits,     misses,  replacements, writebacks, invalidations, miss_rate, repl_rate, wb_rate, inv_rate, label
il1,  64,    64,    1,     l,    cc1.ss_gcc.i, 45397813, 41158668, 4239145, 4239081,      0,          0,             0.0934,    0.0934,    0.0000,  0.0000,   simulation_0
dl1,  64,    64,    1,     l,    cc1.ss_gcc.i, 16934051, 15625167, 1308884, 1308820,      463272,     0,             0.0773,    0.0773,    0.0274,  0.0000,   simulation_0
il1,  32,    32,    1,     l,    cc1.ss_gcc.i, 45397813, 36511502, 8886311, 8886279,      0,          0,             0.1957,    0.1957,    0.0000,  0.0000,   simulation_1
dl1,  32,    32,    1,     l,    cc1.ss_gcc.i, 16934051, 14005642, 2928409, 2928377,      1194355,    0,             0.1729,    0.1729,    0.0705,  0.0000,   simulation_1
```
