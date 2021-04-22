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

Um ponto importante a ser levado em consideração é a estrutura do arquivo *csv* de saída, para evitar dados sem centexto entre si, recomendo que seja utilizado somente um arquivo de configuração paraa cada experimento a ser avaliado, pois assim é garantido que todos os dados extraídos das simulações tenham o mesmo contexto. O arquivo de configuração tem a seguinte estrutura:

```
[
    { # First simulation
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
        "benchmark": "Benchmarks/gcc/cc1.ss Benchmarks/gcc/gcc.i"
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
        "benchmark": "Benchmarks/gcc/cc1.ss Benchmarks/gcc/gcc.i"
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
        "benchmark": "Benchmarks/go/go.ss 50 9 Benchmarks/go/2stone9.in"
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
        "benchmark": "Benchmarks/gcc/cc1.ss Benchmarks/gcc/gcc.i"
    }
]
```

**Importante: Perceba que no segundo exemplo de configuração são utilizados dois benchmarks diferentes, isso pode ser feito sem problemas pois será expecificado o benchmark utilizado em cada simulação. Porém, é importante os arquivos utilizados no benchmark estarem na pasta raiz do programa *sim-cache***

## Saída esperada

Para o primeiro exemplo de experimento, a saída esperada é um arquivo *.csv* que deve seguir este padrão:

```
cache ,nsets ,bsize ,assoc ,repl ,benchmark    ,accesses ,hits     ,misses  ,replacements ,writebacks ,invalidations ,miss_rate ,repl_rate ,wb_rate ,inv_rate ,sim_num_insn ,sim_num_refs ,sim_elapsed_time ,sim_inst_rate ,label
il1   ,64    ,64    ,1     ,l    ,cc1.ss_gcc.i ,45397813 ,41158668 ,4239145 ,4239081      ,0          ,0             ,0.0934    ,0.0934    ,0.0000  ,0.0000   ,45397813     ,16803484     ,2                ,22698906.5000 ,simulation_0
dl1   ,64    ,64    ,1     ,l    ,cc1.ss_gcc.i ,16934051 ,15624209 ,1309842 ,1309778      ,463333     ,0             ,0.0773    ,0.0773    ,0.0274  ,0.0000   ,45397813     ,16803484     ,2                ,22698906.5000 ,simulation_0
il1   ,32    ,32    ,1     ,l    ,cc1.ss_gcc.i ,45397813 ,36511502 ,8886311 ,8886279      ,0          ,0             ,0.1957    ,0.1957    ,0.0000  ,0.0000   ,45397813     ,16803484     ,2                ,22698906.5000 ,simulation_1
dl1   ,32    ,32    ,1     ,l    ,cc1.ss_gcc.i ,16934051 ,14004609 ,2929442 ,2929410      ,1194464    ,0             ,0.1730    ,0.1730    ,0.0705  ,0.0000   ,45397813     ,16803484     ,2                ,22698906.5000 ,simulation_1
```
Onde cada campo significa:

* **cache**: Identificador do tipo e nível da cache (Ex.: *il1*, *dl1*, etc...);

* **nsets**: Quantidade de conjuntos;

* **bsize**: Tamanho do bloco;

* **assoc**: Nível de associação;

* **repl**: Política de substituição

* **benchmark**: Identificador do benchmark utilizado (concatenação dos arquivos de benchmark);

* **accesses**: Número total de acessos;

* **hits**: Número total de hits;

* **misses**: Número total de misses;

* **replacements**: Número total de substituições;

* **writebacks**: Número total de writebacks;

* **invalidations**: Número total de invalidações;

* **miss_rate**: Taxa de perda;

* **repl_rate**: Taxa de substituições;

* **wb_rate**: Taxa de writebacks;

* **inv_rate**: Taxa de invalidações;

* **sim_num_insn**: Número total de instruções executadas;

* **sim_num_refs**: Número total de loads e stores;

* **sim_elapsed_time**: Tempo total da simulação em segundos;

* **sim_inst_rate**: Velocidade da simulação (intruções/seg);

* **label**: Identificador da simulação.
