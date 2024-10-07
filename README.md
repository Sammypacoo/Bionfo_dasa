# Bioinformatics Project

Este projeto envolve a anotação de variantes genéticas a partir de arquivos VCF, utilizando ANNOVAR e um aplicativo em Flask para filtrar por frequencia e DP e baixar os resultados anotados. Abaixo estão as etapas seguidas para realizar o trabalho. 

## Etapas do Projeto

1. **Baixei o arquivo VCF**
   - Recebi o arquivo VCF por email para ser filtrado.

2. **Baixei o ANNOVAR**
   - Visitei a [página de download do ANNOVAR](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) para obter as instruções mais recentes.
   - A versão mais recente do ANNOVAR pode ser baixada [neste link](https://www.openbioinformatics.org/annovar/annovar_download_form.php) (registro necessário).
   - Após o registro, você receberá um e-mail com o link para instalar.

3. **Criei um ambiente Conda**
   - Utilizei o seguinte comando para criar um novo ambiente Conda onde você irá trabalhar:
     ```bash
     conda create -n meu_ambiente python=3.x
     ```
   - Ativei o ambiente criado:
     ```bash
     conda activate meu_ambiente
     ```

4. **Criei um Snakefile**
   - Um `Snakefile` foi criado para automatizar o processo de anotação, incluindo as seguintes etapas:
     4.1. **Baixar os datasets do ANNOVAR**
         - Baixei os datasets necessários para anotar informações sobre frequências populacionais e genes.
     4.2. **Preparar o arquivo VCF**
         - Formatei e prepare o arquivo VCF para a anotação.
     4.3. **Criar o arquivo anotado**
         - Utilizei ANNOVAR para gerar um arquivo anotado a partir do VCF.

5. **Criei uma API em Flask**
   - Desenvolvi uma API em Flask que permite filtrar o arquivo VCF anotado por frequências (`freq`) e profundidades de leitura (`dp`) específicas.
   - A API também permite baixar o arquivo filtrado em formato CSV.

6. **Criei um Dockerfile**
   - Um `Dockerfile` foi criado para empacotar a aplicação, permitindo que ela seja executada em um contêiner Docker
     
7. **Apaguei a pasta ANNOVAR**
   - 30G por isso eu deletei , seguir a etapa 2 para baixar o programa
     
8. **Adicionei ao GitHub**
   - Após finalizar o projeto, adicionei todos os arquivos ao repositório do GitHub usando os comandos:
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



OBS: Os arquivos output do annovar ja foram feitos caso você queria anotar outro arquivo vcf, vc deve:
1. Garantir que vc tenho pelo menos 50 Gigas de espaco
2. Clone o repositório:
   git clone <URL_do_seu_repositório>
   cd nome_do_repositorio
3. Substituir o arquivo presente na pasta vcf pelo novo arquivo vcf que vc quer anotar
4. Deletar os arquivos  annotated_variants.hg19_multianno.csv e variants.avinput
5. Baixar a pasta do annovar no mesmo diretorio (seguindo etapa 2)
6. Rodar o docker 

