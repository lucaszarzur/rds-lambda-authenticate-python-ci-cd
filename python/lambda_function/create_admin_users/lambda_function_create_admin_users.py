import boto3
import os
import requests
import sys
from io import StringIO

# Inicialize o cliente Cognito
cognito_client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    # Criação de um "buffer" para capturar os prints
    log_capture_string = StringIO()
    sys.stdout = log_capture_string  # Redireciona os prints para o log_capture_string

    # User pool ID do Cognito
    user_pool_id = os.environ['USER_POOL_ID']
    second_api_url = os.environ['SECOND_API_GATEWAY_URL']

    # Defina as informações dos 5 usuários
    users = [
        {"username": "user1", "email": "user1@example.com"},
        {"username": "user2", "email": "user2@example.com"},
        {"username": "user3", "email": "user3@example.com"},
        {"username": "user4", "email": "user4@example.com"},
        {"username": "user5", "email": "user5@example.com"}
    ]

    # Defina uma senha temporária para todos os usuários
    password = "TempPassword123!"  # Exemplo de senha temporária

    # Loop para criar usuários no Cognito User Pool
    for user in users:
        try:
            # Criar o usuário no Cognito
            print(f"Attempting to create user {user['username']}...")
            response = cognito_client.admin_create_user(
                UserPoolId=user_pool_id,
                Username=user["username"],
                TemporaryPassword=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': user["email"]
                    },
                    {
                        'Name': 'email_verified',
                        'Value': 'true'
                    }
                ],
                MessageAction='SUPPRESS'  # Suprimir o envio de email de boas-vindas
            )

            print(f"User {user['username']} created successfully")

            # Ativar o usuário no Cognito com senha permanente
            print(f"Starting to activate user {user['username']}...")
            try:
                response = cognito_client.admin_set_user_password(
                    UserPoolId=user_pool_id,
                    Username=user["username"],
                    Password=password,
                    Permanent=True
                )
                print(f"User {user['username']} activated successfully")
            except Exception as e:
                print(f"Error activating user {user['username']}: {str(e)}")

        except Exception as e:
            print(f"Error creating user {user['username']}: {str(e)}")

    # ------------------ SEGUNDA API GATEWAY - START ------------------
    try:
        print("Making POST request to second API...")
        api_response = requests.get(second_api_url)

        # Se a resposta não for JSON, trata a resposta como texto simples
        try:
            api_response_data = api_response.json()  # Tentativa de interpretar a resposta como JSON
            print(f"Second API response (JSON): {api_response_data}")
        except ValueError:
            api_response_data = api_response.text  # Caso não seja JSON, retorna como texto simples
            print(f"Second API response (Text): {api_response_data}")

    except Exception as e:
        print(f"Error calling second API: {str(e)}")

    # Captura do log gerado
    log_contents = log_capture_string.getvalue()

    # Retorna o log completo junto com a resposta final
    return {
        'statusCode': 200,
        'body': f"Users created successfully and second API called\n\nLogs:\n{log_contents}"
    }
    # ------------------ SEGUNDA API GATEWAY - END ------------------
