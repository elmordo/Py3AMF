from src.pyamf.remoting import RemotingService

client = RemotingService('http://demo.pyamf.org/gateway/recordset')
service = client.getService('service')

print service.getLanguages()
