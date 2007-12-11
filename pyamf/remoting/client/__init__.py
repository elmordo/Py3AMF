# -*- encoding: utf8 -*-
#
# Copyright (c) 2007 The PyAMF Project. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Remoting client implementation.

@author: U{Nick Joyce<mailto:nick@boxdesign.co.uk>}

@since: 0.1.0
"""

import httplib, urlparse

import pyamf
from pyamf import remoting

#: Default AMF client type.
#: @see: L{ClientTypes<pyamf.ClientTypes>}
DEFAULT_CLIENT_TYPE = pyamf.ClientTypes.Flash6

class ServiceMethodProxy(object):
    """
    Serves as a proxy for calling a service method.

    @ivar service: The parent service.
    @type service: L{ServiceProxy}
    @ivar name: The name of the method
    @type name: C{str} or C{None}

    @see: L{ServiceProxy.__getattr__}
    """

    def __init__(self, service, name):
        self.service = service
        self.name = name

    def __call__(self, *args):
        """
        Inform the proxied service that this function has been called.
        """
        return self.service._call(self, args)

    def __str__(self):
        """
        Returns the full service name, including the method name if there is
        one.
        """
        service_name = str(self.service)

        if self.name is not None:
            service_name = '%s.%s' % (service_name, self.name)

        return service_name

class ServiceProxy(object):
    """
    Serves as a service object proxy for RPC calls. Generates
    L{ServiceMethodProxy} objects for method calls.

    @ivar _gw: The parent gateway.
    @type _gw: L{RemotingService}
    @ivar _name: The name of the service.
    @type _name: C{str}
    @ivar _auto_execute: If set to C{True}, when a service method is called,
        the AMF request is immediately sent to the remote gateway and a
        response is returned. If set to C{False}, a L{RequestWrapper} is
        returned, waiting for the underlying gateway to fire the
        L{execute<RemotingService.execute>} method.

    @see: L{RequestWrapper} for more info.
    """

    def __init__(self, gw, name, auto_execute=True):
        self._gw = gw
        self._name = name
        self._auto_execute = auto_execute

    def __getattr__(self, name):
        return ServiceMethodProxy(self, name)

    def _call(self, method_proxy, args):
        """
        Executed when a L{ServiceMethodProxy} is called. Adds a request to
        the underlying gateway. If C{_auto_execute} is set to C{True}, then
        the request is immediately called on the remote gateway.
        """
        request = self._gw.addRequest(method_proxy, args)

        if self._auto_execute:
            response = self._gw.execute_single(request)

            # XXX nick: What to do about Fault objects here?
            return response.body

        return request

    def __call__(self, *args):
        """
        This allows services to be 'called' without a method name.
        """
        return self._call(ServiceMethodProxy(self, None), args)

    def __str__(self):
        """
        Returns a string representation of the name of the service.
        """
        return self._name

class RequestWrapper(object):
    """
    A container object that wraps a service method request.

    @ivar gw: The underlying gateway.
    @type gw: L{RemotingService}
    @ivar id: The id of the request.
    @type id: C{str}
    @ivar service: The service proxy.
    @type service: L{ServiceProxy}
    @ivar args: The args used to invoke the call.
    @type args: C{list}
    """

    def __init__(self, gw, id_, service, args):
        self.gw = gw
        self.id = id_
        self.service = service
        self.args = args

    def __str__(self):
        return str(self.id)

    def setResponse(self, response):
        """
        A response has been received by the gateway
        """
        # XXX nick: What to do about Fault objects here?
        self.response = response
        self.result = self.response.body 

    def _get_result(self):
        """
        Returns the result of the called remote request. If the request has not
        yet been called, an exception is raised.
        """
        if not hasattr(self, '_result'):
            raise AttributeError, "'RequestWrapper' object has no attribute 'result'"

        return self._result

    def _set_result(self, result):
        self._result = result

    result = property(_get_result, _set_result)

class RemotingService(object):
    """
    Acts as a client for AMF calls.

    @ivar url: The url of the remote gateway. Accepts http or https as schemes.
    @type url: C{str}
    @ivar requests: The list of pending requests to process.
    @type requests: C{list}
    @ivar request_number: A unique identifier for an tracking the number of
        requests.
    @ivar amf_version: The AMF version to use.
        See L{ENCODING_TYPES<pyamf.ENCODING_TYPES>}.
    @type amf_version: C{int}
    @ivar client_type: The client type. See L{ClientTypes<pyamf.ClientTypes>}.
    @ivar connection: The underlying connection to the remoting server.
    @type connection: C{httplib.HTTPConnection} or C{httplib.HTTPSConnection}

    @raise ValueError: Unknown scheme.
    """

    def __init__(self, url, amf_version=pyamf.AMF0, client_type=DEFAULT_CLIENT_TYPE):
        self.url = urlparse.urlparse(url)
        self.requests = []
        self.request_number = 1
        self._root_url = urlparse.urlunparse(['', ''] + list(self.url[2:]))

        self.amf_version = amf_version
        self.client_type = client_type
        
        port = None
        hostname = None

        if hasattr(self.url, 'port'):
            if self.url.port is not None:
                port = self.url.port
        else:
            if ':' not in self.url[1]:
                port = None
            else:
                hostname, port = self.url[1].rsplit(':', 1)
                port = int(port)

        if hostname is None:
            if hasattr(self.url, 'hostname'):
                hostname = self.url.hostname

        if self.url[0] == 'http':
            if port is None:
                port = 80

            self.connection = httplib.HTTPConnection(hostname, port)
        elif self.url[0] == 'https':
            if port is None:
                port = 443

            self.connection = httplib.HTTPSConnection(hostname, port)
        else:
            raise ValueError, 'Unknown scheme'

    def getService(self, name, auto_execute=True):
        """
        Returns a L{ServiceProxy} for the supplied name. Sets up an object that
        can have method calls made to it that build the AMF requests.

        @raise TypeError: string type required for C{name}.
        """
        if not isinstance(name, basestring):
            raise TypeError, 'string type required'

        return ServiceProxy(self, name, auto_execute)

    def getRequest(self, id_):
        """
        Gets a request based on the id.
        """
        for request in self.requests:
            if request.id == id_:
                return request

        raise LookupError, "request %s not found" % id_

    def addRequest(self, service, *args):
        """
        Adds a request to be sent to the remoting gateway.
        """
        wrapper = RequestWrapper(self, '/%d' % self.request_number,
            service, args)

        self.request_number += 1
        self.requests.append(wrapper)

        return wrapper

    def removeRequest(self, service, *args):
        """
        Removes a request from the pending request list.

        @raise LookupError: Request not found.
        """
        if isinstance(service, RequestWrapper):
            del self.requests[self.requests.index(service)]

            return

        for request in self.requests:
            if request.service == service and request.args == args:
                del self.requests[self.requests.index(request)]

                return

        raise LookupError, "request not found"

    def getAMFRequest(self, requests):
        """
        Builds an AMF request L{envelope<pyamf.remoting.Envelope>} from a
        supplied list of requests.
        """
        envelope = remoting.Envelope(self.amf_version, self.client_type)

        for request in requests:
            service = request.service
            args = request.args

            envelope[request.id] = remoting.Request(str(service), args)

        return envelope

    def execute_single(self, request):
        """
        Builds, sends and handles the response to a single request, returning
        the response.
        """
        body = remoting.encode(self.getAMFRequest([request]))

        self.connection.request('POST', self._root_url, body.getvalue())

        envelope = self._getResponse()
        self.removeRequest(request)

        return envelope[request.id]

    def execute(self):
        """
        Builds, sends and handles the responses to all requests listed in
        C{self.requests}.
        """
        body = remoting.encode(self.getAMFRequest(self.requests))

        self.connection.request('POST', self._root_url, body.getvalue())

        envelope = self._getResponse()

        for response in envelope:
            request = self.getRequest(response[0])
            response = response[1]

            request.setResponse(response)

            self.removeRequest(request)

    def _getResponse(self):
        """
        Gets and handles the HTTP response from the remote gateway.

        @raise RemotingError: Incorrect MIME-type received.
        """
        http_response = self.connection.getresponse()

        if http_response.status != 200:
            raise remoting.RemotingError, "HTTP Gateway reported status %d" % (
                http_response.status,)

        content_type = http_response.getheader('Content-Type')

        if content_type != remoting.CONTENT_TYPE:
            raise remoting.RemotingError, "Incorrect MIME type received."

        content_length = http_response.getheader('Content-Length')
        bytes = ''

        if content_length is None:
            bytes = http_response.read()
        else:
            bytes = http_response.read(content_length)

        return remoting.decode(bytes)