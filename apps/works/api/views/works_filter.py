from datetime import date, timedelta

from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

# apps
from apps.properties.api.serializers.works import PropertiesWorkSerializer
from apps.works.api.serializers.serializers import WorksPropertySerializer


class WorksPropertyViewSet(GenericViewSet):

    serializer_class = PropertiesWorkSerializer
    serializer_class_work = WorksPropertySerializer

    def get_queryset(self):
        return self.serializer_class_work.Meta.model.objects.filter(
            modified_date__lte=date.today() - timedelta(days=5)
        ).all()

    def get_queryset_property(self, pk_client=None, pk_province=None):
        if pk_client and pk_province:
            return self.get_serializer().Meta.model.objects.filter(client=pk_client, province=pk_province).exclude(works=None)
        if pk_client:
            return self.get_serializer().Meta.model.objects.filter(client=pk_client).exclude(works=None)
        return self.get_serializer().Meta.model.objects.filter(province=pk_province).exclude(works=None)

    def get_queryset_work_date(self, date_gte=None, date_lte=None):
        if date_gte and date_lte is None:
            return self.serializer_class_work.Meta.model.objects.filter(
                created_date__gte=date(date_gte[0], date_gte[1], date_gte[2])
            ).all()
        if date_lte and date_gte is None:
            return self.serializer_class_work.Meta.model.objects.filter(
                modified_date__lte=date(date_lte[0], date_lte[1], date_lte[2])
            ).all()
        return self.serializer_class_work.Meta.model.objects.filter(
            Q(created_date__gte=date(date_gte[0], date_gte[1], date_gte[2])) &
            Q(modified_date__lte=date(date_lte[0], date_lte[1], date_lte[2]))
        ).all()

    def list(self, request):
        try:
            client = request.GET.get('client')
            province = request.GET.get('province')
            date_gte = self.parseToTuple(request.GET.get('date_gte'))
            date_lte = self.parseToTuple(request.GET.get('date_lte'))
            works_assign = []

            if date_gte or date_lte:
                queryset_work_date = self.get_queryset_work_date(
                    date_gte, date_lte)
                if queryset_work_date:
                    serializer_work_date = self.serializer_class_work(
                        queryset_work_date, many=True)
                    return Response({'items': serializer_work_date.data, 'message': 'Se encontraron trabajos por fecha.'}, status=status.HTTP_200_OK)
                return Response({'messge': 'No se encontraron trabajos por fecha.'}, status=status.HTTP_404_NOT_FOUND)
            if client or province:
                queryset = self.get_queryset_property(client, province)
                if queryset:
                    properties_serializer = self.get_serializer(
                        queryset, many=True)
                    for works in properties_serializer.data:
                        for work in works['works']:
                            work_assign = work
                            works_assign.append(work_assign)
                    return Response({'items': works_assign, 'message': 'Se encontraron trabajos relacionados.'}, status=status.HTTP_200_OK)
                return Response({'message': 'No se encontraron trabajos relacionados.'}, status=status.HTTP_404_NOT_FOUND)
            queryset = self.get_queryset()
            if queryset:
                serializer = self.serializer_class_work(queryset, many=True)
                return Response({'items': serializer.data, 'message': 'Se encontraron trabajos mayores a 5 días.'}, status=status.HTTP_200_OK)
            return Response({'message': 'No se encontraron trabajos mayores a 5 días.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def parseToTuple(self, date):
        try:
            return tuple(map(int, date.split('-')))
        except:
            return None
