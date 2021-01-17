from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length

class AddPost(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired(),Length(min=5,max=128)])
    short_description = StringField(label='Short Description',
                                    validators=[DataRequired(),Length(min=5,max=250)])
    post = TextAreaField(label='Post Content',
                        validators=[Length(min=100, max=10000)],
                        render_kw={'rows':16})

    submit = SubmitField('Post')
class DeletePost(FlaskForm):
    submit = SubmitField('Delete Post')