# TODO: Create the rest of the methods in SnippetListTests and SnippetDetailTests
import json
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
        create_snippet(self.client.post)
        create_snippet(self.client.post, title="HelloWorld for FooBar")
        response = self.client.get('/snippets/')
        self.assertContains(response, "HelloWorld using FooBar")
        self.assertContains(response, "HelloWorld for FooBar")

    def test_create_snippet(self):
        response = create_snippet(self.client.post)
        self.assertEqual(response.status_code, 201)


class SnippetDetailTests(TestCase):
    def test_get_snippet(self):
        create_snippet(self.client.post, "test the snippet get")
        response = self.client.get('/snippets/1/')
        self.assertContains(response, "test the snippet get")

    def test_delete_snippet(self):
        create_snippet(self.client.post)
        response = self.client.delete('/snippets/1/')
        self.assertEqual(response.status_code, 204)

    def test_update_snippet(self):
        create_snippet(self.client.post)
        response = self.client.put(
            '/snippets/1/',
            data=json.dumps({"title": "FooBar printing HelloWorld", 'code': 'print()'}),
            content_type='application/json',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FooBar printing HelloWorld")
