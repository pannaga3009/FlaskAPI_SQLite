from flask import Flask, request
from flask_restful import Resource, Api, reqparse
#Set up JWT to work with our app
from flask_jwt import JWT, jwt_required
#Resouce are usually mapped in database table as well
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #/auth

#When we intialize JWT object then that is gonna use our app , authenticate and identity.
#When we call /auth we send username and password and sends it over authenticate function.
#/auth endpoint sends a JWT token, then calls identity function to get correct userid and password

items = []
#The api works with resources and every resource must be an app.
#Inheritence
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True, help = "This field cannot be left blank")
    #required = True means no request should come through without price.
    #change in get method
    #@app.route('/student')
    #No need to do jsonify here because restful does it for us so we can return dictionary
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item' : item}, 200 if item is not None else 404
#Filter function alone won't return but when you use a list function on filter - it returns, where as next() will give the first item matched by that item
#So here filter function takes lambda x: x['name'] == name as filter and items are the list of things we will be filtering.
#The most popular http status code = 200
#The rror code for not found is 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' exists already".format(name)}, 400

        data = Item.parser.parse_args()


        # data = request.get_json()
        #Force = true neutralizes content type error, silent = True gives none
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201



    def delete(self,name):
        global items #Items variable in the block is the outer items list
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "Item {} deleted".format(name)}


#put can be used to both create item and update the existing item
    def put(self,name):
        data = Item.parser.parse_args()
        #data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price' : data['price']}
            items.append(item)
            return item, 201
        else:
            item.update(data) #Dictionary have update item
            return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)
    #name is directly related to get name parameter



    #Post method



@app.route('/')
def home():
    return "Hello World"
