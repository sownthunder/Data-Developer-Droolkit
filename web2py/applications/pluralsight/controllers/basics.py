# -*- coding: utf-8 -*-
# try something like
def helloworld():
    msg = "Hello from the controller!"
    return locals()

def index(): 
    return dict(message="hello from basics.py")
