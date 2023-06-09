from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField, TextAreaField, validators, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
from core.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')

    def validate_email(self, email_to_check):
        email= User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email.')

    username = StringField(label='USERNAME', validators=[Length(min=3, max=30), Regexp(regex='\A[\w\-\.]{3,}\Z', message='Username must be 3 characters or more and contain only letters, numbers and underscores.'), DataRequired()])
    email = StringField(label='EMAIL', validators=[Email(), DataRequired()])
    password = PasswordField(label='PASSWORD', validators=[Length(min=6), Regexp(regex='\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message='Password must be 6 characters or more and contain at least one uppercase letter, one lowercase letter and one number.'), DataRequired()])
    confirm_password = PasswordField(label='CONFIRM PASSWORD', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='REGISTER')

class LoginForm(FlaskForm):
    username = StringField(label='USERNAME / EMAIL', validators=[DataRequired()])
    password = PasswordField(label='PASSWORD', validators=[DataRequired()])
    submit = SubmitField(label='SIGN IN')

class SearchForm(FlaskForm):
    search = StringField(label='Search', validators=[DataRequired()])
    submit = SubmitField(label='Search')

class GameForm(FlaskForm):
    def validate_white_elo(self, white_elo_to_check):
        if white_elo_to_check.data and white_elo_to_check.data <= 0:
            raise ValidationError('White Elo must be positive.')
    
    def validate_black_elo(self, black_elo_to_check):
        if black_elo_to_check.data and black_elo_to_check.data <= 0:
            raise ValidationError('Black Elo must be positive.')

    white = StringField(label='WHITE PLAYER*')
    black = StringField(label='BLACK PLAYER*')
    color = SelectField(label='YOUR COLOR*', choices=[(1, 'WHITE'), (-1, 'BLACK')])
    result = SelectField(label='RESULT*', choices=[(1, 'WHITE'), (0, 'DRAW'), (-1, 'BLACK')])
    moves = TextAreaField(label='MOVES*')
    date = DateField('DATE', [validators.optional()])
    white_elo = IntegerField(label='WHITE ELO', validators=[validators.optional()])
    black_elo = IntegerField(label='BLACK ELO', validators=[validators.optional()])
    file = FileField(label='', validators=[FileAllowed(['pgn'], 'Only PGN files are allowed.')])
    submit = SubmitField(label='IMPORT')

class EditorForm(FlaskForm):
    turn = SelectField(choices=[('w', 'White to play'), ('b', 'Black to play')])
    castling_w_k = BooleanField(label='O-O', default=True)
    castling_w_q = BooleanField(label='O-O-O', default=True)
    castling_b_k = BooleanField(label='O-O', default=True)
    castling_b_q = BooleanField(label='O-O-O', default=True)
    choices = [('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -', 'Set the board')]
    with open('core/static/games/openings.txt', 'r') as f:
        for line in f:
            choices.append((line.split(':')[1][:-1], line.split(':')[0]))
    position = SelectField(choices=choices)
    reset = SubmitField(label='Reset board')

class PreferenceForm(FlaskForm):
    about_me = TextAreaField(label='About me', validators=[Length(min=0, max=140)])
    piece_set = SelectField(label='Piece set', choices=[('alpha', 'Alpha'), ('anarcandy', 'Anarcandy'), ('california', 'California'), ('companion', 'Companion'), ('dubrovny', 'Dubrovny'), ('fantasy', 'Fantasy'), ('gioco', 'Gioco'), ('horsey', 'Horsey'), ('kosal', 'Kosal'), ('pixel', 'Pixel')])
    white_color = StringField('Light Color')
    black_color = StringField('Dark Color')
    submit = SubmitField(label='Save Changes')

class PuzzleForm(FlaskForm):
    result = IntegerField()
    submit = SubmitField("Next problem")