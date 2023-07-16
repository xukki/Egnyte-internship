from flask import Flask,render_template,request,abort,url_for
import openai
import sqlite3

openai.api_key="insert key here"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    #print(str(response.choices[0].message))
    #messages.append(response.choices[0].message)
    return response.choices[0].message["content"]




app = Flask(__name__)

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM messages WHERE id = ?',
                        (post_id,)).fetchone()
    conn.commit()
    if post is None:
        abort(404)
    return post

@app.route("/", methods=(["GET","POST"]))
def index():
    if request.method == 'POST':
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM messages').fetchall()
        #for post in posts:
            #print(post["mrole"])
            #print(post["content"])
        post = get_post(1)
        
        content = [{'role':'user','content':request.form["json_input"]+" "+request.form["user_input"]}]
        #messages += content
        conn.execute('INSERT INTO messages (mrole, content) VALUES (?, ?)',
                         ("user", content[0]['content']))
        conn.commit()
        msg = conn.execute('SELECT * FROM messages').fetchall()
        conn.commit()
        for i in msg:
            content += [{'role':'user','content':i["content"]}]
        messages =  [{'role':post["mrole"], 'content':post["content"]}] + content
        for i in messages:
            print(messages)

        conn.close()

        #while user_input != "end session":
        response = get_completion_from_messages(messages, temperature=0)

        return render_template("index.html",response=response,query=request.form["user_input"])
        #else:
            #messages=[]
    else:
        conn = get_db_connection()
        conn.execute('DELETE FROM messages WHERE id !=1')
        conn.commit()
        conn.close()
        return render_template("index.html",response="")
        
    

if __name__ == "__main__":
    app.run(debug=True)

