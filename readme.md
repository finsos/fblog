## Python轻量级个人博客项目

> 使用Django2编写，数据库选择sqlite

#### Notice
- 提交第一个版本，主要实现文章，评论相关功能

#### Dependence
- 依赖都放在requirements.txt中，使用命令`pip install -r requirements.txt`安装环境所需依赖包
- 开发采用virtualenv管理Python环境
- 采用Nginx做静态web服务、反向代理
- 采用uWSGI做服务网关

#### Deploy
- 初始化数据库
```
python manage.py makemigrations
python manage.py migrate
```

- 安装uWSGI
`pip install uwsgi`

- 启动uWSGI
`uwsgi --ini uwsgi.ini`

- 配置Nginx代理,直接贴server段配置
```
server {
    listen       80;
    server_name  blog.finsos.com;

    access_log /var/log/nginx/fblog.access.log main;
    error_log /var/log/nginx/fblog.error.log warn;

    location /static/ {
        alias /opt/fblog/collectstatic/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:9999;
    }
}
```

#### FQA
1. web目录下必须存在migrations这个包目录，不然无法初始化数据库，访问都会报500错误
2. uWSGI可以配置创建socket或者监听端口，socket采用unix://协议转发
