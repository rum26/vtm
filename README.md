# plates


```commandline
flask --app app run --debug --host=0.0.0.0 --port=5000
```

```commandline
gunicorn -w 1 -b 127.0.0.1:8080 bot:app
```