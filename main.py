from flask import Flask,render_template



app = Flask(__name__)


@app.route("/")
def home():
  return render_template('index.html')

@app.route("/dash")
def dash():
  return render_template('dash.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/contact")
def contact():
  return render_template('contact.html')



@app.route("/logins")
def logins():
  return render_template('logins.html')

@app.route("/logint")
def logint():
  return render_template('logint.html')

@app.route("/register")
def register():
  return render_template('register.html')



# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)