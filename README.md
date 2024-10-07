# Bioinformatics Project

Este projeto envolve a anotação de variantes genéticas a partir de arquivos VCF, utilizando ANNOVAR e um aplicativo em Flask para filtrar por frequencia e DP e baixar os resultados anotados. Abaixo estão as etapas seguidas para realizar o trabalho. 

## Etapas do Projeto

1. **Baixar o arquivo VCF**
   - Receba o arquivo VCF que contém as variantes genéticas que você deseja analisar.

2. **Baixar o ANNOVAR**
   - Visite a [página de download do ANNOVAR](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) para obter as instruções mais recentes.
   - A versão mais recente do ANNOVAR pode ser baixada [neste link](https://www.openbioinformatics.org/annovar/annovar_download_form.php) (registro necessário).
   - Após o registro, você receberá um e-mail com o link para instalar.

3. **Criar um ambiente Conda**
   - Utilize o seguinte comando para criar um novo ambiente Conda onde você irá trabalhar:
     ```bash
     conda create -n meu_ambiente python=3.x
     ```
   - Ative o ambiente criado:
     ```bash
     conda activate meu_ambiente
     ```

4. **Criar um Snakefile**
   - Um `Snakefile` foi criado para automatizar o processo de anotação, incluindo as seguintes etapas:
     4.1. **Baixar os datasets do ANNOVAR**
         - Baixe os datasets necessários para anotar informações sobre frequências populacionais e genes.
     4.2. **Preparar o arquivo VCF**
         - Formate e prepare o arquivo VCF para a anotação.
     4.3. **Criar o arquivo anotado**
         - Utilize ANNOVAR para gerar um arquivo anotado a partir do VCF.

5. **Criar uma API em Flask**
   - Desenvolva uma API em Flask que permite filtrar o arquivo VCF anotado por frequências (`freq`) e profundidades de leitura (`dp`) específicas.
   - A API também permite baixar o arquivo filtrado em formato CSV.

6. **Criar um Dockerfile**
   - Um `Dockerfile` foi criado para empacotar a aplicação, permitindo que ela seja executada em um contêiner Docker:
     ```dockerfile
     # Exemplo de Dockerfile
     FROM continuumio/miniconda3

     # Defina o diretório de trabalho
     WORKDIR /app

     # Copie o environment.yml e instale as dependências
     COPY environment.yml .
     RUN conda env create -f environment.yml

     # Copie o restante dos arquivos do seu aplicativo
     COPY . .

     # Comando padrão para executar a aplicação
     CMD ["python", "app.py"]
     ```
7. **Apagar a pasta ANNOVAR**
   - 30G por isso eu apaguei mas ela pode ser encontrada em outro repositorio:

     ```
8. **Adicionar ao GitHub**
   - Após finalizar o projeto, você adicionou todos os arquivos ao repositório do GitHub usando os comandos:
     ```bash
     git init
     git add .
     git commit -m "Adicionando projeto de anotação de variantes"
     git remote add origin <URL_do_seu_repositório>
     git push -u origin master
     ```

## Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone <URL_do_seu_repositório>
   cd nome_do_repositorio

obs: Os arquivos output do annovar ja foram feitos caso vc queria anotar outro arquivo vcf, vc deve:
1. baixar esses arquivos
2. substituir o arquivo presente na pasta vcf pelo novo arquivo vcf que vc quer anotar
3. apagar os arquivos  annotated_variants.hg19_multianno.csv e variants.avinput
4. baixar a pasta do annovar no mesmo diretorio e ai sim vc pode rodar o docker 

