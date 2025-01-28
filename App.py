from minio import Minio
from minio.error import S3Error
import os

# Configurações do cliente MinIO
def get_minio_client():
    return Minio(
        "localhost:9000",  
        access_key="minioadmin",  # Substituir pela sua chave de acesso
        secret_key="minioadmin",  # Substituir pela sua chave secreta
        secure=False  # Defina como True se estiver usando HTTPS
    )

# Função para criar o bucket, caso não exista
def create_bucket(minio_client, bucket_name):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso!")
        else:
            print(f"Bucket '{bucket_name}' já existe.")
    except S3Error as e:
        print(f"Erro ao criar o bucket '{bucket_name}': {e}")

# Função para realizar o upload de um arquivo
def upload_file(minio_client, bucket_name, file_path, file_name):
    if os.path.exists(file_path):
        try:
            minio_client.fput_object(bucket_name, file_name, file_path)
            print(f"Arquivo '{file_name}' carregado com sucesso!")
        except S3Error as e:
            print(f"Erro ao carregar o arquivo '{file_name}': {e}")
    else:
        print(f"O arquivo '{file_path}' não foi encontrado.")

# Função para realizar o download de um arquivo
def download_file(minio_client, bucket_name, file_name, download_path):
    try:
        minio_client.fget_object(bucket_name, file_name, download_path)
        print(f"Arquivo '{file_name}' baixado com sucesso para '{download_path}'!")
    except S3Error as e:
        print(f"Erro ao baixar o arquivo '{file_name}': {e}")

# Função principal para executar as operações
def main():
    # Defina o nome do bucket
    bucket_name = "meu-bucket"
    
    # Inicializa o cliente MinIO
    minio_client = get_minio_client()

    # Cria o bucket (caso não exista)
    create_bucket(minio_client, bucket_name)

    # Caminho do arquivo para upload (relativo ao diretório atual)
    file_path = "exemplo.txt"
    file_name = "exemplo.txt"
    
    # Realiza o upload do arquivo
    upload_file(minio_client, bucket_name, file_path, file_name)

    # Caminho do arquivo para download
    download_path = "baixado_exemplo.txt"
    
    # Realiza o download do arquivo
    download_file(minio_client, bucket_name, file_name, download_path)

if __name__ == "__main__":
    main()
