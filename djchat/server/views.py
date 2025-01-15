from django.shortcuts import render
from.serializer import ServerSerializer,ChannelSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Server
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count

class ServerListViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def list(self, request):
        category = request.query_params.get('category')
        quantity = request.query_params.get('quantity')
        by_user = request.query_params.get('by_user') == 'true'
        by_serverId = request.query_params.get('by_serverId')
        with_num_members = request.query_params.get('with_num_members') == 'true'
        print(with_num_members)
        if by_user or by_serverId and not request.user.is_authenticated:
            raise AuthenticationFailed
        if category:
            self.queryset = self.queryset.filter(category=category)
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member = user_id)
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))
            print(self.queryset)
        if quantity:
            self.queryset = self.queryset[: int(quantity)]
        if by_serverId:
            self.queryset = self.queryset.filter(id=by_serverId)
        
        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)