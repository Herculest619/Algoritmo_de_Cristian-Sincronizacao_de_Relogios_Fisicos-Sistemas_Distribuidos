# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para o container
COPY . /app

# Instala as dependências (se houver)
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o servidor vai usar (ajuste conforme necessário)
EXPOSE 20000