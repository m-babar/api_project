import uuid

from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Playlist, Assest, Schedule


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    It's user registration model serializer.
    """
    user_password = serializers.CharField(source='password', style={'input_type': 'password'},
        max_length=20, min_length=8)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'user_password')
        

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        token = Token.objects.create(user=user)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    It's authentication serializer. it's valid method check if not valid user raise exception or if authenticate
    return user.
    """
    username = serializers.CharField(label=("username"))
    password = serializers.CharField(label=("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user_obj = User.objects.filter(username=username)
            if user_obj:    
                user = authenticate(username=user_obj[0].username, password=password)

                if user:
                    if not user.is_active:
                        msg = ({'user': 'User account is disabled.'})
                        raise serializers.ValidationError(msg, code='authorization') 
                else:
                    msg = ({'logging' : 'Unable to log in with provided credentials.'})
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = ({'username' : 'username address is not correct or user is not valid user type.'})
                raise serializers.ValidationError(msg, code='authorization')
        else:
            if not username and not password:
                msg = ({
                    'username': 'Must include "email"', 
                    'password': 'Must include "password".'
                })

            if not username:
                msg = ({
                    'username': 'Must include "username"', 
                })

            if not password:
                msg = ({
                    'password': 'Must include "password".'
                })

            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserLogoutSerializer(serializers.Serializer):
    """
    It's user logout serializer. it's logout on token bases.
    """
    token = serializers.CharField(label=("Token"))

    def validate(self, attrs):
        token = attrs.get('token')
        
        if token:
            token = Token.objects.filter(key=token)
            if not token:
                msg = ({'token' : 'Invalid token.'})
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ({'token' : 'Must include "token".'})
            raise serializers.ValidationError(msg, code='authorization')

        attrs['token'] = token
        return attrs


class AssetSerializer(serializers.ModelSerializer):
    """
    It's assest model serilizer to insert assests records into assest model.
    """
    Uid = serializers.CharField(source='Assest.Uid', allow_blank=True)

    class Meta:
        model = Assest  
        fields= ('Title','Uid', 'Uri', 'Type')


class PlayListSerializer(serializers.ModelSerializer):
    """
    It's playlist model serilizer to insert playlist records into playlist model.
    """
    assests = AssetSerializer(many=True)
    Uid = serializers.CharField(source='Playlist.Uid', allow_blank=True)

    class Meta:
        model = Playlist
        fields = ('Title', 'Uid', 'assests')


    def create(self, validated_data):
        # insert records into playlist model along with assests model.
        assests = validated_data.pop('assests')
        created_by = self.context['user']
        uid = validated_data.pop('Playlist')['Uid']
        
        
        uid = uuid.UUID(uid).hex if uid else uuid.uuid4()

        playlist = Playlist.objects.create(created_by=created_by, Uid=uid ,**validated_data)
        
        for assest in assests:
            ass_uid = assest.pop('Assest')['Uid']
            ass_uid = uuid.UUID(ass_uid).hex if ass_uid else uuid.uuid4()
            Assest.objects.create(**assest, created_by=created_by, Uid=ass_uid,  playlist=playlist)
        return playlist


    def validate(self, attrs):
        uid = attrs.get('Playlist')['Uid']
        if uid:
            try:
                uid = uuid.UUID(uid, version=4)
            except ValueError:
                msg = ({'Uid' : 'Uid is not correct format'})
                raise serializers.ValidationError(msg, code='authorization')

            playlist = Playlist.objects.filter(Uid=uid).exists()
            if playlist:
                msg = ({'Uid' : 'Uid is already exists into database , please try another.'})
                raise serializers.ValidationError(msg, code='authorization')

        assest_uid = attrs['assests']
        for assest in  assest_uid:
            ass_uid =  assest['Assest']['Uid']
            if ass_uid:
                try:
                    ass_uid = uuid.UUID(ass_uid, version=4)
                except ValueError:
                    msg = ({'Uid' : 'Uid is not correct format'})
                    raise serializers.ValidationError(msg, code='authorization')

                assest = Assest.objects.filter(Uid=ass_uid).exists()
                if assest:
                    msg = ({'Uid' : 'Uid is already exists into database , please try another.'})
                    raise serializers.ValidationError(msg, code='authorization')
                
                return attrs

        return attrs


class CommonPlaylistSerializer(serializers.ModelSerializer):
    NumberAssets = serializers.IntegerField(source='playlist_assests_count')


class PlaylistResSerializer(CommonPlaylistSerializer):
    """
    It's return playlist results.
    """
    class Meta:
        model = Playlist
        fields = ('Title', 'Uid', 'Status', 'CreatedOn', 
                    'CompletedOn', 'Uri', 'NumberAssets')


class PlaylistRetriveSerializer(CommonPlaylistSerializer):
    """
    It's return data of the json format with specific playlist records.
    """

    class Meta:
        model = Playlist
        fields = ('Title', 'Uid', 'Status', 'CreatedOn', 
                'ProcessedOn', 'ScheduledOn', 'Duration',
                'NumberAssets', 'Uri',  )


class ScheduleSerializer(serializers.ModelSerializer):
    """
    It's store information into schedule model.
    """

    Uid = serializers.UUIDField(source="playlist.Uid")

    class Meta:
        model = Schedule
        fields = ('Title', 'Uid', 'StartAt', 'isLoop')

    def create(self, validated_data):
        created_by = self.context['user']
        playlist_uid = validated_data.pop('playlist')['Uid']

        try:
            playlist = Playlist.objects.get(Uid=playlist_uid)
        except Exception as e:
            msg = ({'Uid' : 'Playlist Uid is not matching into database.'})
            raise serializers.ValidationError(msg, code='authorization')
        

        schedule = Schedule.objects.create(created_by=created_by, playlist=playlist, **validated_data)
        return schedule


class ScheduleResSerializer(serializers.ModelSerializer):
    """
    It's return the json response to endpoint /api/v1/APXSchedule/.
    """

    Status = serializers.CharField(source='playlist.Status')
    CreatedOn = serializers.DateTimeField(source='playlist.CreatedOn')
    ProcessedOn = serializers.DateTimeField(source='playlist.ProcessedOn')
    ScheduleOn = serializers.DateTimeField(source='playlist.ScheduledOn')
    Duration = serializers.DateTimeField(source="playlist.Duration")
    Uri = serializers.URLField(source="playlist.Uri")
    NumberAssets = serializers.IntegerField(source='playlist.playlist_assests_count')

    class Meta:
        model = Schedule
        fields = ('Title', 'Uid', 'Status', 'CreatedOn', 'ProcessedOn',
            'ScheduleOn', 'Duration', 'Uri', 'NumberAssets')

