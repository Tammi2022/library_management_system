from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.book_record.views import BookRecordApiview, BookBorrowView, BookReturnView, BookRecordDetailsApiview
from apps.books.views import BookApiview, BookDestructionApiview, BookEditApiview
from apps.users.views import UserApiview, UserEditApiview

urlpatterns = [
    path('books/', csrf_exempt(BookApiview.as_view())),
    path('books/<int:book_id>', csrf_exempt(BookEditApiview.as_view())),
    path('books/destruction/<int:book_id>', csrf_exempt(BookDestructionApiview.as_view())),
    path('book_record/', csrf_exempt(BookRecordApiview.as_view())),
    path('book_record/<int:record_id>', csrf_exempt(BookRecordDetailsApiview.as_view())),
    path('book_record/borrow', csrf_exempt(BookBorrowView.as_view())),
    path('book_record/return/<int:record_id>', csrf_exempt(BookReturnView.as_view())),
    path('users/', csrf_exempt(UserApiview.as_view())),
    path('users/<int:user_id>', csrf_exempt(UserEditApiview.as_view())),
]
