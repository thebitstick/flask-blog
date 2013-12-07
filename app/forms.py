from flask.ext.login import current_user
from flask.ext.wtf import Form, TextField, TextAreaField, validators, \
    HiddenField, BooleanField, PasswordField, SubmitField

from app.helpers import is_name
from app.models import User


class LoginForm(Form):
    username = TextField('Username', [
        validators.Required(),
        validators.length(min=1, max=64)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.length(min=1, max=64)
    ])
    remember_me = BooleanField('Remember me', default=False)

    def validate(form):
        """Validate login credentials.

        The error messages has been purposely left out so an attacker gain no
        knowledge which field is wrong.

        """
        # Validate built in validators
        if not Form.validate(form):
            return False
        # Validate user credentials
        username = form.username.data
        password = form.password.data
        form.user = User.query.filter_by(name=username).first()
        if not form.user or not form.user.compare_password(password):
            return False
        # Successfully validated
        return True


class ChangePasswordForm(Form):
    password = PasswordField('Current Password', [
        validators.Required(),
        validators.length(min=1, max=64)
    ])
    new_password = PasswordField('New Password', [
        validators.Required(),
        validators.length(min=1, max=64),
        validators.EqualTo('confirm', message='Passwords must match.'),
    ])
    confirm = PasswordField('Confirm New Password', [
        validators.Required(),
        validators.length(min=1, max=64)
    ])
    submit = SubmitField('Change Password')

    def validate_password(form, field):
        password = field.data
        if not current_user.compare_password(password):
            raise validators.ValidationError('Current password is wrong.')


class ChangeUsernameForm(Form):
    username = TextField('New Username', [
        validators.Required(),
        validators.length(min=2, max=64),
        is_name
    ])
    submit = SubmitField('Change Username')

    def validate_username(form, field):
        username = field.data
        form.user = User.query.filter_by(name=username).first()
        if form.user:
            raise validators.ValidationError('Username already exists.')


class CommentForm(Form):
    name = TextField('Name', [
        validators.Required(),
        validators.Length(min=2, max=50),
        is_name,
    ])
    body = TextAreaField('Comment', [
        validators.Required(),
        validators.Length(min=2, max=510),
    ])
    user_id = HiddenField('user_id')
    reply_id = HiddenField('reply_id')
