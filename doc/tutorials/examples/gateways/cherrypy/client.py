import logging

from src.pyamf.remoting import RemotingService


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)


path = 'http://localhost:8080/gateway/'
gw = RemotingService(path, logger=logging)
service = gw.getService('myservice')

print service.echo('Hello World!')
