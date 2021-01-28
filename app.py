from blog import app
from flask import render_template, request
from blog.model import Post


@app.route('/')
def home():
    search_term = request.args.get('search')
    page = request.args.get('page', type=int)

    if search_term:
        q = '%{}%'.format(search_term)
        posts = Post.query.filter(Post.title.ilike(q) | Post.short_description.ilike(q) | Post.author.has(username=search_term))\
            .order_by(Post.date.desc()).paginate(per_page=5, page=page)
    else:
        posts = Post.query.order_by(
            Post.date.desc()).paginate(per_page=5, page=page)

    return render_template('posts/index.html', posts=posts, search_term=search_term)


if __name__ == '__main__':
    app.run()
