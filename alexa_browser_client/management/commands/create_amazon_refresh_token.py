from django.conf import settings
from django.core.management import BaseCommand

from avs_client.refreshtoken import handlers, http_server


class Command(BaseCommand):

    help = 'Run http server for retrieving AVS refresh token'

    def add_arguments(self, parser):
        parser.add_argument('--address', dest='address', default='localhost')
        parser.add_argument('--port', dest='port', type=int, default=8000)

    def handle(self, *args, **options):
        server_address = (options['address'], options['port'])
        server = http_server.AmazonLoginHttpServer(
            server_address=server_address,
            RequestHandlerClass=handlers.AmazonAlexaServiceLoginHandler,
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            client_secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
            device_type_id=settings.ALEXA_BROWSER_CLIENT_AVS_DEVICE_TYPE_ID,
        )
        self.stdout.write(
            self.style.SUCCESS(
                'running server on http://{}:{}'.format(*server_address)
            )
        )
        server.serve_forever()
