from django.shortcuts import render
from django.contrib import messages
from io import BytesIO
import base64
import rpy2.robjects as ro
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import subprocess

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers




class FileUploadSerializer(serializers.Serializer):
    host_file = serializers.FileField()
    parasite_file = serializers.FileField()
    hpmatrix_file = serializers.FileField()

@api_view(['POST'])
def tanglegram(request):
    serializer = FileUploadSerializer(data=request.data)
    if serializer.is_valid():
        host_file = serializer.validated_data['host_file']
        parasite_file = serializer.validated_data['parasite_file']
        hpmatrix_file = serializer.validated_data['hpmatrix_file']

        try:
            if default_storage.exists('host.nwk'):
                default_storage.delete('host.nwk')
            if default_storage.exists('parasite.nwk'):
                default_storage.delete('parasite.nwk')
            if default_storage.exists('hpmatrix.txt'):
                default_storage.delete('hpmatrix.txt')
            if default_storage.exists('Tanglegram.png'):
                default_storage.delete('Tanglegram.png')

            host_file_path = default_storage.save('host.nwk', ContentFile(host_file.read()))
            parasite_file_path = default_storage.save('parasite.nwk', ContentFile(parasite_file.read()))
            hpmatrix_file_path = default_storage.save('hpmatrix.txt', ContentFile(hpmatrix_file.read()))
            subprocess.run(['Rscript', 'Tanglegram.r'])

            with open('Tanglegram.png', 'rb') as f:
                Tanglegram_data = f.read()

            Tanglegram_png = base64.b64encode(Tanglegram_data)
            context = {'Tanglegram_png': Tanglegram_png}
            
            default_storage.delete(host_file_path)
            default_storage.delete(parasite_file_path)
            default_storage.delete(hpmatrix_file_path)
            default_storage.delete('Tanglegram.png')

            return Response(context, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    else:
        return Response(serializer.errors, status=400)


class FileUploadSerializer1(serializers.Serializer):
    host_file = serializers.FileField()

@api_view(['POST'])
def tree(request):
    serializer = FileUploadSerializer1(data=request.data)
    if serializer.is_valid():
        host_file = serializer.validated_data['host_file']
        print(host_file)

        try:
            if default_storage.exists('Tree.png'):
                default_storage.delete('Tree.png')

            if default_storage.exists('host.nwk'):
                default_storage.delete('host.nwk')

            host_file_content = host_file.read().decode('utf-8')
            host_file_path = default_storage.save('host.nwk', ContentFile(host_file_content))

            if request.data['selected_status'] == "fan":
                subprocess.run(['Rscript', 'Fan_Tree.r'])
            elif request.data['selected_status'] == "radial":
                subprocess.run(['Rscript', 'Radial_Tree.r'])
            else:
                subprocess.run(['Rscript', 'Default_Tree.r'])

            with open('Tree.png', 'rb') as f:
                Tree_data = f.read()

            Tree_png = base64.b64encode(Tree_data).decode('utf-8')
            context = {'Tree_png': Tree_png}
            default_storage.delete('Tree.png')
            default_storage.delete(host_file_path)

            return Response(context, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    else:
        return Response(serializer.errors, status=400)