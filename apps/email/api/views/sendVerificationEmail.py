from django.core.mail import EmailMessage

from rest_framework.response import Response
from rest_framework import status

from smtplib import SMTPAuthenticationError


class SendVerificationEmail:

    def sendEmial(data):
        try:
            subject = data['subject']
            message = data['message']
            # from_email = request.POST.get('de')
            recipient_list = data['recipient_list']
            # files = request.POST.get('files')
            email = EmailMessage(
                subject=subject,
                body=message,
                to=recipient_list
            )
            # email.attach_file(str(self.get_queryset(files).file))  # Ruta completa al archivo PDF
            # # email.attach_file('ruta/al/archivo.xml')  # Ruta completa al archivo XML
            email.send()

            return Response({'message': 'Correo enviado.'}, status=status.HTTP_200_OK)
        except ConnectionRefusedError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except UnicodeEncodeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except SMTPAuthenticationError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)