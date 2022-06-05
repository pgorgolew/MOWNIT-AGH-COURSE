from app import app
from flask import render_template, flash, redirect, url_for, session
from app.forms import ArticleSearcherForm
from app.logic.article_finder import find


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ArticleSearcherForm()
    if form.validate_on_submit():  # if post it is true and validate all data
        flash(f'Searching articles for `{form.input.data}`')  # stored somehow in flask, can be shown
        articles = find(form.input.data, form.num_of_articles.data)
        session['articles'] = articles
        return redirect(url_for('results'))
    return render_template('index.html', form=form)


@app.route('/results')
def results():
    if 'articles' not in session:
        session['articles'] = list()
    return render_template('results.html', articles=session['articles'])
