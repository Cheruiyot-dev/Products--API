from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

Base = declarative_base()

app = Flask(__name__)

#  Tables
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    buying_price = Column(Integer)
    selling_price = Column(Integer)

    def __init__(self,name,buying_price,selling_price):
        self.name = name
        self.buying_price = buying_price
        self.selling_price = selling_price


    def __repr__(self):
        return f"({self.id} {self.name} {self.buying_price} {self.selling_price})"

engine = create_engine('sqlite:///duka.db', echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine) 
session = Session()

@app.route('/')
def hello():
    return jsonify({"name": "Your name"}), 200

@app.route('/products', methods=['POST', 'GET'])
def create_product():
    if request.method == 'POST':
        data= request.json
        name=data.get('name')
        buying_price = data.get('buying_price')
        selling_price = data.get('selling_price')

        product = Products(name=name, buying_price=buying_price, selling_price=selling_price)
        session.add(product)
        session.commit()

        response_body = {"id": product.id, "name": name, "buying_price": buying_price, "selling_price": selling_price}

        return jsonify(response_body), 201

    else: 
        products = session.query(Products).all()
        response_body = []
        for product in products:
            response_body.append({"id": product.id, "name": product.name, "buying_price": product.buying_price, "selling_price": product.selling_price})
        return jsonify(response_body), 200
   
    
    # return jsonify(response_body), 201
    
if __name__ == '__main__':
    app.run(debug=True)
    
