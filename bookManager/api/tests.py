from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Book
from django.utils import timezone
from django.urls import reverse

class BookAPITest(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create_user(username="owner", password="pass")
        self.user_intruder = User.objects.create_user(username="intruder", password="pass")
        self.creation_time = timezone.now
        self.book_owner = Book.objects.create(
            user = self.user_owner,
            title = "Owner Book Title",
            completed = False,
            # created_at = self.creation_time,
        )
        self.book_intruder = Book.objects.create(
            user = self.user_intruder,
            title = "Intruder Book Title",
            completed = False,
            # created_at = self.creation_time,
        )
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse("book-detail", args = [self.book_owner.id])
        self.book_data = {"title" : "API Book title", "completed" : False, "author": "API Author"}

    def test_only_authenticated_user_can_create_book(self):
        self.client.force_authenticate(user = self.user_owner)
        initial_book_count = Book.objects.count()
        response = self.client.post(self.book_list_url, self.book_data, format = "json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), initial_book_count + 1)
        new_book = Book.objects.latest("id")
        self.assertEqual(response.data["id"], new_book.id)
        self.assertEqual(new_book.user, self.book_owner.user)