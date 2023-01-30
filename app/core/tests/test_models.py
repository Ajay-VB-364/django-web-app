"""Testing models"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


class Models(TestCase):

    def test_create_user_by_email(self):
        """ Test user creation by email """
        email = "test@example.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test email  """
        sample = [
            ['test1@Example.com', 'test1@example.com'],
        ]

        for email, expected in sample:
            user = get_user_model().objects.create_user(email, 'sample')

            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """ Test email is must """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample')

    def test_create_super_user(self):
        """ Test super user """
        email = "test@example.com"
        password = "password"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        """ Test Recipe creation """
        email = "test@example.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe',
            time_minutes=5,
            price=Decimal('5.5'),
            description='Sample Recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """ Test Tag creation """
        email = "test@example.com"
        password = "password"
        new_user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        tag = models.Tag.objects.create(user=new_user, name='New')

        self.assertEqual(str(tag), tag.name)
    
    def test_create_ingredient(self):
        """ Test Ingredient creation """
        email = "test@example.com"
        password = "password"
        new_user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        ingredient = models.Ingredient.objects.create(user=new_user, name='New')

        self.assertEqual(str(ingredient), ingredient.name)
