from flask import jsonify, request, render_template, send_file, redirect, url_for, render_template_string,session
import os
import pandas as pd
import io  # Importing io for handling I/O operations
import csv
from app import app


# Rota para a página inicial
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('filter_variants'))

# Rota para exibir o formulário e processar o filtro
@app.route('/filter_variants', methods=['GET', 'POST'])
def filter_variants():
    global filtered_data  # Use global variable
    global t 



    # Se os parâmetros de filtro não estiverem na URL, exibe o formulário
    if not request.args.get('frequency') or not request.args.get('depth'):
        return render_template('filter_form.html')

    # Obter os parâmetros de frequência e profundidade da requisição
    freq_threshold = float(request.args.get('frequency', 0.01))
    depth_threshold = int(request.args.get('depth', 10))
    



    # Caminho para o arquivo CSV anotado
    csv_path = os.path.join(os.getcwd(), "annotated_variants.hg19_multianno.csv")
    
    # Tentar ler o arquivo CSV e tratar erros
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return jsonify({"error": "Arquivo CSV não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Verificar se as colunas necessárias estão presentes
    required_columns = ['Otherinfo1']
    for col in required_columns:
        if col not in df.columns:
            return jsonify({"error": f"Coluna {col} não encontrada no DataFrame."}), 400
    
    # Remover colunas desnecessárias
    df = df.drop(columns=["Otherinfo2", "Otherinfo3"], errors='ignore')

    # Separar a coluna 'Otherinfo1' em colunas adicionais
    df[['GT', 'INFO', 'DP']] = df['Otherinfo1'].str.split('\t', expand=True)
    df = df.drop(columns=["Otherinfo1"], errors='ignore')

    # Certifique-se de que as colunas AF e DP sejam convertidas para tipos numéricos
    df['AF'] = pd.to_numeric(df['AF'], errors='coerce')
    df['DP'] = pd.to_numeric(df['DP'], errors='coerce')

    # Filtrar variantes por frequência (AF) e profundidade (DP)
    filtered_df = df[(df['AF'] <= freq_threshold) & (df['DP'] >= depth_threshold)]

    # Retornar os resultados filtrados em formato JSON ou mensagem de "Sem Conteúdo"
    if filtered_df.empty:
        return jsonify([]), 204  # No Content
    
    # Criando um dicionário com os dados
    data = {
    'freq':freq_threshold,  # Substitua 0.5 pelo seu valor real
    'dp': depth_threshold     # Substitua 0.1 pelo seu valor real
    }
    df = pd.DataFrame(data, index=[0]) 

# Criando um DataFrame a partir do dicionário
    #df = pd.DataFrame(data)

# Convertendo o DataFrame para um dicionário com orient='records'
    t = df.to_dict(orient='records')
    
    # Armazenar os resultados filtrados na variável global
    filtered_data = filtered_df.to_dict(orient='records')


    # Redirecionar para a rota de download
    return redirect(url_for('show_csv_download_page'))
    
    
    #result = filtered_df.to_dict(orient='records')
    

    #return jsonify(result)


# Rota para exibir a página com o botão de download
@app.route('/show_csv_download_page', methods=['GET'])
def show_csv_download_page():
    global filtered_data
    global t 
    t = pd.DataFrame(t)
    freq=t.iloc[0,0]
    dp=t.iloc[0,1]



    

    # Se não houver dados filtrados, exibe uma mensagem de erro
    if not filtered_data:
        return jsonify({"message": "Nenhum dado filtrado disponível."}), 204  # No Content

    # Aqui você deve usar pd.DataFrame ao invés de pd.read_json
    df = pd.DataFrame(filtered_data)  # Converte a lista de dicionários para um DataFrame

    # Criar as colunas necessárias
    df['nonsynonymous'] = df['ExonicFunc.refGene'].apply(lambda x: 1 if isinstance(x, str) and x.startswith('nonsynonymous') else 0)
    df['synonymous'] = df['ExonicFunc.refGene'].apply(lambda x: 1 if isinstance(x, str) and x.startswith('synonymous') else 0)
    df['splicing'] = df['Func.refGene'].apply(lambda x: 1 if 'splicing' in x else 0)
    df['intergenic'] = df['Func.refGene'].apply(lambda x: 1 if 'intergenic' in x else 0)
    df['exonic'] = df['Func.refGene'].apply(lambda x: 1 if 'exonic' in x else 0)
    df["check"] = df['Gene.refGene'].apply(lambda x: 1 if 'NONE' in x else 0)

    # Filtrar DataFrame
    df_filtered = df[df['check'] == 0]

    # Contar valores únicos na coluna 'Gene.refGene'
    num_unicos_filtered = df_filtered['Gene.refGene'].nunique()
    num_unicos_filtered = int(num_unicos_filtered)

    # Contar ocorrências
    count_nonsyn = int((df['nonsynonymous'] == 1).sum())
    count_syn = int((df['synonymous'] == 1).sum())
    count_spli = int((df['splicing'] == 1).sum())
    count_exo = int((df['exonic'] == 1).sum())
    count_int = int((df['intergenic'] == 1).sum())

    # Contar o número total de linhas no conjunto de dados filtrados
    num_rows = len(filtered_data)

    # Exibir a página HTML com os números contados e o botão de download
    html = f'''
    <html>
        <body>
            <h2>Arquivo VCF anotado em formato csv filtrado por AF (gnomAD) menores que {freq} e DP maiores que {dp} </h2>
            <p>Número total de variantes: {num_rows}</p>
            <p>Número de variantes sinônimas: {count_syn}</p>
            <p>Número de variantes não sinônimas: {count_nonsyn}</p>
            <p>Número de variantes em sítios de Splicing: {count_spli}</p>
            <p>Número de variantes em regiões exônicas: {count_exo}</p>
            <p>Número de variantes em regiões intergênicas: {count_int}</p>
            <p>Número de genes: {num_unicos_filtered}</p>
            <form action="/download_csv_file" method="GET">
                <button type="submit">Baixar CSV</button>
            </form>
        </body>
    </html>
    '''
    return render_template_string(html)


# Rota para baixar o arquivo CSV
@app.route('/download_csv_file', methods=['GET'])
def download_csv_file():
    global filtered_data
    global t 

    # Se não houver dados filtrados, exibe uma mensagem de erro
    if not filtered_data:
        return jsonify({"error": "Nenhum dado filtrado disponível para download."}), 400

    # Gerar o CSV a partir dos dados filtrados
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=filtered_data[0].keys())
    writer.writeheader()
    writer.writerows(filtered_data)
    output.seek(0)

    # Enviar o arquivo CSV para download
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='filtered_variants.csv')  # Use download_name em vez de attachment_filename


if __name__ == '__main__':
    app.run(debug=True)
