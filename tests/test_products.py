from .base import BaseTestClass, to_json
import unittest, re

from .test_users import create_user


def create_product(client, name, price, token):
    return client.post(
        '/products',
        data={
            "name": name,
            "price": price,
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

class ProductsCase(BaseTestClass):

    def test_products(self):
        access_token = to_json(create_user(self.client, "username", "password").data)['payload']['access_token']

        print('- Get all products')
        res = self.client.get('/products', 
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Create product')
        res = self.client.post('/products', 
            data={
                "name": "Vino A",
                "price": 5000,
                "description": "Un vino"
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(201, res.status_code)

        print('- Create product - error if product already exists')
        res = self.client.post('/products', 
            data={
                "name": "Vino A",
                "price": 5000,
                "description": "Un vino"
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(400, res.status_code)

        print('- Get product data')
        res = self.client.get(f'/products/1',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Get product data - error if product not exists')
        res = self.client.get(f'/products/990',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Edit product data')
        res = self.client.put(f'/products/1',
            data={
                "name": "Vino B",
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Edit product data - error if product already exists')
        res = self.client.put(f'/products/1',
            data={
                "name": "Vino B",
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(400, res.status_code)

        print('- Edit product data - error if product not exists')
        res = self.client.put(f'/products/999',
            data={
                "name": "Vino B",
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Delete product')
        res = self.client.post(
            '/products',
            data={
                "name": "Vino Test",
                "price": 500000,
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        id = to_json(res.data)['payload']['product']['id']

        res = self.client.delete(f'/products/{id}',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Delete product - error if product not exists')
        res = self.client.delete(f'/products/9999',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)