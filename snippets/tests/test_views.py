# TODO:
# - Add setUp() to TestCase classes?
# - Refactor and make tests similar to
#   https://realpython.com/test-driven-development-of-a-django-restful-api/

import json
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
# from django.test import TestCase
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.urls import reverse
from django.contrib.auth.models import User


# def create_snippet(client_post_func, title=None, code=None):  # need to be defensive about post?
#     if title is None:
#         title = "HelloWorld using FooBar"
#     else:
#         title = title
#     if code is None:
#         code = "def foo():\n    print('hello')\n\n def bar():\n    print('world!')\n"
#     else:
#         code = code

#     return client_post_func('/snippets/', {'title': title, 'code': code, 'linenos': True})


class SnippetListTests(APITestCase):
    """
    Test SnippetList views to respond with proper http response codes
    """
    # def test_no_snippets(self): does this need to happen?

    def setUp(self):
        self.authorized_user_username = "hardy"
        self.authorized_user_email = "hardy@hardyhardy.com"
        self.authorized_user_password = "hardyhardy"
        self.authorized_user = User.objects.create_user(
            username=self.authorized_user_username,
            email=self.authorized_user_email,
            password=self.authorized_user_password
        )

        self.valid_snippet = {
            'title': "HelloWorld using FooBar",
            'code': "def foo():\n    print('hello')\n\n def bar():\n    print('world!')\n",
        }
        self.invalid_snippet = {
            'title': "invalid",
            'code': "",
        }

    def test_list_snippets(self):
        Snippet.objects.create(
            title="snippet one",
            code="print('Hello')",
            owner=self.authorized_user
        )
        Snippet.objects.create(
            title="snippet two",
            code="print('World')",
            owner=self.authorized_user)
        response = self.client.get(reverse('snippet-list'))
        request = APIRequestFactory().get(reverse('snippet-list'))
        serializer = SnippetSerializer(
            Snippet.objects.all(),
            many=True,
            context={'request': request}
        )
        # need to get content from 'results' key because of pagination
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # post tests
    def test_create_valid_snippet(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.post(
            reverse('snippet-list'),
            data=json.dumps(self.valid_snippet),
            content_type='application/json'
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_snippet(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.post(
            reverse('snippet-list'),
            data=json.dumps(self.invalid_snippet),
            content_type='application/json'
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_snippet_success_from_authorized_user(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.post(
            reverse('snippet-list'),
            data=json.dumps(self.valid_snippet),
            content_type='application/json'
        )
        self.client.logout()
        self.assertEqual(response.data['owner'], self.authorized_user_username)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # do not know how to make unauthorized user ... simply users that are not logged in?
    def test_new_snippet_fail_from_unauthorized_user(self):
        response = self.client.post(
            reverse('snippet-list'),
            data=json.dumps(self.valid_snippet),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SnippetDetailTests(APITestCase):
    """
    Test SnippetDetail views to respond with proper http response codes
    """

    def setUp(self):
        self.authorized_user_username = "hardy"
        self.authorized_user_email = "hardy@hardyhardy.com"
        self.authorized_user_password = "hardyhardy"
        self.authorized_user = User.objects.create_user(
            username=self.authorized_user_username,
            email=self.authorized_user_email,
            password=self.authorized_user_password
        )

        self.random_user_username = "leeroy"
        self.random_user_email = "leeroy@jenkins.com"
        self.random_user_password = "leeroyjenkins"
        self.random_user = User.objects.create_user(
            username=self.random_user_username,
            email=self.random_user_email,
            password=self.random_user_password
        )

        self.valid_snippet = {
            'title': "HelloWorld using FooBar",
            'code': "def foo():\n    print('hello')\n\n def bar():\n    print('world!')\n",
        }
        self.invalid_snippet = {
            'title': "invalid",
            'code': "",
        }

        self.authorized_user_snippet = Snippet.objects.create(
            title=self.valid_snippet['title'],
            code=self.valid_snippet['code'],
            owner=self.authorized_user
        )
        self.random_user_snipept = Snippet.objects.create(
            title=self.valid_snippet['title'],
            code=self.valid_snippet['code'],
            owner=self.random_user
        )

    # get tests

    def test_get_valid_snippet(self):
        response = self.client.get(
            reverse('snippet-detail',
                    kwargs={'pk': self.authorized_user_snippet.pk})
        )
        request = APIRequestFactory().get(
            reverse('snippet-detail',
                    kwargs={'pk': self.authorized_user_snippet.pk})
        )
        serializer = SnippetSerializer(
            Snippet.objects.get(pk=self.authorized_user_snippet.pk),
            context={'request': request}
        )
        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_snippet(self):
        response = self.client.get(
            reverse('snippet-detail', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # put tests
    def test_update_valid_snippet(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.put(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
            data={'code': "def change(): \n    return None"}
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_snippet(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.put(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
            data=self.invalid_snippet
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_user(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.put(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
            data=self.valid_snippet
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_user(self):
        self.client.login(username=self.random_user_username,
                          password=self.random_user_password)
        response = self.client.put(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
            data=self.valid_snippet
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # delete tests
    def test_delete_valid_snippet(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.delete(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_snippet(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.delete(
            reverse('snippet-detail', kwargs={'pk': 30}),
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_user(self):
        self.client.login(username=self.authorized_user_username,
                          password=self.authorized_user_password)
        response = self.client.delete(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_user(self):
        self.client.login(username=self.random_user_username,
                          password=self.random_user_password)
        response = self.client.delete(
            reverse('snippet-detail', kwargs={'pk': self.authorized_user_snippet.pk}),
        )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
