import requests
import json
import os

def lambda_handler(event, context):
    # Acessando o corpo da requisição (que está em formato de string)
    body = event.get('body')

    if body:
        # Convertendo o corpo (string JSON) para um dicionário
        body_data = json.loads(body)
        
        # Acessando USERNAME e PASSWORD a partir do corpo da requisição
        username = body_data.get('USERNAME')
        password = body_data.get('PASSWORD')

        # Acessando a variável de ambiente
        client_id = os.getenv('CLIENT_ID', '4f19md0ce5hj13qdnciqh56oiv')  # '4f19md0ce5hj13qdnciqh56oiv' é o valor padrão caso a variável não exista
        
        # Verificando se USERNAME e PASSWORD estão presentes
        if not username or not password:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'USERNAME e PASSWORD must be filled.'})
            }

        # Definindo a URL e os headers para a requisição do Cognito
        url = 'https://cognito-idp.us-east-1.amazonaws.com/'
        headers = {
            'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth',
            'Content-Type': 'application/x-amz-json-1.1'
        }

        auth_parameters = {
            'USERNAME': username,
            'PASSWORD': password
        }

        data = {
            'AuthParameters': auth_parameters,
            'AuthFlow': 'USER_PASSWORD_AUTH',
            'ClientId': client_id
        }

        # Enviando a requisição POST para o Cognito
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Verificando a resposta
        if response.status_code == 200:
            response_data = response.json()
            
            # Extraindo o IdToken da resposta
            id_token = response_data.get('AuthenticationResult', {}).get('IdToken')
            
            if id_token:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'IdToken': id_token})
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'IdToken not found'})
                }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({'error': response.text})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body is empty.'})
        }
