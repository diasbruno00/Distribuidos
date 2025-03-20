FROM python:3.7-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto
COPY . .

# Define a variável de ambiente para desativar o buffering
ENV PYTHONUNBUFFERED=1

# Define o comando padrão para o contêiner
CMD ["python", "server.py"]
