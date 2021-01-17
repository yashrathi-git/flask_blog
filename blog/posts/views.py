from flask import Blueprint,render_template,redirect,url_for,flash,abort,request
from blog.posts.forms import AddPost,DeletePost
from blog.model import Post
from blog import db,app
from flask_login import login_required,current_user
posts_blueprint = Blueprint('posts',
                            __name__,)


@posts_blueprint.route('/add/',methods=['GET','POST'])
@login_required
def add():
    form = AddPost()
    if form.validate_on_submit():
        post = Post(current_user.id,
                    form.title.data,
                    form.post.data,
                    form.short_description.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('posts/add_post.html',form=form,title='Add Post')
@posts_blueprint.route('/<int:post_id>/')
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = DeletePost()
    return render_template('posts/single_post.html',post=post,form=form)

@posts_blueprint.route('/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    form = AddPost()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    
    if form.validate_on_submit():
        post.title = form.title.data 
        post.short_description = form.short_description.data
        post.post = form.post.data
        db.session.commit()
        return redirect(url_for('posts.single_post',post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.short_description.data = post.short_description
        form.post.data = post.post
    return render_template('posts/add_post.html',form=form,title = 'Edit Post')

@posts_blueprint.route('/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))