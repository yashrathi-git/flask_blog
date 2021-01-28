from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from blog.model import User, Post
from blog import db, app
from flask_login import login_required, current_user
from blog.profile.forms import UpdateForm, ChangePassword
import secrets
import os
from PIL import Image
from PIL import UnidentifiedImageError
from werkzeug.security import generate_password_hash
profile_blueprint = Blueprint('profile',
                              __name__,)


def save_image(profile_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(profile_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pic', picture_fn)
    # There is no point in storing really large images in file system
    # In the end they are going to be scaled down by css
    # Storing large images would cause the website to slow down as it have to download larger images

    output_size = (125, 125)
    try:
        i = Image.open(profile_pic)
    except UnidentifiedImageError:
        raise UnidentifiedImageError()
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def delete_bloat():
    if current_user.image_file == 'default.jpg':
        return
    picture_path = os.path.join(
        app.root_path, 'static/profile_pic', current_user.image_file)
    os.remove(picture_path)


@profile_blueprint.route('/account_info/', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            try:
                picture_file = save_image(form.profile_pic.data)
            except UnidentifiedImageError:
                flash('Invalid image file provided', 'danger')
                return redirect(url_for('profile.update_account'))
            delete_bloat()
            current_user.image_file = picture_file
            db.session.commit()
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account info has been updated successfully!', 'success')
        return redirect(url_for('profile.update_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    username = current_user.username
    email = current_user.email
    profile_pic = url_for(
        'static', filename=f'profile_pic/{current_user.image_file}')
    return render_template('profile/edit_profile.html', profile_pic=profile_pic,
                           email=email, username=username, form=form)


@profile_blueprint.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully.', 'info')
        return redirect(url_for('profile.change_password'))
    return render_template('profile/change_password.html', form=form)


@profile_blueprint.route('/<username>/')
def user_posts(username):
    page = request.args.get('page', type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(
        Post.date.desc()).paginate(per_page=5, page=page)
    return render_template('profile/profile_page.html', username=user.username, posts=posts, email=user.email,
                           profile_pic=url_for(
                               'static', filename=f'profile_pic/{user.image_file}'),
                           profile=True)
