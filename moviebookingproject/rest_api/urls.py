from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    path('users/signup/',csrf_exempt(SignupView.as_view()),name='signup'),
    path('users/login/',csrf_exempt(LoginView.as_view()),name='login'),
    path('users/resetpassword/',csrf_exempt(ResetPasswordView.as_view()),name='signup'),
    path('refresh/',csrf_exempt(RefreshTokenView.as_view()),name='signup'),
    path('movies/',csrf_exempt(AllMoviesViews.as_view()),name='all-movies'),
    path('movies/single/',csrf_exempt(SingleMovie.as_view()),name='single-Movie'),
    path('theaters/',csrf_exempt(AllTheatersView.as_view()),name='all-theaters'),
    path('movies/language/',csrf_exempt(MoviesByLanguageView.as_view()),name='movie-by-language'),
    path('movies/genre/',csrf_exempt(MoviesBygenreView.as_view()),name='movie-by-genre'),
    path('movies/theaters/',csrf_exempt(TheaterForMovieView.as_view()),name='movies-theater'),
    path('movies/theaters/seats/',csrf_exempt((GetTheaterSeatsView.as_view())),name='available-seats'),
    path('movies/theater/seats/select/',csrf_exempt(SeatSelectView.as_view()),name='seat-select'),
    path('movies/booking/',csrf_exempt(BookingView.as_view()),name='booking'),
    path('user/booking/',csrf_exempt(UserBookingView.as_view()),name='user-booking'),
    path('movies/search/',csrf_exempt(MovieBySearchView.as_view()),name='movie-search'),
    path('theater/',csrf_exempt(TheaterbyidView.as_view()),name='theater'),
    path('booking/movie/',csrf_exempt(MoviebyidView.as_view()),name='movie'),
    path('user/bookings/',csrf_exempt(UserAllBookingView.as_view()),name='user-all-booking')


]