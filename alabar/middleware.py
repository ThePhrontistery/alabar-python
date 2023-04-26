from flask import request, redirect, url_for, session


def authenticate_handler(response):
    "Middleware to enforce redirect to login if not authenticated (not the 'static' route)"
    
    if not request.endpoint:
        return redirect(url_for('page_not_found'))
    
    if request.endpoint in 'static':
        return response
    
    if request.endpoint not in ('login', 'logout') and 'CURRENT_USER' not in session:
        return redirect(url_for('login', next=request.url))

    return response

