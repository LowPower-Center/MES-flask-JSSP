from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import Email, DataRequired



class CreateMaterialForm(FlaskForm):
    name = StringField('name',
                         id='name_create',
                         validators=[DataRequired()])
    number =IntegerField('number',
                      id='number_create',
                      validators=[DataRequired()])
    img = StringField('img',
                             id='img_create',
                             )