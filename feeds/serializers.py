from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from comments.models import * 

class FeedSerializer(serializers.ModelSerializer):
     desc= serializers.CharField(read_only=True, source="feeduser.desc")
     username= serializers.CharField(read_only=True, source="feeduser.profileuser.username")
     firstname= serializers.CharField(read_only=True, source="feeduser.profileuser.first_name")
     lastname= serializers.CharField(read_only=True, source="feeduser.profileuser.last_name")
     desc= serializers.CharField(read_only=True, source="feeduser.desc")
     useravatar= serializers.CharField(read_only=True, source="feeduser.avatar")
 
     def to_representation(self, instance):
            representation = super().to_representation(instance)
            feeduser=representation['feeduser']
            feedpost=representation['id']
            print(feeduser)
            likes=Like.objects.filter(likedpost=feedpost).count()
            representation["likes"]=likes


            comments=Comment.objects.filter(commentPost=feedpost).count()
            representation["comments"]=comments
            return  representation
     class Meta:
        model=Feed
        fields="__all__"
        extra_fields = ['desc',"username",
                        'first_name','last_name'
                        'useravatar','desc',
                        ]
class LikeFeedSerializer(serializers.ModelSerializer):
     def to_internal_value(self, data):
        if "postid" not in data:
             return super().to_internal_value(data)
        post=Feed.objects.filter(id=data["postid"]).first()
        if not post:
             return super().to_internal_value(data)
        user = self.context['request'].user
        instance = Like.objects.get_or_create(
            likedby=user,
            likedpost=post
        )
        return super().to_internal_value(instance)
     class Meta:
          model=Like
          fields="__all__"
class CreateFeedSerializer(serializers.ModelSerializer):
     avatar = serializers.ImageField(required=True)
     feeduser= serializers.ReadOnlyField(source='creator.id')
     def to_internal_value(self, data):
        user = self.context['request'].user
        if "avatar" not in data:
             return super().to_internal_value(data)
        instance=Feed.objects.get_or_create(
             feeduser=user,
             avatar=data["avatar"] if "avatar" in data else None,
             desc=data["desc"] if "desc" in data else "",
             link=data["link"] if "link" in data else "",
             
                )
        return super().to_internal_value(instance)
     class Meta:
          model=Feed
          fields=("avatar","feeduser")

