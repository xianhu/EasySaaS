# EasySaaS

This project will be attempted to make a great starting point for your next big business as easy and efficent as possible. This project will create an easy way to build a SaaS
application using Python and Dash.

## Install For Development

### Run mysql And redis By Docker

```
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD={password} -d mysql:5.7
docker run --name redis -p 6379:6379 -d redis --requirepass "{redis-password}"
docker inspect mysql/redis | grep IPAddress
```

### Update System Environs

```
vim .bash_profile
# export ES_APP_DOMAIN=http://0.0.0.0:8088
# export ES_APP_SECRET_KEY=fejiadhjfehuhad
# export ES_MAIL_SERVER=smtp.feishu.cn
# export ES_MAIL_PORT=465
# export ES_MAIL_USERNAME=noreply@databai.com
# export ES_MAIL_PASSWORD=xxxxxxxxxxxxxxxxxxx
# export ES_REDIS_URI=redis://:password@host:port
# export ES_DATABASE_URI=sqlite:///{DIR}/main.db?charset=utf8
# mysql+pymysql://user:password@host:port/dbname?charset=utf8
source .bash_profile
```

### Install venv And requirements.txt

```
# Python3.8 required
cd {DIR} && python3.8 -m venv .venv
source .venv/bin/activate / deactivate
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Run uwsgi, Config File: aconfig/uwsgi.ini

```
.venv/bin/uwsgi --ini aconfig/uwsgi.ini
.venv/bin/uwsgi --reload index.pid
.venv/bin/uwsgi --stop index.pid
```

### Run nginx By Docker, Config File: aconfig/nginx.conf

```
docker run --name nginx -v {DIR}/aconfig/nginx.conf:/etc/nginx/nginx.conf:ro \ 
                        -v /tmp/:/tmp/ -p 8088:8088 -p 80:80 -p 443:443 -d nginx
```

## Others

### Frontend

- Css File: https://github.com/thomaspark/bootswatch
- Css File: https://github.com/tcbegley/dash-bootstrap-css
- Bootstrap: https://getbootstrap.com/docs/5.1/utilities/api/
- CheatSheet: https://dashcheatsheet.pythonanywhere.com/
- Front4.0: https://htmlstream.com/front-v4.0/index.html
