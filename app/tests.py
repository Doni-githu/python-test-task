from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Comic, Rating


class ComicViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.comic = Comic.objects.create(title='Comic 1', author=self.user)

    def test_list_comics(self):
        response = self.client.get('/api/comic/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.comic.title)

    def test_create_comic(self):
        data = {
            'title': 'New Comic',
            'author_id': self.user.id
        }

        response = self.client.post('/api/comic/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['author']['username'], self.user.username)

    def test_retrieve_comic(self):
        response = self.client.get(f'/api/comic/{self.comic.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.comic.title)

    def test_update_comic(self):
        data = {
            'title': 'Updated Comic',
            'author_id': self.user.id
        }

        response = self.client.put(f'/api/comic/{self.comic.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['author']['username'], self.user.username)

    def test_delete_comic(self):
        response = self.client.delete(f'/api/comic/{self.comic.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comic.objects.filter(id=self.comic.id).exists())


class CreateRatingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.comic = Comic.objects.create(title='Comic 1', author=self.user)

    def test_create_rating(self):
        data = {
            'comic_id': self.comic.id,
            'user_id': self.user.id,
            'value': 4,
        }

        response = self.client.post('/api/ratings/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 4.0)

        self.comic.refresh_from_db()
        self.assertEqual(self.comic.rating, 4.0)

    def test_update_rating(self):
        rating = Rating.objects.create(comic_id=self.comic, user_id=self.user, value=3)

        data = {
            'comic_id': self.comic.id,
            'user_id': self.user.id,
            'value': 5,
        }

        response = self.client.post('/api/ratings/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 5.0)

        rating.refresh_from_db()
        self.assertEqual(rating.value, 3)

        self.comic.refresh_from_db()
        self.assertEqual(self.comic.rating, 4)


class GetRatingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.comic = Comic.objects.create(title='Comic 1', author=self.user)

    def test_get_rating(self):
        Rating.objects.create(comic_id=self.comic, user_id=self.user, value=4)
        Rating.objects.create(comic_id=self.comic, user_id=self.user, value=5)

        response = self.client.get(f'/api/comics/{self.comic.id}/rating/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4.5)