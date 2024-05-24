from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from cinema.models import Movie, Actor, CinemaHall, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ("id", "name", "rows", "seats_in_row")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "actors", "genres", "duration"]

    def create(self, validated_data):
        movie = Movie.objects.create(**validated_data)
        if actors := self.initial_data.get("actors"):
            self.add_to_actor_model(actors, movie)

        if genres := self.initial_data.get("genres"):
            self.add_to_genre_model(genres, movie)

        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.duration = validated_data.get("duration", instance.duration)

        if actors := self.initial_data.get("actors"):
            self.add_to_actor_model(actors, instance)

        if genres := self.initial_data.get("genres"):
            self.add_to_genre_model(genres, instance)

        instance.save()
        return instance

    @staticmethod
    def add_to_actor_model(actors: list[dict], instance: Movie):
        for actor_data in actors:
            actor = get_object_or_404(Actor, **actor_data)
            instance.actors.add(actor)

    @staticmethod
    def add_to_genre_model(genres: list[dict], instance: Movie):
        for genre_data in genres:
            genre = get_object_or_404(Genre, **genre_data)
            instance.genres.add(genre)
