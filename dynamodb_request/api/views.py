from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from api.dynamo_models import Fruit
from boto3 import client

dynamodb_client = client('dynamodb')

class DynamoListRequest(APIView):
    def get(self, request):
        response = []
        items = dynamodb_client.scan(TableName='Fruits')['Items']
        for item in items:
            fruit = Fruit(item['Name']['S'])
            fruit.price = item.get('Price',{}).get('N', '')
            response.append(fruit.__dict__)
        return Response(response)
    
    def post(self, request):
        request_data = request.data
        item = {'Name': {'S': request_data['Name']}}

        if 'Price' in request_data:
            item['Price'] = {'N': request_data['Price']}

        dynamodb_client.put_item(
            TableName = 'Fruits',
            Item = item
        )
        return Response(status=status.HTTP_201_CREATED)


class DynamoDetailRequest(APIView):
    def get(self, request, pk):
        item = dynamodb_client.get_item(
            TableName = 'Fruits',
            Key = {
                'Name': {'S': pk},
            }
        )['Item']
        fruit = Fruit(item['Name']['S'])
        fruit.price = item.get('Price',{}).get('N', '')
        return Response(fruit.__dict__)
    
    def put(self, request, pk):
        request_data = request.data

        item = dynamodb_client.get_item(
            TableName = 'Fruits',
            Key = {
                'Name': {'S': pk},
            }
        )['Item']

        price = item.get('Price',{}).get('N', '0')

        if 'Price' in request_data:
            price = request_data['Price']

        dynamodb_client.put_item(
            TableName = 'Fruits',
            Item = {
                'Name': {'S': item['Name']['S']},
                'Price': {'N': price}
            }
        )

        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        dynamodb_client.delete_item(
            TableName = 'Fruits',
            Key = {
                'Name': {'S': pk},
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

