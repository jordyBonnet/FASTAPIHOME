# FASTAPIHOME
Home server done with FAST API to be installed on a raspberry py

run server: uvicorn main:app --reload

## Functions:
Send notifications to smartphones with pushbullet

## installation:
1. pip install fastapi
2. pip install "uvicorn[standard]"<br>
see: https://fastapi.tiangolo.com/
3. pip install fastapi-utils<br>
see: https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/<br>
for task/function scheduling

## Ideas:
- https://nickgeorge.net/pydantic-sqlite3/<br>
making SQLite3 and pydantic working together

## Todo:
- [ ] send messages with telegram API
- [ ] create a sheduled function to send these messages
- [ ] create a database to store glass trash days
- [ ] create a small UI accessible from local wifi to populate the dates
