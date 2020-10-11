from flask import url_for, current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_reset_email(user):
    token = user.get_user_token()
    msg = Message('Password Reset Request',
                  sender='pistaftab@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('user.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.'''
    html_body = render_template('email/reset.html', user=user, token=token)
    msg.html = html_body
    Thread(target=send_async_email,
            args=(current_app._get_current_object(), msg)).start()

