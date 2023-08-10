import os

from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .. import app
from ..models import Product
from ..forms import AddProductForm
from .. import app, db


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()

    if form.validate_on_submit():
        name = form.ProductName.data
        description = form.Description.data
        category = form.category.data
        expire_date = form.expire_date.data
        price = form.price.data
        image = form.image.data
        new_product = Product(
            name=name,
            description=description,
            category=category,
            expire_date=expire_date,
            price=price,
            user=current_user
        )

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.root_path, 'app/static/product_images', filename)
            image.save(image_path)
            new_product.image = filename
            db.session.commit()

        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')

        return redirect(url_for('myitems'))

    return render_template('addProducts.html', form=form)


@app.route('/ProductPage/<int:id>', methods=['POST', 'GET'])
def ProductPage(id):
    product = Product.query.get_or_404(id)
    final_rating = 0
    if request.method == 'POST':
        if not current_user.is_anonymous and current_user.id != product.user_id and current_user.is_authenticated:
            rating = int(request.form.get('rating', 0))
            if 1 <= rating <= 5:
                product.rating = (product.rating + rating)
                final_rating = round(product.rating / (product.rating_count + 1), 1)
                product.rating_count += 1
                db.session.commit()
        else:
            flash('You cannot rate your own product.', 'danger')
            return redirect(url_for('login'))

    return render_template('productPage.html', products=[product], final_rating=final_rating)