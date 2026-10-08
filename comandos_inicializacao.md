Sempre que mudar algo rode os comando abaixo,
isso devido a API ficar rodando ao subir os
Dockers
```yaml 
docker compose up -d --build frontend - ele irá reconstrui o docker frontend
docker compose ps
docker compose logs --tail=100 frontend
```

URL
```yaml
Flet - http://localhost:8550/
API  - http://localhost:8000/
```

Comandos\
Compila os Dockers:
```yaml
docker compose up -d --build

ou para compilar um Docker especifico:

docker compose up -d --build api
```

Mostra o status do processamento do chat:
```yaml
docker stats datamind-ollama
```
Mostra o log da API:
```yaml
docker compose logs -f api
```
Mandando uma mensagem no prompt:
```yaml
docker exec -it datamind-api python -c "import requests,time; p={'message':'Crie uma função de soma de dois números em python.'}; t=time.time(); r=requests.post('http://localhost:8000/api/v1/chat',json=p,timeout=180); print('STATUS:',r.status_code); print('TEMPO:',round(time.time()-t,2),'segundos'); print(r.text)"
```
Em 'message' coloque a mensagem.