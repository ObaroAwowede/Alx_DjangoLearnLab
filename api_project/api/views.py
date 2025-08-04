from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    # def list(self, request):
    #     pass
    # def create(self,request):
    #     pass
    # def retrieve(self,request):
    #     pass
    # def update(self, request):
    #     pass
    # def destroy(self, request):
    #     pass
    queryset = Book.objects.all()
    serializer_class = BookSerializer
  
