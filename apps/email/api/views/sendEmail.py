from django.core.mail import EmailMessage

from rest_framework import viewsets,status
from rest_framework.response import Response
from smtplib import SMTPAuthenticationError

from apps.resources.api.serializers.receipt import ProofPaymentSerializer

class SendEmail(viewsets.GenericViewSet):

    serializer_class = ProofPaymentSerializer

    def get_queryset(self, pk=None, resource_pk=None):
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def create(self, request):
        try:
            subject = request.POST.get('asunto')
            message = request.POST.get('mensaje')
            from_email = request.POST.get('de')
            recipient_list = [request.POST.get('para')]
            files = request.POST.get('files')
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach_file(str(self.get_queryset(files).file))  # Ruta completa al archivo PDF
            # email.attach_file('ruta/al/archivo.xml')  # Ruta completa al archivo XML
            email.send()

            return Response({'message': 'Correo enviado.'}, status=status.HTTP_200_OK)
            # if is_send_email:
            # else:
            #     return Response({'message': 'Correo no enviado.'}, status=status.HTTP_200_OK)
        except ConnectionRefusedError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except UnicodeEncodeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except SMTPAuthenticationError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)