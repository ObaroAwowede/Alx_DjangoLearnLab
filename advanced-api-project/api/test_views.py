# api/test_views.py
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Book, Author


class BookAPITestCase(APITestCase):
    """
    Tests for Book API endpoints:
      - List, Detail
      - Create, Update, Delete
      - Filtering, searching, ordering on list endpoint
    """

    def setUp(self):
        # Clients
        self.client = APIClient()

        # Users
        self.user = User.objects.create_user(username="tester", password="password123")
        self.other_user = User.objects.create_user(username="other", password="password123")

        # Authors
        self.author_a = Author.objects.create(name="Eichiro Oda")
        self.author_b = Author.objects.create(name="J.R Tolkien")

        # Books
        self.book1 = Book.objects.create(
            title="Wanted", publication_year=1992, author=self.author_a
        )
        self.book2 = Book.objects.create(
            title="One piece", publication_year=1997, author=self.author_a
        )
        self.book3 = Book.objects.create(
            title="LOTR", publication_year=1954, author=self.author_b
        )

        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")

    def test_list_books_anonymous_allowed(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        self.assertTrue(isinstance(res.data, list))
        titles = [item["title"] for item in res.data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertIn(self.book3.title, titles)

    def test_detail_book_anonymous_allowed(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.book1.title)
        self.assertEqual(res.data["publication_year"], self.book1.publication_year)

    def test_create_book_requires_authentication(self):
        payload = {"title": "New Book", "publication_year": 2024, "author": self.author_a.pk}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "New Book", "publication_year": 2024, "author": self.author_a.pk}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_id = res.data.get("id")
        self.assertIsNotNone(created_id)
        created = Book.objects.get(pk=created_id)
        self.assertEqual(created.title, payload["title"])
        self.assertEqual(created.publication_year, payload["publication_year"])
        self.assertEqual(created.author.pk, payload["author"])

    def test_create_book_validation_errors(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "", "publication_year": 2024, "author": self.author_a.pk}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.filter(title="").count(), 0)

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        res = self.client.patch(url, {"title": "Wanted"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Wanted")

    def test_update_book_unauthenticated_forbidden(self):
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        res = self.client.patch(url, {"title": "Hacked Title"}, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, "Hacked Title")

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", kwargs={"pk": self.book3.pk})
        res = self.client.delete(url)
        
        # DRF DestroyAPIView normally returns 204 No Content
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())

    def test_delete_book_unauthenticated_forbidden(self):
        url = reverse("book-delete", kwargs={"pk": self.book2.pk})
        res = self.client.delete(url)
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertTrue(Book.objects.filter(pk=self.book2.pk).exists())

    def test_filter_by_author_name(self):
        # search for author_a books using filter param 'author_name'
        res = self.client.get(self.list_url, {"author_name": "Tolkien"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertNotIn(self.book3.title, titles)

    def test_filter_by_publication_year_range(self):
        """Filtering by pub_year_min and pub_year_max should return correct books."""
        res = self.client.get(self.list_url, {"pub_year_min": 1990, "pub_year_max": 2022})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertNotIn(self.book3.title, titles)

    def test_search_title_and_author(self):
        """Search should match title and author__name per search_fields."""
        # search for 'piece' should match One Piece
        res = self.client.get(self.list_url, {"search": "piece"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn(self.book3.title, titles)
        
        # search for 'Oda' should match books by Oda
        res2 = self.client.get(self.list_url, {"search": "Oda"})
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        titles2 = [b["title"] for b in res2.data]
        self.assertIn(self.book1.title, titles2)
        self.assertIn(self.book2.title, titles2)
        self.assertNotIn(self.book3.title, titles2)

    def test_ordering_publication_year(self):
        # ascending
        res = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years))

        # descending order
        res_desc = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(res_desc.status_code, status.HTTP_200_OK)
        years_desc = [b["publication_year"] for b in res_desc.data]
        self.assertEqual(years_desc, sorted(years_desc, reverse=True))
