import boto3
import os

# Initialize the API Gateway client
api_gateway_client = boto3.client('apigateway')

def lambda_handler(event, context):
    # ID da API e nome do stage (definido em variáveis de ambiente)
    rest_api_id = os.environ['API_GATEWAY_ID']
    stage_name = "prod"

    try:
        # Realizar o deploy do stage da API Gateway
        response = api_gateway_client.create_deployment(
            restApiId=rest_api_id,
            stageName=stage_name
        )

        # Retornar a resposta de sucesso
        return {
            'statusCode': 200,
            'body': f"Deploy do stage '{stage_name}' realizado com sucesso! Deployment ID: {response['id']}"
        }

    except Exception as e:
        # Retornar erro caso o deploy falhe
        return {
            'statusCode': 500,
            'body': f"Erro ao realizar o deploy do stage '{stage_name}': {str(e)}"
        }
