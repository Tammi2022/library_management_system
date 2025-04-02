from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.book_record.views import BookRecordApiview
from apps.books.views import BookApiview
from apps.users.views import UserApiview

urlpatterns = [
    path('books/', csrf_exempt(BookApiview.as_view())),
    path('book_record/', csrf_exempt(BookRecordApiview.as_view())),
    path('users/', csrf_exempt(UserApiview.as_view())),
]
