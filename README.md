### Local install

```bash
ngrok http 8080
cp .env.sample .env #and fill it (WH_HOST=xxxxx.ngrok.io)
```
###### With outside db
```bash
make i  # install deps with poetry
make migrate  # apply migrations
make run  # start bot
```
###### Within docker
```bash
docker-compose up -d --build
```

### Prod deployment
1. Fill in secret vars (BT, PT, WH_HOST, WH_PATH, PORT, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD) in [ci\cd variables](https://gitlab.com/mixartemev/aiogram-template/-/settings/ci_cd#js-cicd-variables-settings)
2. Set HOST, PORT, WH_PATH in variables section at .gitlab-ci.yml
3. Configure nginx config at server:
```
server {
    server_name {HOST};

    location = /{WH_PATH} {
    	proxy_pass http://0.0.0.0:{PORT};
    }
    ...
```
4. At server `mkdir /home/dev/project-name # (it is 'aiogram-template' in current case)` for copy deployment script in itself.


### Predefined operations
```bash
make migration msg='some label'  # make new migration
```
