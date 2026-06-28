from src.pyamf.remoting import WSGIGateway

def echo(data):
   return data

services = {
   'echo': echo,
   # Add other exposed functions here
}

gateway = WSGIGateway(services)
