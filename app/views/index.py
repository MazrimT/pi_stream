from flask import Blueprint, render_template
from flask_login import current_user

index = Blueprint('index', __name__)


@index.route('/', methods=["POST", "GET"], endpoint='index')
def v_index():    
    
    
    return render_template(
        'index.html', 
        current_user=current_user
    )
    