from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

class FileForm(FlaskForm):
    code = FileField('Code', validators=[FileRequired(), FileAllowed(['cpp', 'c', 'py'])])
    language = SelectField('Language', choices=[('c', 'C'), ('c++', 'C++'), ('python', 'Python')])
    submit = SubmitField('Submit')

class AddProblemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    statement = TextAreaField('Statement', validators=[DataRequired()])
    input_format = TextAreaField('Input Format', validators=[DataRequired()])
    output_format = TextAreaField('Output Format', validators=[DataRequired()])
    constraints = TextAreaField('Constraints', validators=[DataRequired()])
    # time_limit = IntegerField('Time Limit', validators=[DataRequired()])
    # memory_limit = IntegerField('Memory Limit', validators=[DataRequired()])
    submit = SubmitField('Add Problem')

class AddTestCasesForm(FlaskForm):
    # prob_id = IntegerField('Problem ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    input = TextAreaField('Input', validators=[DataRequired()])
    output = TextAreaField('Output', validators=[DataRequired()])
    submit = SubmitField('Add Test Cases')