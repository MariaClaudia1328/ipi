# Trabalho 1 de Introdução ao Processamento de Imagens

## Descrição

Este repositório contém os códigos e os resultados processados de acordo com as especificações dadas pelo professor da Disciplina que podem ser vistas neste [documento](https://github.com/MariaClaudia1328/ipi/blob/main/trabalho1/especificacoes.pdf).

O código foi feito em python 3.10.12, utilizando bibliotecas como opencv, numpy e matplotlib.

Todos os códigos se encontram na pasta `src`. Já os resultados, na pasta `assets`.

Dentro de `assets` temos as imagens utilizadas pra testar os códigos em `media_test` e os resultados de cada questão em sua respectiva pasta.

O relatório em [colocar link] desenvolve comentários sobre os resultados, assim como contextualiza os códigos desenvolvidos.

## Como executar

Cada código elaborado para capturar os resultados das questões estão nos respectivos arquivos python:

- Questão 1: `LER_YUV.py`
- Questão 2: `AGUCAMENTO.py`
- Questao 3: `FILTRO_REJEITA_NOTCH.py`

### Preparação do ambiente para executar

Para executar, recomenda-se criar um ambiente virtual utilizando venv, tal como se segue

```bash
sudo apt install python3.10-venv
python3 -m venv envIPI
source envIPI/bin/activate
```

Quando dentro do ambiente virtual, é necessário instalar as dependências do projeto por meio do comando

```bash
cd trabalho1
pip3 install -r requirements.txt
```

### Questão 1

Para executar o código da questão 1, basta digitar no terminal

```bash
python3 LER_YUV.py foreman.yuv 352 288 15
```

Sendo que `foreman.yuv` é o nome do arquivo ou o caminho para o arquivo binário de vídeo `.yuv` a ser processado. `325 288` são respectivamente a largura e altura da imagem do arquivo `.yuv` e pode ser alterado. `15` é o número do quadro contendo a imagem YUV a ser processada, também pode ser alterado.

Caso queira executar as imagens padrões do trabalho, basta trocar `foreman.py` por `../assets/media_test/foreman.py`.

### Questão 2

Para executar o código da questão 2, basta digitar no terminal

```bash
python3 AGUCAMENTO.py Image1.pgm -4
```

Sendo que `Image1.pgm` é o nome do arquivo ou o caminho para o arquivo de imagem `.pgm` a ser processado. O número que segue, `-4` diz respeito ao tipo de kernel do filtro de laplace a ser utilizado. Ele pode assumir somente valores iguais a `-4, 4, -8, 8`, caso contrário, o programa será terminado.

Caso queira executar as imagens padrões do trabalho, basta trocar `Image1.pgm` por `../assets/media_test/Image1.pgm`.

### Questão 3

Para executar o código da questão 3, basta digitar no terminal

```bash
python3 AGUCAMENTO.py moire.tif
```

Sendo que `moire.tif` é o nome do arquivo ou o caminho para o arquivo de imagem `.pgm` a ser processado.

Caso queira executar as imagens padrões do trabalho, basta trocar `moire.tif` por `../assets/media_test/moire.tif`.
