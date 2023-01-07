from flask import Flask, render_template, request
from PyDictionary import PyDictionary
import sqlite3

app = Flask(__name__)
dictionary = PyDictionary()

conn = sqlite3.connect('learning-list.db')
#conn.execute('CREATE TABLE newLearningList (word TEXT, noOfSearches)')
#conn.execute('CREATE TABLE masteredList (word TEXT, noOfSearches)')


@app.route("/", methods=['GET','POST'])
def index():
    masteredWord = request.form.get("mastered-word")
    if masteredWord:
        with sqlite3.connect('learning-list.db') as con:
            cur = con.cursor()
            query = "INSERT INTO masteredList (word, noOfSearches) VALUES (?, ?)"
            val = (masteredWord, 1)
            cur.execute(query, val)

            query = "DELETE FROM newLearningList WHERE word = ?"
            val = (masteredWord, )
            cur.execute(query, val)

            con.commit()

    learnedWord = request.form.get("learned-word")
    if learnedWord:
        with sqlite3.connect('learning-list.db') as con:
            cur = con.cursor()
            query = "INSERT INTO newLearningList (word, noOfSearches) VALUES (?, ?)"
            val = (learnedWord, 1)
            cur.execute(query, val)

            query = "DELETE FROM masteredList WHERE word = ?"
            val = (learnedWord,)
            cur.execute(query, val)

            con.commit()

    with sqlite3.connect('learning-list.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("select * from newLearningList")
        learnedRows = cur.fetchall();

        cur.execute("select * from masteredList")
        masteredRows = cur.fetchall();

    return render_template("index.html", learnedRows = learnedRows, masteredRows = masteredRows)

@app.route("/search",methods=['GET','POST'])
def search():
    word = request.form.get("word")
    meanings = dictionary.meaning(word)
    word_types = meanings.keys()

    with sqlite3.connect('learning-list.db') as con:
        cur = con.cursor()
        query = "INSERT INTO newLearningList (word, noOfSearches) VALUES (?, ?);"
        val = (word, 1)
        cur.execute(query, val)

        con.commit()

    return render_template("result.html",
                           word = word.capitalize(),
                           word_types = word_types,
                           meanings=meanings)


conn.close()


if __name__ == '__main__':
    app.run(debug=True)