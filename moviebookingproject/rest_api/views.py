from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import json
from .serializer import *
from .models import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated


class SignupView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        userExists = User.objects.filter(
            Q(email=data["email"]) | Q(username=data["username"])
        )

        if not userExists:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    {"message": "Account created successfully"},
                    safe=False,
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"message": "User already registered!!"}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data

            refresh_token = RefreshToken.for_user(user)

            return JsonResponse(
                {
                    "refresh_token": str(refresh_token),
                    "access_token": str(refresh_token.access_token),
                },
                safe=False,
                status=status.HTTP_200_OK,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def put(self, request):
        data = json.loads(request.body)
        username = request.GET.get("username")

        try:
            user = User.objects.get(
                Q(username__iexact=username) & Q(phone__exact=data["phone"])
            )

            if user:
                user.set_password(data["password"])
                user.save()
                return JsonResponse(
                    {"message": "Password successfully updated"},
                    status=status.HTTP_200_OK,
                    safe=False,
                )
            return JsonResponse(
                {"message": "No user found!!"},
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )
        except:
            return JsonResponse(
                {"message": "No user found!!"},
                status=status.HTTP_400_BAD_REQUEST,
                safe=False,
            )


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return JsonResponse({"message": "Refresh token is required!!"}, safe=False)
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = refresh_token.access_token
        except Exception as e:
            return JsonResponse({"message": "Invalid Refresh Token!!"}, safe=False)
        return JsonResponse(
            {"access_token": str(access_token)}, status=status.HTTP_200_OK, safe=False
        )


class AllMoviesViews(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        paginator = Paginator(movies, 8)

        page_number = request.GET.get("page")

        page_obj = paginator.get_page(page_number)

        movie_pages = page_obj.object_list

        serialized = MovieSerializer(movie_pages, many=True).data

        return JsonResponse(
            {
                "movies": serialized,
                "total_pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
            },
            safe=False,
            status=status.HTTP_200_OK,
        )


class MovieBySearchView(APIView):
    def get(self, request):
        movieName = request.GET.get("search")

        movies = Movie.objects.filter(title__icontains=movieName)

  

        serialized = MovieSerializer(movies, many=True).data

        return JsonResponse(
            {
                "movies": serialized,
            },
            safe=False,
            status=status.HTTP_200_OK,
        )


class MoviesByLanguageView(APIView):
    def get(self, request):
        lang = request.GET.get("language")
        page = request.GET.get("page")
        allMovies=Movie.objects.all()
        movies = Movie.objects.filter(language__icontains=lang)
        
        if movies:
            paginator = Paginator(movies, 8)
            page_obj = paginator.get_page(page)
            movie_pages = page_obj.object_list

            serialized = MovieSerializer(movie_pages, many=True).data

            return JsonResponse(
                {
                    "movies": serialized,
                    "total_pages": paginator.num_pages,
                    "has_next": page_obj.has_next(),
                },
                safe=False,
            )
        else:
            paginator = Paginator(allMovies, 8)
            page_obj = paginator.get_page(page)
            movie_pages = page_obj.object_list

            serialized = MovieSerializer(movie_pages, many=True).data

            return JsonResponse(
                {
                    "movies": serialized,
                    "total_pages": paginator.num_pages,
                    "has_next": page_obj.has_next(),
                },
                safe=False,
            )



class MoviesBygenreView(APIView):
    def get(self, request):
        genre = request.GET.get("genre")
        page = request.GET.get("page")
        movies = Movie.objects.filter(genre__icontains=genre)

        allMovies=Movie.objects.all()



        if movies:
            paginator = Paginator(movies, 8)
            page_obj = paginator.get_page(page)
            movie_pages = page_obj.object_list

            serialized = MovieSerializer(movie_pages, many=True).data

            return JsonResponse(
                {
                    "movies": serialized,
                    "total_pages": paginator.num_pages,
                    "has_next": page_obj.has_next(),
                },
                safe=False,
            )
        else:
            paginator = Paginator(allMovies, 8)
            page_obj = paginator.get_page(page)
            movie_pages = page_obj.object_list

            serialized = MovieSerializer(movie_pages, many=True).data

            return JsonResponse(
                {
                    "movies": serialized,
                    "total_pages": paginator.num_pages,
                    "has_next": page_obj.has_next(),
                },
                safe=False,
            )

        


class AllTheatersView(APIView):
    def get(self, request):
        theater = Theater.objects.all()
        serialized = TheaterSerializer(theater, many=True).data
        return JsonResponse(serialized, safe=False, status=status.HTTP_200_OK)
    

class MoviebyidView(APIView):
    def get(self,request):
        mid=request.GET.get('movie')
    
        movie=Movie.objects.filter(movie_id=mid)
        serialized=MovieSerializer(movie,many=True).data
        return JsonResponse({'movies':serialized},safe=False)    


class TheaterbyidView(APIView):
    def get(self,request):
        tid=request.GET.get('theater')
    
        theater=Theater.objects.filter(theater_id=tid)
        serialized=TheaterSerializer(theater,many=True).data
        return JsonResponse({'theaters':serialized},safe=False)
    
      




class TheaterForMovieView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        mv = request.GET.get("movie")
        page = request.GET.get("page")
        theater = Theater.objects.filter(movie_id=mv)
        paginator = Paginator(theater, 6)
        page_obj = paginator.get_page(page)
        theater_pages = page_obj.object_list

        serialized = TheaterSerializer(theater_pages, many=True).data

        return JsonResponse(
            {
                "theaters": serialized,
                "total_pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
            },
            safe=False,
            status=status.HTTP_200_OK,
        )


class SingleMovie(APIView):
    def get(self, request):
        movieid = request.GET.get("id", "")

        movie = Movie.objects.filter(movie_id=movieid)
        serialized = MovieSerializer(movie, many=True).data

        return JsonResponse(
            {"movies": serialized}, safe=False, status=status.HTTP_200_OK
        )


class GetTheaterSeatsView(APIView):
    def get(self, request):
        movie = request.GET.get("movie")
        theater = request.GET.get("theater")

        seats = Seat.objects.filter(Q(movie=movie) & Q(theater=theater))
        serialized = SeatsSerializer(seats, many=True).data
        return JsonResponse(serialized, safe=False, status=status.HTTP_200_OK)


class SeatSelectView(APIView):
    def post(self, request):
        user = request.user.id
        movie = request.GET.get("movie")
        theater = request.GET.get("theater")
        seatn = request.GET.get("seat")
        price = request.GET.get("price")
     
        seat = Seat.objects.filter(
            Q(number=seatn) & Q(movie=movie) & Q(theater=theater)
        )
        if seat:
            seat.delete()
            return JsonResponse(
                {"message": "Seat Unselected!!"}, safe=False, status=status.HTTP_200_OK
            )

        data = {
            "number": seatn,
            "movie": movie,
            "theater": theater,
            "available": False,
            "price": price,
        }

        serialized = SeatsSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            return JsonResponse(
                serialized.data, safe=False, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            serialized.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
        )




class BookingView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        data['user'] = request.user.id

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserBookingView(APIView):
    def get(self, request):
        user = request.user.id
        theater=request.GET.get("theater")
        movie=request.GET.get("movie")

        bookings = Booking.objects.filter(Q(user_id=user) & Q(movie=movie) & Q(theater=theater))

        serialized = BookingSerializer(bookings, many=True).data

        return JsonResponse(serialized, safe=False)
    

class UserAllBookingView(APIView):
    def get(self,request):
        user=request.user.id

        bookings=Booking.objects.filter(user_id=user)

        serialized=BookingSerializer(bookings,many=True).data

        return JsonResponse(serialized,safe=False)