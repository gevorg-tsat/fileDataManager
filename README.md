# CSV File Manager

## Запуск
1. Установить docker
2. В терминале перейти в папку проекта
3. Изменить [config](config.py) под себя, если необходимо (если меняете порт, то также его следует сменить в [docker-compose.yaml](docker-compose.yaml)
4. Запустить проект через docker-compose
```bash
docker-compose up
```
5. Swagger-Документация находится на http://0.0.0.0:8081, если вы не меняли порт и хост.