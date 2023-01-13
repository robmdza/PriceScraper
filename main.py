# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from MLSearch import start
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#from flask_mako import

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/rober/PycharmProjects/PriceScraper/database.db'
db.init_app(app)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    shipping = db.Column(db.Float)
    condition = db.Column(db.String)
    url = db.Column(db.String)


@app.route('/')
def flask_show_table():
    # items = db.session.query(Item).all()
    items = Item.query.order_by(Item.price).all()
    return render_template('table.html', items=items)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi()
    start()
    app.run(port=5000)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
