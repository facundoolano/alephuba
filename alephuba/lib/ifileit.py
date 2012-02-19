'''
Wrapper for the ifile.it API. Uses the requests api.
'''
import requests
import json

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
        
        data = cls._get_akey()
        response = cls._open_and_check(cls._determine_upload_url(), data=data,
                                                    files={'Filedata' : the_file})
        
        return cls.UPOLOADED_FILE_URL.format(ukey=response['ukey'])
    
    @classmethod
    def _determine_upload_url(cls):
        """ Gets the upload url from ifile.it API. """
        
        return cls._open_and_check(cls.GET_UPLOAD_URL)['upload_url']
    
    @classmethod
    def _open_and_check(cls, url, **kwargs):
        """ 
        Opens the given url string or Request object and checks for the status
        parameter in the response.  If it's 'ok' returns a dict with the 
        response. otherwise raises IfileitApiError.
        
        kwargs can contain data or files as used by requests post method.
        """
        
        if kwargs:
            response = requests.post(url, **kwargs)
        else:
            response = requests.get(url)
            
        response = json.loads(response.text)
    
        if response['status'] != 'ok':
            raise IfileitApiError(response['message'])
        
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
                                               data={'username' : cls.USER,
                                                     'password' : cls.PASSWORD})
                cls.API_KEY = response['akey']
            
            return {'akey' : cls.API_KEY }
        
        return {}

class IfileitApiError(Exception):
    pass
