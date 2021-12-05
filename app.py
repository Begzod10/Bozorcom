from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import Column, Integer, String
import json
import pandas as pd
import requests
from pprint import pprint
import geocoder
import folium

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'bozor')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    # g = geocoder.ip('me')
    # myAddress = g.latlng
    #
    # my_map1 = folium.Map(location=myAddress,zoom_start=12)

    # with open('shopsList/Bozor va savdo majmualari roʻyxati 09.04.2021 yil holatiga.json','r') as outfile:
    #     text = json.loads(outfile)
    # print(text)

    # with open("shopsList/Toshkent viloyatidagi bozorlar va savdo majmualari ro‘yxati 2021 yil 2-chorak holatiga.json",encoding='utf-8', newline='') as file:
    #     reader_Qoraqalpogiston = json.load(file)
    #     for i in reader_Qoraqalpogiston:
    #         print()

    # Products.query.filter_by(id=6).update({'shop_id':2})
    add = Products(product_name="")
    db.session.add(add)
    db.session.commit()
    return render_template('Home/Home.html')


@app.route('/selectDirect')
def selectDirect():
    regions = Region.query.all()
    products = Products.query.all()
    categories = []
    for pr in products:
        categories.append(pr.cattegory)
    categories = list(dict.fromkeys(categories))
    print(categories)
    return render_template('User/SelectDirection.html', regions=regions, products=products, categories=categories)


@app.route('/collectInfo', methods=['GET', "POST"])
def collectInfo():
    if request.method == "POST":
        region = request.form.get('region')
        category = request.form.get('category')
        product_name = request.form.get('product_name')
        region_list = Region.query.filter_by(region_name=region).first()
        product_one = Products.query.filter_by(product_name=product_name).first()
        product = Products.query.filter_by(product_name=product_name).all()
        for pr in product:
            bazar_list = Bazar.query.filter_by(region_id=region_list.id, id=pr.bazar_id).all()
            print(len(bazar_list))
            return render_template('User/UserSettings.html', bazar_list=bazar_list, region=region, category=category,
                                   product_name=product_name,product_one=product_one)
        return render_template('User/UserSettings.html', region=region, category=category, product_name=product_name,
                               product_one=product_one)

    with open("shopsList/Qoraqalpogiston Respublikasida bozorlar va savdo majmualari ro'yahati.json", encoding='utf-8',
              newline='') as file:
        reader_Qoraqalpogiston = json.load(file)
    return render_template("User/UserSettings.html", reader_Qoraqalpogiston=reader_Qoraqalpogiston)


@app.route('/getCordinator/<int:place_id>')
def getCordinator(place_id):
    with open("shopsList/Qoraqalpogiston Respublikasida bozorlar va savdo majmualari ro'yahati.json", encoding='utf-8',
              newline='') as file:
        reader_Qoraqalpogiston = json.load(file)
    bazar_list = Bazar.query.filter_by(id=place_id).first()
    location = bazar_list.cordinates

    # new_location = location.replace("\"", "")
    # loc = [new_location]
    #
    # final = ('[%s]' % ', '.join(map(str, loc)))
    #
    # final2 = ("[{0}]".format(
    #     ', '.join(map(str, loc))))
    for i in reader_Qoraqalpogiston:

        if bazar_list.id == int(i.get('id')):
            my_map1 = folium.Map(location=i.get("G7"), zoom_start=12)
            return my_map1._repr_html_()


@app.route('/find_product/', methods=['POST'])
def find_product():
    body = {}
    region = request.get_json()['region']
    print(region)
    category = request.get_json()['category']
    product = request.get_json()['product']
    region_list = Region.query.filter_by(region_name=region).first()
    category_list = Products.query.filter_by(cattegory=category).first()
    products = Products.query.filter_by(product_name=product, region_id=region_list.id,
                                        cattegory=category_list.cattegory).all()
    product_names = []
    for pr in products:
        product_names.append(pr.product_name)
    product_names = list(dict.fromkeys(product_names))
    # print(product)
    # if product in product_names:
    #     print('yes')
    # else:
    #     print('no')
    products_ilike = Products.query.filter(Products.product_name.ilike("%" + product + "%"),
                                           Products.region_id == region_list.id,
                                           Products.cattegory == category_list.cattegory).all()
    products_name_ilike = []
    for pr in products_ilike:
        products_name_ilike.append(pr.product_name)
    products_name_ilike = list(dict.fromkeys(products_name_ilike))
    found = False
    if products_ilike:
        found = True
    body['product'] = product
    body['found'] = found
    return jsonify(body)


from models import *

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
