# Projeto de Programação SQLite 📊

## Home Broker + Crowler de Dados 🏦🔍

Este projeto, proposto pelo Professor Adilson no curso de programação da Fatec São Caetano do Sul, visa desenvolver um sistema de home broker completo, utilizando SQLite para armazenamento de dados e um crawler para coletar informações do mercado financeiro. O sistema permitirá aos usuários realizar diversas operações de compra e venda de ativos, além de acompanhar dados atualizados do mercado.

Algo que posso dizer que considero bem interessante aqui: segurança de entrada e saída de dados (fazendo a sanitização dos dados), também inseri funcionalidade de geração de logs no sistema, que armazenarão todas ações do usuário como logs para futuras auditorias do sistema.

### Algumas ações que este home broker pode fazer:

#### Instruções de Uso:

##### LINUX
1. Instale Python3 e pip, caso não tenha:
    ```bash
    sudo apt-get install python3 python3-pip
    ```

2. Navegue até a pasta raiz do repositório:
    ```bash
    cd caminho/para/o/repositório
    ```

3. Ative o ambiente virtual:
    ```bash
    source .venv/bin/activate
    ```

4. Instale as dependências listadas no arquivo requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

5. Execute o módulo principal:
    ```bash
    python main.py
    ```

6. Aguarde a solicitação (puxando todos os dados da bolsa).

7. Siga os passos solicitados na tela.

##### WINDOS
#### Instruções de Uso:

1. Clone o repositorio:
    ```bash
    git clone https://github.com/efraim-lima/secured-broker
    ```

2. Navegue até a pasta raiz do repositório:
    ```bash
    cd caminho/para/o/repositório
    ```

3. Ative o ambiente virtual:
    ```bash
    .venv\Scripts\activate
    ```

4. Instale as dependências listadas no arquivo requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

5. Execute o módulo principal:
    ```bash
    python main.py
    ```


#### `broker`

Apresenta dados atuais do mercado.

#### Lógica para Comprar:

- Faça um request pela API da bolsa.
- Salve como uma nova tabela no banco de dados.
- Verifique o saldo.

#### Lógica para Vender:

- Verifique se existe este ativo na bolsa (beta).
- Verifique se existe quantidade na carteira do cliente:
    - Se existir, venda (beta).
    - Se não existir, alerte que será feita uma venda à seco (perigosa) (beta).
- Verifique o saldo (beta).
- Compare com o preço do ativo (beta).
- Venda.
