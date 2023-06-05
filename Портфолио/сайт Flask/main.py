from flask import Flask, render_template,url_for,request,redirect,abort
import requests
import sqlite3


app = Flask(__name__)
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

def get_data_from_db():
    con = sqlite3.connect("info.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    data_list = []
    for row in rows:
        data_list.append(row)
    return data_list[::-1]
@app.route('/posts')
def posts():
    data = get_data_from_db()
    return render_template("posts.html",articles=data)


@app.route('/posts/<int:id>')
def post_detail(id):
    data = get_data_from_db()
    article = next((item for item in data if item[0] == id), None)
    return render_template("post-detail.html",article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    data = get_data_from_db()
    article = next((item for item in data if item[0] == id), None)
    if article is None:
        abort(404)
    try:
        if article is not None:
            con = sqlite3.connect("info.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM people WHERE id = ?", (id,))
            con.commit()
            cursor.close()
            con.close()
            return redirect("/posts")
         
    except Exception as e:
        return f'При удалении статьи произошла ошибка: {str(e)}' 
def update_data_in_db(id, title, intro, text):
    con = sqlite3.connect("info.db")
    cursor = con.cursor()

    try:
        cursor.execute("UPDATE people SET title=?, intro=?, text=? WHERE id=?", (title, intro, text, id))
        con.commit()
        cursor.close()
        con.close() 
        return redirect('/posts')
    except Exception as e:
        return f'При редактировании статьи произошла ошибка: {str(e)}'

def get_post_from_db(id):
    con = sqlite3.connect("info.db")
    cursor = con.cursor()

    try:
        cursor.execute("SELECT * FROM people WHERE id=?", (id,))
        post = cursor.fetchone()
        cursor.close()
        con.close() 
        return post
    except Exception as e:
        return f'При получении статьи произошла ошибка: {str(e)}'

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    if request.method == 'POST':
        updated_title = request.form.get('title')
        updated_intro = request.form.get('intro')
        updated_text = request.form.get('text')
 
        update_data_in_db(id, updated_title, updated_intro, updated_text)

        
        return redirect('/posts')
    else:
        article = get_post_from_db(id)

        if article is None:
            abort(404)  

        return render_template('post-update.html', article=article)

    

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        new_title = request.form.get('title')
        new_intro = request.form.get('intro')
        new_text = request.form.get('text')

        if not new_title or not new_intro or not new_text:
            return 'Заполните все поля'

        try:
            con = sqlite3.connect("info.db")
            cursor = con.cursor()

            cursor.execute("INSERT INTO people (title, intro, text) VALUES (?, ?, ?)",
                           (new_title, new_intro, new_text))
            con.commit()

            cursor.close()
            con.close()

            return redirect('/posts')
        except Exception as e:
            return f'При добавлении статьи произошла ошибка: {str(e)}'
    else:
        return render_template("create-article.html")
if __name__ == "__main__":
    app.run(debug=True) 