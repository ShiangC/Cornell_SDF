from flask import Flask, render_template, url_for, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from Decision_Model import tradespace_explore
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Outputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<%r>' % self.id


priceVector = {
                'yield': 100,
                'electricity': 10,
                'water': 5,
                'pesticides': 50,
                'labor': 300
            }
ts = None


def generate():
    ts = tradespace_explore.Tradespace(0, priceVector)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generate')
def generate_ts():
    def inner():
        # proc = subprocess.Popen(
        #     generate(),  # call something with a lot of output so we can see it
        #     shell=True,
        #     stdout=subprocess.PIPE
        # )
        proc = subprocess.run(generate(), stdout=subprocess.PIPE)
        print(proc.stdout.readline())
        for line in iter(proc.stdout.readline, ''):
            # yield line.rstrip() + '<br/>\n'
            new_output = Outputs(content=line.rstrip())
            db.session.add(new_output)
            db.session.commit()

    inner()
    outputs = db.Outputs.query.order_by(Outputs.id).all()
    return render_template('index.html', output=outputs)



if __name__ == "__main__":
    app.run(debug=True)
