import os

from flask import render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .. import app
from ..models import Product

from ..forms import UpdateProfileImageForm, AddProductForm
from .. import app, db


@app.route('/UserPage', methods=['GET', 'POST'])
@login_required
def userPage():
    form = UpdateProfileImageForm()

    if form.validate_on_submit():
        if form.profile_image.data:
            filename = secure_filename(form.profile_image.data.filename)
            file_path = os.path.join(app.root_path, 'static/profile_images', filename)
            form.profile_image.data.save(file_path)
            current_user.profile_image = filename
            db.session.commit()

    return render_template('userPage.html', current_user=current_user, form=form)


@app.route('/myitems', methods=['GET', 'POST'])
@login_required
def myitems():
    prod_form = AddProductForm()
    products = Product.query.filter_by(user_id=current_user.id).order_by(Product.id.desc()).all()

    return render_template('myitems.html', prod_form=prod_form, products=products)
