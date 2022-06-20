## Dependencies

    UA VPN configured

    OpenVPN configured

## Deploy application

    bash app-deploy.sh

## Methods

    GET / -> for test purposes, return all accounts in database

    GET /signup -> redirect to signup page
        input: string redirectUrl - json
    
    POST /signup -> INTERNAL USE - create account and redirect to redirectUrl given on GET /signup
        output: string token, string username - headers

    GET /login -> redirect to login page
        input: string redirectUrl - json
    
    POST /login -> INTERNAL USE - login and redirect to redirectUrl given on GET /login
        output: string token, string username - headers

    POST /logout -> logout account
        input: string username, string website - json

    GET /status -> get account status 
        input: string token - json
        output: string token - json
            '' if not logged in
            token if logged in
    
    GET /update -> redirect to account page
        input: string redirectUrl, string token - json
    
    POST /update -> INTERNAL USE - update account and redirect to redirectUrl given on GET /update

    DELETE /delete -> delete an account
        input: string username, string website - json
                   

## Notes

When logging in, the application will redirect to the given link and the token will be returned in the header.

When redirected, it is needed to clik the link. For some reason it doesn't redirect automatically.

When testing service alone:
    put variable TEST to True in beggining of file auth.py
    put a valid token in variable TOKEN_TEST in beggining of file auth.py