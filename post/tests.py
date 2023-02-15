from django.test import TestCase
from django.shortcuts import reverse
from .models import Post

class HarChiDostDari(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title = 'test',
            description = 'test aval',
            image = 'no image',
            creator = 'hossein',
            create_at = '2020-11-11 10:43',
        )

    def test_find_url(self): #Error
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_finding_url_by_name(self): #OK
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_finding_post_title_in_page(self): #OK
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.post.title)
        self.assertEqual(self.post.title, 'test')