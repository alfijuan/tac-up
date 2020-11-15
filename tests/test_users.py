from .base import BaseTestClass, to_json
import unittest, re


def create_user(client, user, password):
    return client.post('/users',
        data={
            "username": user,
            "password": password,
        }
    )


def login(client, user, password):
    return client.post(
        '/login',
        data={
            "username": user,
            "password": password,
        }
    )


class UsersCase(BaseTestClass):
    
    def test_users(self):
        username = "alfi4112"
        password = "123"

        print('- Able to create a new user')
        res = self.client.post(
            '/users',
            data={
                "username": username,
                "password": password,
                "first_name": "Juan",
                "last_name": "Alfieri"
            }
        )
        self.assertEqual(201, res.status_code)
        
        print('- Error if user already exists')
        res = self.client.post(
            '/users',
            data={
                "username": username,
                "password": password,
            }
        )
        self.assertEqual(400, res.status_code)

        print('- Login with recently created user')
        res = login(self.client, username, password)
        self.assertEqual(200, res.status_code)
        self.assertTrue(to_json(res.data)['payload']['access_token'])
        self.assertTrue(to_json(res.data)['payload']['refresh_token'])

        print('- Login with incorrect user')
        res = login(self.client, "testuser", "testpassword")
        self.assertEqual(400, res.status_code)

        access_token = to_json(login(self.client, username, password).data)['payload']['access_token']

        print('- Get all users')
        res = self.client.get('/users', 
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Get user data')
        res = self.client.get(f'/users/1',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Get user data - error if user not exists')
        res = self.client.get(f'/users/990',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Edit user data')
        res = self.client.put(f'/users/1',
            data={
                "first_name": "Juan Change",
                "last_name": "Alfieri 2"
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)
        self.assertEqual(to_json(res.data)['payload']['user']['first_name'], "Juan Change")
        self.assertEqual(to_json(res.data)['payload']['user']['last_name'], "Alfieri 2")

        print('- Edit user data - error if username already exists')
        res = self.client.put(f'/users/1',
            data={
                "username": "alfi4112"
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(400, res.status_code)

        print('- Edit user data - error if user doesnt exists')
        res = self.client.put(f'/users/2222',
            data={
                "username": "alfi4112"
            },
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)

        print('- Delete user')
        res = self.client.post(
            '/users',
            data={
                "username": "alfitest",
                "password": "123",
            }
        )
        id = to_json(res.data)['payload']['user']['id']

        res = self.client.delete(f'/users/{id}',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(200, res.status_code)

        print('- Delete user - error if user doesnt exists')
        res = self.client.delete(f'/users/222',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        self.assertEqual(404, res.status_code)
        
