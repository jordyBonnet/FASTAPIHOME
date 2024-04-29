# FASTAPIHOME
Home server done with FAST API<br>
http://127.0.0.1:8000/docs

Usefull home functions gathered into a local API.<br>

Scheduled functions are runned by schedul_trhead.py script.<br>
They call certain FAST API functions that uses [pushbullet](https://docs.pushbullet.com/#api-quick-start) to send notifications on your smartphone.<br>

To be installed on a raspberry py for example

- run API server on VScode terminal: 
```
source .venv/bin/activate
uvicorn main:app --reload
```
- run scheduler on a terminal:
```
python3.11 /home/pommi/FASTAPIHOME/schedul_thread.py
```

## Functions:
Send notifications to smartphones with pushbullet

## installation:
1. pip install fastapi
2. pip install "uvicorn[standard]"<br>
see: https://fastapi.tia[text](requirements.txt)ngolo.com/
3. pip install pushbullet.py 
4. [NOT USED] pip install fastapi-utils<br>
see: https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/<br>
for task/function scheduling

```pip install -r requirements.txt```<br>
```pip freeze > requirements.txt```<br>

## set git user & mail
```git config --global user.name jordy-Raspy```
```git config --global user.email jordy.bonnet@gmail.com```

## on raspberrypi OS:
virtual environment installation:<br>
```python3.11 -m venv .venv```
activate venv:<br>
```source .venv/bin/activate```


## Ideas:
- https://nickgeorge.net/pydantic-sqlite3/<br>
making SQLite3 and pydantic working together

## Todo:
- [x] send messages with telegram API
- [x] create a sheduled function to send these messages

