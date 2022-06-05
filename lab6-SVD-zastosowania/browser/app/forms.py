from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ArticleSearcherForm(FlaskForm):
    input = StringField('Input', validators=[DataRequired()], default='Default text to be search')
    num_of_articles = IntegerField('Articles number to show', validators=[DataRequired()], default=5)
    submit = SubmitField('Search articles')
