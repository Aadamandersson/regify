from flask import Flask, render_template, flash, request
app = Flask(__name__)

@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/api')
def api():
   return render_template('api.html')

@app.route('/header')
def header():
   return render_template('header.html')

if __name__ == '__main__':
    app.run(debug=True)
