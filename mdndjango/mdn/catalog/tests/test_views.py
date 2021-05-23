import datetime

from django.utils import timezone
from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
from catalog.models import Author, BookInstance, Book, Genre, Language

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Tony {author_id}',
                last_name=f'Surname {author_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_name_of_url(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagi_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_list_of_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)

class LoanedBookInstancesByUserListViewTest(TestCase):
    def setUp(self):
        # Create 2 users
        test_user_1 = User.objects.create_user(username='tara1', password='tara3676')
        test_user_2 = User.objects.create_user(username='tara2', password='sitara2356')

        test_user_1.save()
        test_user_2.save()

        # Create a book
        test_author = Author.objects.create(first_name='tony', last_name='kalsi')
        test_genre = Genre.objects.create(name='Social')
        test_language = Language.objects.create(name='Farsi')
        test_book = Book.objects.create(
            title='who is who',
            summary='who sold this book withiout my knowledge',
            isbn = '956793917789',
            author=test_author,
        )

        # Create Genre as a post op
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # create language as post
        language_objects_for_book = Language.objects.all()
        test_book.language.set(language_objects_for_book)
        test_book.save()

        # CREATE NUMBER OF BOOKINSTANCE TO 30
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user_1 if book_copy % 2 else test_user_2
            status = 'm'
            BookInstance.objects.create(
                book = test_book,
                imprint = '2',
                due_back = return_date,
                borrower = the_borrower,
                status = status
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_correct_template(self):
        login = self.client.login(username='tara1', password='tara3676')
        response = self.client.get(reverse('my-borrowed'))

        # check user is logged in
        self.assertEqual(str(response.context['user']), 'tara1')
        # check response is success 200
        self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')

    def test_borrowed_books_only(self):
        login = self.client.login(username='tara2', password='sitara2356')
        response = self.client.get(reverse('my-borrowed'))

        #Check our user is logged in
        self.assertEqual(str(response.context['user']), 'tara2')
        #check we got status 200
        self.assertEqual(response.status_code, 200)
        #CHECK INTIALLY WE DONT HAVE BOOKS IN THE LIST
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)
        # Now change all books to be on loan
        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('my-borrowed'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'tara2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)

        # Confirm all books belong to testuser1 and are on loan
        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual(bookitem.status, 'o')

    def test_pages_ordered_by_due_date(self):
        # Change all books to be on loan
        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        login = self.client.login(username='tara2',
                                  password='sitara2356')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'tara2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back


import uuid

from django.contrib.auth.models import Permission  # Required to grant the permission needed to set a book as returned.

class RenewBookInstanceViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1',
                                              password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2',
                                              password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user2 permission to renew books.
        permission = Permission.objects.get(name = 'Set book as returned')
        test_user2.user_permission.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John',
                                            last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(
            genre_objects_for_book
        )  # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create Language as post-setup
        language_objects_for_book = Language.objects.all()
        test_book.language.set(
            language_objects_for_book
        ) # Direct assignments of many-to-many types not allowed
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user1,
            status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user2,
            status='o',
        )
        
        def test_redirect_if_not_logged_in(self):
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
            # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/accounts/login/'))

        def test_forbidden_if_logged_in_but_not_correct_permission(self):
            login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
            self.assertEqual(response.status_code, 403)

        def test_logged_in_with_permission_borrowed_book(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))

            # Check that it lets us login - this is our book and we have the right permissions.
            self.assertEqual(response.status_code, 200)

        def test_logged_in_with_permission_another_users_borrowed_book(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))

            # Check that it lets us login. We're a librarian, so we can view any users book
            self.assertEqual(response.status_code, 200)

        def test_HTTP404_for_invalid_book_if_logged_in(self):
            # unlikely UID to match our bookinstance!
            test_uid = uuid.uuid4()
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':test_uid}))
            self.assertEqual(response.status_code, 404)

        def test_uses_correct_template(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
            self.assertEqual(response.status_code, 200)

            # Check we used correct template
            self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')
            
        def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
            self.assertEqual(response.status_code, 200)

            date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
            self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)
            
        def test_redirects_to_all_borrowed_book_list_on_success(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
            response = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})
            self.assertRedirects(response, reverse('all-borrowed'))
        
        def test_form_invalid_renewal_date_past(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
            response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': date_in_past})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')

        def test_form_invalid_renewal_date_future(self):
            login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
            invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
            response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': invalid_date_in_future})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')