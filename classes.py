class request:
    """"
    A class used to represent a HTTP request
    ...

    Attributes
    ----------
    content :  bytes
        the content of the request .
    url : str
        the url of the site the request is meant for
    """

    def __init__(self, flow):
        """"
        Parameters

        ----------
        flow : HTTP flow from mitmproxy object type
            the flow object containing the requests and responses
        """
        self.content = flow.request.content
        self.url = flow.request.url

    def update_flow(self):
        """"
        returns the content of the request object .
        input : none
        output: none
        """
        return [self.content, self.url]


class response:
    """"
    A class used to represent a HTTP request
    ...

    Attributes
    ----------
    content :  bytes
        the content of the request .
    content_type : str
        the content type header in the HTTP response
    content_length: str
        the content length header  in the HTTP response
    response_code: str
        the response code of the request -
            200 - ok
            302 - redirect
            etc
    ---------

    Note: the response_code and content_length are str types that represent an int
    """

    def __init__(self, flow):
        """"
        Parameters

        ----------
        flow : HTTP flow from mitmproxy object type
            the flow object containing the requests and responses
        """
        self.content = flow.response.content
        self.content_type = flow.response.headers.get("content-type", "")
        self.content_length = flow.response.headers.get("content-length", "")
        self.response_code = flow.response.status_code

    def update_flow(self):
        """"
        returns the content of the response object .
        input : none
        output: none
        """
        return [self.content, self.content_type, self.content_length, self.response_code]
