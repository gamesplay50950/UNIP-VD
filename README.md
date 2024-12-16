# UNIP-VD
Um script feito em python para baixar video-aulas do AVA da Unip.

# Finalidade
  O **UNIP-VD** foi desenvolvido para baixar vídeo-aulas do AVA da UNIP e salvá-los localmente. O intuito do programa é fazer uma cópia 
legítima e offline para consultas ou backup. Caso queira acessar as vídeo-aulas de forma online sem interesse em fazer o Download dos 
arquivos, recomendo usar o player de vídeo VLC da VideoLan, disponível em https://github.com/videolan/vlc, onde ao abrir a opção "mídia"
e ir em "Abrir transmissão de rede" é possível colocar o link da transmissão contendo o mesmo formato de url citado abaixo porém com a 
extensão **.m3u8** no final da URL, o vídeo será reproduzido normalmente sem a necessidade de baixá-lo em seu dispositivo.

# Como funciona?
  O **UNIP-VD** é um script python que calcula com base na duração da vídeo-aula do AVA da UNIP quantos "pedaços" tem o arquivo completo,  
baixando cada um deles individualmente e transformando em um arquivo de extensão **.mp4**. Ao acessar a aba de rede na função de inspecionar 
presente nos navegadores é possível encontrar o local onde os "pedaços" do vídeo estão armazenados, o nome listado geralmente é index_4_1.ts, 
index_3_1.ts, index_2_1.ts e index_1_1.ts, ao localizar o link a informação em "URL da Solicitação" mostra o local onde está armazenado 
os pedaçosdo vídeo, o final da url deve conter algo como "_.../index_x_y.ts_" onde "x" e "y" são números inteiros, onde x é a qualidade 
do vídeo e y os "pedaços" do arquivo.
  Os arquivos são divididos em "pedaços" de 6 segundos, variando de acordo com o tamanho do vídeo. Na url dos vídeos é possível determinar a 
qualidade dos vídeos, por exemplo "_.../index_1_0.ts_" indica que o vídeo tem qualidade de 1080p no primeiro "pedaço" de 6 segundos, 
"_.../index_2_0.ts_" tem qualidade de 720p, "_.../index_3_0.ts_" tem qualidade de 480p e "_.../index_4_0.ts_" tem qualidade 360p. Com base 
nessa informação o scipt calcula de acordo com o tempo do vídeo quantos "pedaços" o vídeo possui no total e os baixa sequencialmente, após 
baixado ele converte em formato **.mp4**, salvando no diretório especifícado.

# Requisitos
  O script necessita do ffmpeg instalado e configurado no dispositivo (disponível em https://ffmpeg.org/download.html), caso não tenha o 
Python instalado no dispositivo Windows, baixe o script disponível nas builds deste repositório. Caso opte por rodar o script python será 
necessário instalar algumas bibliotecas como:

  - Os
  - Requests
  - Pathlib
  - Subprocess
  - Ffmpeg

_Obs.:_ Caso não saiba adicionar o ffmpeg ao Path do windows, use a build com o ffmpeg já baixado para Windows junto do arquivo **.bat**, 
ele adicionará o ffmpeg ao Path do Windows.

