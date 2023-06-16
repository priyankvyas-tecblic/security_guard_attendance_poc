from rest_framework import serializers
from .models import User,AttendanceHistory,SecurityAttendance
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AttendanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceHistory
        fields = "__all__"

    def validate(self, attrs):
        point = Feature(geometry=Point((float(attrs.get('latitude')), float(attrs.get('longitude')))))
        polygon = Polygon(
            [
                [
                    (23.028409867393275, 72.52950620826724),
                    (23.028647429855575, 72.5296390363293),
                    (23.028882523441418, 72.5297557711373),
                    (23.02902722773806, 72.52947713566499),
                    (23.029169463426847, 72.52918508914762),
                    (23.029014295572367, 72.52908346277621),
                    (23.02888742302458, 72.52926562013035),
                    (23.028811153778545, 72.52929757377963),
                    (23.028707984385942, 72.52928637922578),
                    (23.02861766315832, 72.52924789686396)
                ]
            ]
        )
        guard_is_inside = boolean_point_in_polygon(point, polygon)
        if guard_is_inside == False:
            raise serializers.ValidationError("The guard is outside the premises.")
        return attrs


class SecurityAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityAttendance
        fields = "__all__"

    def validate(self, attrs):
        print(self.context,"context")
        print(attrs,"attrs")
        point = Feature(geometry=Point((float(self.context['latitude']), float(self.context['longitude']))))
        polygon = Polygon(
            [
                [
                    (23.028409867393275, 72.52950620826724),
                    (23.028647429855575, 72.5296390363293),
                    (23.028882523441418, 72.5297557711373),
                    (23.02902722773806, 72.52947713566499),
                    (23.029169463426847, 72.52918508914762),
                    (23.029014295572367, 72.52908346277621),
                    (23.02888742302458, 72.52926562013035),
                    (23.028811153778545, 72.52929757377963),
                    (23.028707984385942, 72.52928637922578),
                    (23.02861766315832, 72.52924789686396)
                ]
            ]
        )
        guard_is_inside = boolean_point_in_polygon(point, polygon)
        if guard_is_inside == False:
            raise serializers.ValidationError("The guard is outside the premises.")
        return attrs


class SecurityAttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityAttendance
        fields = "__all__"
