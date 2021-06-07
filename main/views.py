from django.http import JsonResponse
from django.shortcuts import render

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from main.models import Category, Post
# from main.serializers import CategorySerializer, PostSerializer
#
#
# @api_view(['GET'])
# def categories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)
#
#
# class PostListView(APIView):
#     def get(self,request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         post = request.data
#         serializer = PostSerializer(data=post)
#         if serializer.is_valid(raise_exception=True):
#             post_saved = serializer.save()
#             return Response(serializer.data)
from django.views import View
from rest_framework import generics, permissions

from main import serializers
from main.models import Category, Post, PostImages
from main.serializers import CategorySerializer, PostSerializer, PostImageSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostImageView(generics.ListAPIView):
    queryset = PostImages.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class UserReactionView(View):
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        post_id = self.request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        like = self.request.GET.get('like')
        dislike = self.request.GET.get('dislike')
        post_user_reactions = Post.objects.filter(user=request.user)
        if like and (request.user not in post_user_reactions.all()):
            post.likes += 1
            post.users_reaction.add(request.user)
            post.save()
        if dislike and (request.user not in post_user_reactions.all()):
            post.dislikes += 1
            post.users_reaction.add(request.user)
            post.save()
        data = {
            'likes': post.likes,
            'dislikes': post.dislikes
        }

        return JsonResponse(data)
