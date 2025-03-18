# Sincronização de Relógios
Este projeto implementa um sistema de sincronização de relógios usando um servidor e múltiplos clientes.  
O servidor sincroniza o tempo com um servidor NTP e os clientes ajustam seus relógios com base no tempo recebido do servidor.


## Opção 1: Rodar Localmente
Instale as dependências:
```bash
pip install ntplib
```

Execute o servidor:

```bash
python Server.py
```
Execute os clientes:  
Abra terminais separados para cada cliente e execute:

```bash
python Cliente.py
```


## Opção 2: Rodar com Docker Compose
### Construa as imagens e inicie os containers:

```bash
docker-compose up --build
```
### Isso criará e iniciará os seguintes containers:

**server:** Servidor que sincroniza o tempo com um servidor NTP.

**client1, client2, client3, client4:** Clientes que se conectam ao servidor para sincronizar seus relógios.

### Verifique os logs dos containers:
Para visualizar os logs de cada container em tempo real, use os seguintes comandos:

#### Servidor:

```bash
docker-compose logs -f server
```
#### Clientes:

```bash
docker-compose logs -f client1
docker-compose logs -f client2
docker-compose logs -f client3
docker-compose logs -f client4
```

Isso exibirá as saídas de cada container em terminais separados, permitindo que você acompanhe o comportamento do servidor e dos clientes individualmente.

### Parar os containers:
Para parar e remover os containers, use:

```bash
docker-compose down
```