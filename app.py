from flask import Flask, request
from flask_restful import Resource, Api ,reqparse

app = Flask(__name__)
api = Api(app)


orders = [
    {
        'id': 1,
        'name':'eat'
    },
    {
        'id': 2,
        'name':'code'
    },
    {
        'id': 3,
        'name': 'sleep'
    }
]

class Orders(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, required = True,
            help = 'No order name provided', location = 'json')
        
        super(Orders, self).__init__()


    def get(self):
        return {'orders': orders}

    def post(self):
        data = self.reqparse.parse_args()
        order ={'name':data['name'], 'id':orders[-1]['id']+1}
        orders.append(order)
        return order, 201



class OrdersList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str,location = 'json')
        super(OrdersList, self).__init__()

    def get (self,id):
            # loop over the orders list and find the order with the specified id
        order = next(filter(lambda x: x['id'] == id, orders), None)
        return {'order': order}, 200 if order  else 404

    def delete(self,id):
        global orders #refer to the global list
        orders = list(filter(lambda x: x['id'] != id, orders))
        return {'message': 'order deleted'}

    def put(self,id):
        data = request.get_json()
        # check if the order exist
        order = next(filter(lambda x:x['id'] == id, orders), None)
        if order is None:
            order = {'name': data['name'], 'id':data['id']}
            orders.append(order)
        else:
            order.update(data)
        return order

        
api.add_resource(Orders ,'/api/v1/orders/')
api.add_resource(OrdersList, '/api/v1/orders/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
