
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.projects.api.serializers.projects import ProjectSerializer, ProjectsSerializer

from apps.projects.models import Project

class ProjectViewSet(GenericViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return Project.objects.filter(state=True).all()
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data, 'message': 'Proyecto creado'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = ProjectsSerializer(queryset, many=True)
            if serializer:
                return Response({'items': serializer.data, 'message': 'Todos los proyectos'}, status=status.HTTP_200_OK)
            return Response({ 'error': 'Error en el serializer'}, status=status.HTTP_409_CONFLICT)
        return Response({'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            queryset = self.get_queryset(pk)
            if queryset:
                serializer = self.get_serializer(queryset)
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error:' 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as error:
            return Response({
                'error': str(error),
                'message': 'Error interno del servidor. Inténtelo de nuevo más tarde.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Proyecto eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'El proyecto ya fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)

