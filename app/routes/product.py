import os

from flask import flash, redirect, url_for, render_template, request, session
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
            image_path = os.path.join(app.root_path, 'static/product_images', filename)
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
    danger_message = session.pop('login_success', None)
    if request.method == 'POST':
        if not current_user.is_anonymous and current_user.id != product.user_id and current_user.is_authenticated:
            rating = int(request.form.get('rating', 0))
            if 1 <= rating <= 5:
                product.rating = (product.rating + rating)
                product.final_rating = round(product.rating / (product.rating_count + 1), 1)
                product.rating_count += 1
                db.session.commit()
        else:
            flash('You cannot rate your own product.', 'danger')
            return redirect(url_for('login'))

    return render_template('productPage.html', products=[product], final_rating=product.final_rating)


@app.route('/pop_item', methods=['GET', 'POST'])
def pop_item():
    products = Product.query.filter(Product.final_rating >= 4).all()

    return render_template('popular_items.html', products=products)


@app.route('/all_items', methods=['GET', 'POST'])
def all_items():
    products = Product.query.all()

    return render_template('all_items.html', products=products)


@app.route('/new_arrivals')
def new_arrivals():
    from datetime import datetime, timedelta
    last_week = datetime.now() - timedelta(days=3)
    products = Product.query.filter(Product.expire_date >= last_week).all()

    return render_template('new_arrivals.html', products=products)
