## Dependencies

    sudo pip3 install flask, flask-cors, flask-restful

## Deploy application

    python3 auth.py

## Notes

To use application in test mode turn variable TEST=True in the beggining of the file auth.py. This will assume that the redirectUrl is empty ('').

When logging in, the application will redirect to the given link and the token will be returned in the header.

When redirected, it is needed to clik the link. For some reason it doesn't redirect automatically.

## Next tasks

Improve the method PUT /update.

Use MySQL DB instead of sqlite.

Make docker container for application and db.