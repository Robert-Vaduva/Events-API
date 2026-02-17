import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from models import User


class TestUserLogic(unittest.TestCase):
    def test_password_hashing_and_verification(self):
        u = User(username='John')
        u.set_password('S3cret_Pass!')

        self.assertNotEqual(u.password_hash, 'S3cret_Pass!')

        self.assertTrue(u.check_password('S3cret_Pass!'))

        self.assertFalse(u.check_password('Other_Pass'))

    def test_to_dict_format(self):
        u = User(username='test_user', is_admin=True)
        data = u.to_dict()

        self.assertEqual(data['username'], 'test_user')
        self.assertEqual(data['is_admin'], True)
        self.assertIsNone(data['id'])
        self.assertIsNone(data['created_at'])


if __name__ == '__main__':
    unittest.main()
