from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/index')
def index():

    with open('data.json', 'r') as file:
        posts = json.load(file)

    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with open('data.json', 'r') as file:
            blog_posts = json.load(file)
        id_number = len(blog_posts) + 1
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        new_data = {
            'id': int(id_number),
            'author': author,
            'title': title,
            'content': content
        }

        data_file = 'data.json'

        # Read existing data from the JSON file
        with open(data_file, 'r') as file:
            data = json.load(file)

        # Append new info
        data.append(new_data)

        # Write updated data back to JSON file
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open('data.json', 'r') as handle:
        blog_posts = json.load(handle)

    for i in range(len(blog_posts)):
        if int(blog_posts[i]['id']) == post_id:
            del blog_posts[i]
            break

    with open('data.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))

# route for displaying the update form
@app.route('/update/<int:post_id>', methods=["GET"])
def update_form(post_id):
    with open('data.json', 'r') as handle:
        blog_posts = json.load(handle)
    return render_template('update.html', post=blog_posts[post_id-1])

# route the handling the form submission
@app.route('/update/<int:post_id>', methods=['POST'])
def update_post(post_id):
    with open('data.json', 'r') as handle:
        blog_posts = json.load(handle)
    author = request.form['author']
    title = request.form['title']
    content = request.form['content']

    # Update the post with the new author
    post = blog_posts[post_id-1]
    post['author'] = author
    post['title'] = title
    post['content'] = content

    for post in blog_posts:
        if post['id'] == int(post_id):
            post['author'] = author
            post['title'] = title
            post['content'] = content

    sorted_blog_posts = sorted(blog_posts, key=lambda x: x['id'])
    with open('data.json', 'w') as file:
        json.dump(sorted_blog_posts, file, indent=4)

    return redirect(url_for('index'))

@app.route('/star_update/<post_star>')
def star_update(post_star):
    with open('data.json', 'r') as file:
        blog_posts = json.load(file)
    for post in blog_posts:
        if post['author'].lower() == post_star.lower():
            post['count'] += 1
            post['star_class'] = 'red'
            break

    with open('data.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5025, debug=True)
