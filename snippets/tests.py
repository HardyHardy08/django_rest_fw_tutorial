# TODO:
# - Add setUp() to TestCase classes?
# - Refactor and make tests similar to
#   https://realpython.com/test-driven-development-of-a-django-restful-api/
import json
from rest_framework import status
from django.test import TestCase
# from snippets.models import Snippet


def create_snippet(client_post_func, title=None, code=None):  # need to be defensive about post?
    if title is None:
        title = "HelloWorld using FooBar"
    else:
        title = title
    if code is None:
        code = "def foo():\n    print('hello')\n\n def bar():\n    print('world!')\n"
    else:
        code = code

    return client_post_func('/snippets/', {'title': title, 'code': code, 'linenos': True})


class SnippetListTests(TestCase):
    # def test_no_snippets(self): does this need to happen?

    def test_list_snippets(self):
        # this definitely needs to be refactored
        create_snippet(self.client.post)
        create_snippet(self.client.post, title="HelloWorld for FooBar")
        response = self.client.get('/snippets/')
        self.assertContains(response, "HelloWorld using FooBar")
        self.assertContains(response, "HelloWorld for FooBar")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_snippet(self):
        response = create_snippet(self.client.post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_snippet(self):
        response = create_snippet(self.client.post, title="", code="")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SnippetDetailTests(TestCase):
    def test_get_valid_snippet(self):
        create_snippet(self.client.post, "test the snippet get")
        response = self.client.get('/snippets/1/')
        self.assertContains(response, "test the snippet get")

    def test_get_invalid_snippet(self):
        response = self.client.get('/snippets/30/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_snippet(self):
        create_snippet(self.client.post)
        response = self.client.put(
            '/snippets/1/',
            data=json.dumps({"title": "FooBar printing HelloWorld", 'code': 'print()'}),
            content_type='application/json',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "FooBar printing HelloWorld")

    def test_invalid_update_snippet(self):
        create_snippet(self.client.post)
        response = self.client.put(
            '/snippets/1/',
            data=json.dumps({"title": "", "code": ""}),
            content_type='application/json',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_snippet(self):
        create_snippet(self.client.post)
        response = self.client.delete('/snippets/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_snippet(self):
        create_snippet(self.client.post)
        response = self.client.delete('/snippets/30/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
