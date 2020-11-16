from .base import BaseTestClass, to_json
import unittest, re

from .test_users import create_user
from .test_products import create_product

from .helpers import products, users, sales

class SalesCase(BaseTestClass):

    def test_products(self):
        # Init users
        for x in users:
            create_user(self.client, x['username'], x['password'])

        access_token = to_json(create_user(self.client, "username", "password").data)['payload']['access_token']

        # Init products
        for x in products:
            create_product(self.client, x['name'], x['price'], access_token)


        print('- Get all sales')
        res = self.client.get('/sales', 
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Create sales')
        for x in sales:
            res = self.client.post('/sales', 
                data={
                    "user_id": x["user_id"],
                    "product_id": x["product_id"],
                    "date": x["date"],
                },
                headers={
                    'Authorization': f'Bearer {access_token}'
                }
            )
            self.assertEqual(201, res.status_code)

        print('- Create sales - error if user doesnt exists')
        res = self.client.post('/sales', 
            data={
                "user_id": 99999,
                "product_id": 1,
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Create sales - error if product doesnt exists')
        res = self.client.post('/sales', 
            data={
                "user_id": 1,
                "product_id": 99999,
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Get sale data')
        res = self.client.get(f'/sales/1',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Get sale data')
        res = self.client.get(f'/sales/9999',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Delete sale')
        res = self.client.delete(
            '/sales/1',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Delete sale - error if not exists')
        res = self.client.delete(f'/sales/9999',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)