'''
Wrapper for the ifile.it API. Uses the poster api.
'''
import urllib2
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib

class Ifileit(object):
    """ Wrapper class for the ifile.it API. """
    
    UPOLOADED_FILE_URL = 'http://ifile.it/{ukey}'
    GET_UPLOAD_URL = 'http://ifile.it/api-fetch_upload_url.api'
    FETCH_API_KEY_URL = 'https://secure.ifile.it/api-fetch_apikey.api'
    PING_URL = 'http://ifile.it/api-ping.api'
    
    USER = 'chacholano'
    PASSWORD = 'dx9dx9'
    API_KEY = ''
    
    @classmethod
    def ping(cls):
        """ Returns True if the ifile.it server is up. """
        
        response = cls._open_and_check(cls.PING_URL)
        return response.get('message', '') == 'pong'
    
    @classmethod
    def upload(cls, the_file):
        """ 
        Uploads the_file to the ifile.it server. It should be a file-like 
        object as required by poster. 
        """
        
        #Needed by poster
        register_openers()
    
        post_data = {'Filedata' : the_file}
        post_data.update(cls._get_akey())
        datagen, headers = multipart_encode(post_data)
        
        request = urllib2.Request(cls._determine_upload_url(), 
                                                    datagen, headers)
        response = cls._open_and_check(request) 
        
        return cls.UPOLOADED_FILE_URL.format(ukey=response['ukey'])
    
    @classmethod
    def _determine_upload_url(cls):
        """ Gets the upload url from ifile.it API. """
        
        return cls._open_and_check(cls.GET_UPLOAD_URL)['upload_url']
    
    @classmethod
    def _open_and_check(cls, url, data=None):
        """ 
        Opens the given url string or Request object and checks for the status
        parameter in the response.  If it's 'ok' returns a dict with the 
        response. otherwise raises IfileitApiError.
        
        Data should be a dictionary of POST arguments or None for a GET request.
        """
        
        if data:
            data = urllib.urlencode(data)
        
        response = json.loads(urllib2.urlopen(url, data).read())
    
        if response['status'] != 'ok':
            raise IfileitApiError()
        
        return response
    
    @classmethod
    def _get_akey(cls):
        """ 
        If the user info is set, return the akey parameter for the POST API 
        calls. Otherwise returns an empty dict.
        """
        
        if cls.USER and cls.PASSWORD:
            if not cls.API_KEY:
                response = cls._open_and_check(cls.FETCH_API_KEY_URL, 
                                               {'username' : cls.USER,
                                                'password' : cls.PASSWORD})
                cls.API_KEY = response['akey']
            
            return {'akey' : cls.API_KEY }
        
        return {}

class IfileitApiError(Exception):
    pass
