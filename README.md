# VTM

### Копирую

```bash
scp ./plates.json abk:/opt/vtm/
scp abk:/opt/vtm/plates.json .
```

# Управление

```bash
gunicorn -w 1 -b 127.0.0.1:8080 app:app

sudo systemctl daemon-reload
sudo systemctl enable flask_app
sudo systemctl start flask_app
sudo systemctl status flask_app
sudo systemctl restart flask_app
sudo systemctl stop flask_app
sudo systemctl disable flask_app
```

# Установка

```bash
pip install flask
pip install gunicorn
pip install requests
apt install certbot python3-certbot-nginx
```

# SECRET KEY

```bash
python3 -c "import secrets; print(secrets.token_hex())"

export SECRET_KEY=
```

# Сервис

```bash
sudo nano /etc/systemd/system/flask_app.service
```

```bash
[Unit]
Description=Flask App
After=network.target

[Service]
Environment=SECRET_KEY=
Type=simple
User=root
WorkingDirectory=/opt/vtm
ExecStart=/opt/vtm/venv/bin/gunicorn -w 1 -b 127.0.0.1:8080 app:app
Restart=always
RestartSec=90

[Install]
WantedBy=multi-user.target
```

# NGINX

### Управление сервисом nginx

```bash
sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
sudo systemctl restart nginx
sudo systemctl stop nginx
sudo systemctl disable nginx
```

```bash
sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default
```


```bash
sudo nano /etc/nginx/sites-available/app
```

```bash
server {
    server_name site.ru;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
certbot --nginx -d site.ru
```
