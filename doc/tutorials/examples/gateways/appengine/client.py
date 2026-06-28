import logging

from src.pyamf.remoting import RemotingService


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)


path = 'http://localhost:8080/'
gw = RemotingService(path, logger=logging, debug=True)
service = gw.getService('myservice')

print service.echo('Hello World!')
