from flask import Flask, render_template, request, redirect, session
import sys
sys.path.append("..")

from app import session

def login_required(f):
    def wrapper_login():
        # If not connected
        if 'compte' not in session: #NOT LOGGED IN
            return redirect("/signin")
        return f()
    return wrapper_login