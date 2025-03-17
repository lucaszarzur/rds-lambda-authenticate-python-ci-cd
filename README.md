# Python AWS Lambda: Conjunto de lambdas Python para testar diversas funções na AWS, utilizando GitHub Actions como CI/CD

Este repositório tem como objetivo fornecer um conjunto de códigos em Python e pequenas instruções para auxiliar na criação de funções Lambda na Amazon AWS. Além dos lambdas este repositório cobre a criação de um AWS SAM template, que é útil para a [Infrastructure as code](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html).

Em uma função Lambda para o devido funcionamento do código (independente de qual a linguagem de programação escolhida) é necessário que o código suba juntamente as dependências (bibliotecas, etc.), seja diretamente na função Lambda ou através das Layers.

Os exemplos utilizarão a layer "arn:aws:lambda:us-east-2+1:336392948345:layer:AWSSDKPandas-Python313:1", que refere-se a uma Layer contendo o Python 3.13 (a versão dos códigos desse repositório) disponibilizada pela própria AWS.

Aqui fora utilizado o [AWS SAM](https://aws.amazon.com/pt/serverless/sam/) e melhorado a lógica de autenticação do usuário.

Resumo de tecnologias e funcionalidades neste repositório:

## 🛠 Tecnologias utilizadas
- AWS Lambda
- AWS SAM
- Códigos Lambda em Python
- Uso de varáveis de ambiente do AWS Lambda
- CI/CD GitHub Actions
- AWS Toolkit para IntelliJ


## 🖱️ Execute a aplicação

### Pré-requisitos
Antes de rodar o projeto, é necessário ter as seguintes ferramentas instaladas:
* AWS CLI;
* AWS SAM;

### Passo a passo
**OBS**: Para que o AWS SAM consiga realizar as ações na AWS é necessário que a configuração de credenciais do AWS CLI já estejam realizadas, pois é pego diretamente dele.

**1** - Faça o clone do projeto;

**2** - Compile o projeto (preparar o pacote da aplicação com suas dependencias e etc) no formato necessário para o AWS:
```
sam build --no-cached
```

**3** - Suba para a AWS:
```
sam deploy --guided
```

**4** - Confira as váriaveis de ambiente dentro do template.yaml ou diretamente nas funções Lambda;

**5** - Para que os usuários admin de testes sejam criados, confira o arquivo [instrucoes_adicionais.txt](resources/instrucoes_adicionais.txt). 

**6** - Limpeza de todos os recursos subidos pelo AWS SAM:
```
sam delete
```

Sim, apenas isso! :)
