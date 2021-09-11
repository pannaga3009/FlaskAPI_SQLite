from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True, help = "This field cannot be left blank")
    #required = True means no request should come through without price.
    #change in get method
    #@app.route('/student')
    #No need to do jsonify here because restful does it for us so we can return dictionary
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404


        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item' : item}, 200 if item is not None else 404
#Filter function alone won't return but when you use a list function on filter - it returns, where as next() will give the first item matched by that item
#So here filter function takes lambda x: x['name'] == name as filter and items are the list of things we will be filtering.
#The most popular http status code = 200
#The rror code for not found is 404

    @classmethod
    def find_by_name(cls, name):
        #To retrieve items from the database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone() #Willl give only one row with specific name
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}



    def post(self, name):
        if self.find_by_name(name):
        # if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' exists already".format(name)}, 400

        data = Item.parser.parse_args()


        # data = request.get_json()
        #Force = true neutralizes content type error, silent = True gives none
        item = {'name': name, 'price': data['price']}
        # items.append(item) ---- used when there is a list to append but now we will try to append into database
        #Writing items into the database
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred nserting the item"}, 500
            #Internal server error

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT into items VALUES (?,?)"
        result = cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self,name):
        # global items #Items variable in the block is the outer items list
        # items = list(filter(lambda x: x['name'] != name, items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "Delete from items where name=?"
        result = cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': "Item {} deleted".format(name)}

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "Update items set price=? where name=?"
        result = cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()




#put can be used to both create item and update the existing item
    def put(self,name):
        data = Item.parser.parse_args()
        #data = request.get_json()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return{"message": "An error occurred inserting items"},500
        else:
            try:
                self.update(updated_item) #Dictionary have update item
            except:
                return{"message": "An error occurred updating items"},500
        return updated_item

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})


        connection.close()
        return {'items': items}
