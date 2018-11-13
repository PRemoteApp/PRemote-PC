import unittest
from app import get_user, formatMail
import os

class TestUserDetails(unittest.TestCase):

    def test_email_formatting(self):
        self.assertEqual(formatMail("test@gmail.com"), "test@gmail,com")

    def test_user_parsing(self):
        # Setup
        detailsFile = open("data.txt", "w+")
        detailsFile.write("username:password")
        detailsFile.close()

        # Test
        self.assertEqual(get_user(), ["username", "password"])

        # Delete data.txt file after text
        os.remove("data.txt")


if __name__ == '__main__':
    unittest.main()
