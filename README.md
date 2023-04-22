# Lordaeron chat
This is example of work:  
https://github.com/Sobolev5/channel-box  
https://github.com/Sobolev5/carrot-rpc  

See live here:
http://89.108.77.63:1025


# Scheme
Microservice `interface` render chat interface 
and open websocket channel for new chat messages.  

Microservice `bot` await messages from `interface`
and ask to `interface` via next chain:
`rabbitmq -> proxy function on *interface* -> websocket`  


## Install
To install run:
```no-highlight
git clone https://github.com/Sobolev5/LordaeronChat
cd LordaeronChat
mv .env.example .env
```

# Production mode
Start with:
```no-highlight
docker compose -f docker-compose.yml up --build -d # start
docker exec -i chat-interface python run src.database "db_init" # init db 
```

# Dev mode
Start with:
```
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d # start
docker exec -i chat-interface python run src.database "db_init" # init db  
docker compose logs -f chat-interface -f chat-bot # console
docker exec -it chat-interface bash # go inside 
docker exec -it chat-bot bash # go inside 
```

#### Chat interface
http://127.0.0.1:1025

#### RabbitMQ 
```
http://127.0.0.1:15762
user: admin
password: admin
```

#### Postgres 
```
http://127.0.0.1:5433
user: admin
password: admin
db: chat-db
```

