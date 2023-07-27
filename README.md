# EasySaaS

This project will be attempted to make a great starting point for your next big business as easy and efficient as possible.
This project will create an easy way to build a SaaS application using Flask、Dash and feffery-xxx-components, or using FastAPI.

### Run mysql And redis By Docker

```
curl -fsSL https://get.docker.com | bash -s docker
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD={password} -d mysql
docker run --name redis -p 6379:6379 -d redis --requirepass "{redis-password}"
docker inspect mysql/redis | grep IPAddress
```

### Update System Environs

```
# vim .bash_profile / .zshrc
export {ENV_PRE}_DEBUG=1

export {ENV_PRE}_APP_NAME=EasySaaS
export {ENV_PRE}_APP_VERSION=0.0.1-beta

export {ENV_PRE}_APP_DOMAIN=http://127.0.0.1:8000
export {ENV_PRE}_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxx

export {ENV_PRE}_MAIL_SERVER=smtp.exmail.xx.com
export {ENV_PRE}_MAIL_PORT=465
export {ENV_PRE}_MAIL_USERNAME=noreply@easysaas.com
export {ENV_PRE}_MAIL_PASSWORD=xxxxxxxxxxxxxxxxxxxxxx

export {ENV_PRE}_REDIS_URI=redis://:password@host:port
export {ENV_PRE}_DATABASE_URI=sqlite:///{DIR}/main.db
# mysql+pymysql://user:password@host:port/dbname
# source .bash_profile / .zshrc
```

### Install venv And requirements.txt

```
# Python3.10+ required
cd {DIR} && python3 -m venv .venv
source .venv/bin/activate / deactivate
pip3 install -r requirements.txt
```

### Run Application With uwsgi / gunicorn / uvicorn

```
.venv/bin/uwsgi --module index:server --http :8000 --virtualenv .venv 
                --pidfile index.pid --master --daemonize index.log
.venv/bin/uwsig --stop / --reload index.pid

.venv/bin/uvicorn main:app --port 8000 --reload  # for test
.venv/bin/gunicorn main:app --bind 127.0.0.1:8000 --workers 2 
                            --worker-class uvicorn.workers.UvicornWorker
```

### Run Nginx With Config

```
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 80;
    listen [::]:80;
    server_name example.com;

    root        /data/www/example;
    index       index.html;
    
    access_log /data/log/nginx/example.access.log udcombined;
    error_log  /data/log/nginx/example.error.log error;

    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    ssl_certificate cert/example.com.pem;
    ssl_certificate_key cert/example.com.key;

    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout 5m;

    # ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://localhost:8000/;
    }
}
```