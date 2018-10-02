from django.test import TestCase
from snippets.models import Snippet, User


class SnippetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create({
            # create a user
        }
        )

    def test_new_snippet_require_owner(self):
        invalid_snippet = Snippet.objects.create({
            "title": "Test Snippet",
            "code": "some lines of code",
            "linenos": True,
            "owner": "",
        })
        self.assertEqual(invalid_snippet, False)