# Escolha a imagem base
FROM continuumio/miniconda3

# Defina o diretório de trabalho
WORKDIR /Dasa

# Copie o environment.yml para o contêiner
COPY environment.yml .

# Instale as dependências
RUN conda env create -f environment.yml && conda list -n snake


# Ative o ambiente e adicione ao PATH
ENV PATH=/opt/conda/envs/snake/bin:$PATH

# Copie o restante dos arquivos do seu aplicativo
COPY . .



# Use o comando para ativar o ambiente e rodar seu aplicativo
CMD ["bash", "-c", "source activate snake && snakemake --snakefile Snakefile --cores 4 && exec python run.py"]
