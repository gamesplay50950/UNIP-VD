import os
import requests
from pathlib import Path
import subprocess

outro = 'SIM'
while outro == 'SIM':
    # Informações do vídeo
    mint = int(input("Quantos minutos tem o vídeo? "))
    seg = int(input("Quantos segundos tem o vídeo? "))
    url = str(input("Digite a URL do vídeo blob: "))

    # Verificação de formato da URL
    if "index_" not in url or ".ts" not in url:
        print("A URL fornecida não contém o padrão esperado.")
        continue  # Reinicia o loop caso o formato seja inválido

    # Pergunta se o usuário quer criar uma nova pasta
    criar_pasta = input("Deseja criar uma nova pasta para o vídeo? (SIM/NAO): ").strip().upper()
    if criar_pasta == "SIM":
        pasta_nome = input("Digite o nome da nova pasta: ")
        downloads_path = Path.home() / "Downloads" / pasta_nome
        downloads_path.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir
        video_nome = pasta_nome  # Nome do arquivo final será igual ao da pasta
    else:
        pasta_nome = input("Digite o caminho da pasta existente onde o vídeo será salvo: ")
        downloads_path = Path(pasta_nome)
        if not downloads_path.exists():
            print("A pasta especificada não existe. Verifique o caminho.")
            continue
        video_nome = input("Digite o nome do arquivo final (sem extensão): ")

    # Converter os minutos em segundos e somar com os segundos finais do vídeo
    segundos = mint * 60 + seg
    segundos = int(segundos / 6) + 1  # Calcula o total de pedaços

    # Localizar o padrão base da URL
    base_url = url[:url.rfind("_") + 1]  # Parte até "index_"
    suffix = url[url.rfind("."):]       # Parte a partir de ".ts"

    # Baixar os pedaços
    print("Baixando arquivos...")  # Mensagem única
    arquivos = []  # Lista para armazenar os nomes dos arquivos baixados
    for c in range(0, segundos):  # De 0 até o número total de pedaços
        new_url = f"{base_url}{c}{suffix}"
        arquivo_nome = downloads_path / f"index_{c}.ts"
        arquivos.append(str(arquivo_nome))

        # Download do arquivo
        try:
            response = requests.get(new_url, stream=True)
            response.raise_for_status()
            with open(arquivo_nome, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {new_url}: {e}")
            continue

    # Criar o nome do vídeo final
    video_final = downloads_path / f"{video_nome}.mp4"
    lista_arquivos_txt = downloads_path / "lista.txt"

    # Criar lista de arquivos para ffmpeg
    with open(lista_arquivos_txt, "w") as f:
        for arquivo in arquivos:
            f.write(f"file '{arquivo}'\n")

    # Combinar os vídeos
    try:
        print("Criando o vídeo final...")
        subprocess.run(
            [
                r"C:\ffmpeg\bin\ffmpeg.exe",  # Substitua pelo caminho absoluto para o executável do FFmpeg
                "-f", "concat",
                "-safe", "0",
                "-i", str(lista_arquivos_txt),
                "-c", "copy",
                str(video_final)
            ],
            check=True
        )
        print(f"Vídeo final criado: {video_final}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar o vídeo final: {e}")

    # Criar o arquivo com a URL e o tempo do vídeo
    info_arquivo = downloads_path / f"{video_nome}_info.txt"
    with open(info_arquivo, "w") as f:
        f.write(f"URL do vídeo: {url}\n")
        f.write(f"Duração do vídeo: {mint} minutos e {seg} segundos ({mint * 60 + seg} segundos)\n")
    print(f"Informações do vídeo salvas em: {info_arquivo}")

    # Remover arquivos temporários
    for arquivo in arquivos:
        try:
            os.remove(arquivo)
        except OSError as e:
            print(f"Erro ao apagar {arquivo}: {e}")

    # Remover lista de arquivos temporários
    try:
        os.remove(lista_arquivos_txt)
    except OSError as e:
        print(f"Erro ao apagar {lista_arquivos_txt}: {e}")

    # Perguntar se o usuário deseja continuar
    outro = input("Deseja continuar? (Digite 'SIM' para repetir ou 'NAO' para encerrar): ").strip().upper()
