from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = "__all__"

# class BookingSerializer(serializers.ModelSerializer):
#     seats = serializers.ListField(write_only=True)  # Assuming you're sending seat IDs in the request

#     class Meta:
#         model = Booking
#         fields = '__all__'

#     def create(self, validated_data):
#         seats_data = validated_data.pop('seats', [])
#         booking = Booking.objects.create(**validated_data)

#         # Process seats and associate them with the booking
#         seats = Seat.objects.filter(number__in=seats_data)
#         booking.seats.set(seats)

#         return booking
#     def get_seat_numbers(self, obj):
#         return [seat.number for seat in obj.seats.all()]

# class BookingSerializer(serializers.ModelSerializer):
#     seats = serializers.ListField(write_only=True)
#     seat_numbers = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Booking
#         fields = '__all__'

#     def create(self, validated_data):
#         seats_data = validated_data.pop('seats', [])
#         booking = Booking.objects.create(**validated_data)

#         seats = Seat.objects.filter(number__in=seats_data)
#         booking.seats.set(seats)

#         return booking

#     def get_seat_numbers(self, obj):
#         return [seat.number for seat in obj.seats.all()]

class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.ListField(write_only=True)
    seat_numbers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        seats_data = validated_data.pop('seats', [])
        booking = Booking.objects.create(**validated_data)

        seats = Seat.objects.filter(number__in=seats_data)
        booking.seats.set(seats)

        return booking

    def get_seat_numbers(self, obj):
        seat_numbers = [seat.number for seat in obj.seats.all()]
        unique_seat_numbers = list(set(seat_numbers))  # Remove duplicates
        return unique_seat_numbers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            name=validated_data["name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid username or password !!")






class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class TheaterSerializer(serializers.ModelSerializer):
    stheater = SeatsSerializer(many=True)
    class Meta:
        model = Theater
        fields = "__all__"




class MovieSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(many=True)
    class Meta:
        model = Movie
        fields = "__all__"