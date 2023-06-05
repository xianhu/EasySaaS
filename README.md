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
export {PRE}_DEBUG=1

export {PRE}_APP_NAME=EasySaaS
export {PRE}_APP_DOMAIN=http://127.0.0.1:8000
export {PRE}_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxx

export {PRE}_MAIL_SERVER=smtp.exmail.xx.com
export {PRE}_MAIL_PORT=465
export {PRE}_MAIL_USERNAME=noreply@easysaas.com
export {PRE}_MAIL_PASSWORD=xxxxxxxxxxxxxxxxxxxxxx

export {PRE}_REDIS_URI=redis://:password@host:port
export {PRE}_DATABASE_URI=sqlite:///{DIR}/main.db
# mysql+pymysql://user:password@host:port/dbname
# source .bash_profile / .zshrc
```

### Install venv And requirements.txt

```
# Python3.10+ required
cd {DIR} && python3.10 -m venv .venv
source .venv/bin/activate / deactivate
pip3.10 install -r requirements.txt
```

### Run Application With uwsgi / gunicorn / uvicorn

```
.venv/bin/uwsgi --module index:server --http :8000 --virtualenv .venv 
                --pidfile index.pid --master --daemonize index.log
.venv/bin/uwsig --stop / --reload index.pid

.vnev/bin/uvicorn main:app --port 8000 --reload  # for test
.venv/bin/gunicorn main:app --bind 127.0.0.1:8000 --workers 2 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend

- Bootstrap: https://getbootstrap.com/docs/5.1/utilities/api/
- CheatSheet: https://dashcheatsheet.pythonanywhere.com/
- Front4.0: https://htmlstream.com/front-v4.0/index.html
- Echarts: https://echarts.apache.org/examples/zh/index.html
- Antd: https://ant-design.gitee.io/index-cn
- Fac: https://fac.feffery.tech/what-is-fac
- Fuc: https://fuc.feffery.tech/what-is-fuc
- FastAPI: https://fastapi.tiangolo.com
- Pydantic: https://pydantic-docs.helpmanual.io
