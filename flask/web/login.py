from flask import flash, request, redirect, render_template, url_for
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user

from . import app
from .models import User

# begin user access management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # endpoint = request.form['sign-out-endpoint']
    logout_user()
    # flash('Logged out successfully.', 'success')
    return redirect('/')

# # next_is_valid should check if the user has valid
# # permission to access the `next` url
# def next_is_valid(n):
#     return current_user.is_authenticated

@app.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')  # THIS IS NEEDED ?

    if current_user is not None and current_user.is_authenticated:
        return redirect('/')

    elif request.method == 'POST':
        username = str(request.form['username']).strip()
        pwd = str(request.form['pwd'])

        if username=='admin' and pwd=='secret':
            user = User(username)
            login_user(user)
            # flash('Welcome!', 'success')
            return redirect(next or '/mines/')
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

