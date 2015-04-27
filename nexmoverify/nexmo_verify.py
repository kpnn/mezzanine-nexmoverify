import requests

NEXMO_ERRORS = {
    '1': 'Throttled',
    '2': 'A parameter is missing',
    '3': 'Invalid value for parameter',
    '4': 'Invalid credentials were provided',
    '5': 'Internal Error',
    '6': 'Un-routable request',
    '7': 'The number is blacklisted for verification',
    '8': 'The api_key you supplied is for an account that has been barred from submitting messages',
    '9': 'Partner quota exceeded',
    '15': 'The destination number is not in a supported network',
    '16': 'The code inserted does not match the expected value',
    '17': 'A wrong code was provided too many times',
    '18': 'Too many request_ids provided',
    '101': 'No response found',
}


NEXMO_NUMBER_VERIFY_URL = 'https://api.nexmo.com/verify/json'
NEXMO_NUMBER_VERIFY_CHECK_URL = 'https://api.nexmo.com/verify/check/json'


#check_respone = {
#"event_id":"eventId",
#"status":"status",
#"price":"price",
#"currency":"currency",
#"error_text":"error"
#}


def get_error_msg(status):
    return NEXMO_ERRORS.get(status) or 'Unknown error'


class NexmoException(Exception):
    """Base exception for all Nexmo errors."""
    pass

class NexmoVerify(object):

    def __init__(self, api_key, api_secret, brand):
        self.api_key = api_key
        self.api_secret = api_secret
        self.brand = brand

    def verify(self, number, **kwargs):
        """
        https://docs.nexmo.com/index.php/verify/verify
        """
        data =  {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'number': number,
            'brand': self.brand 
        }
        data.update(kwargs)

        return self._send_request(NEXMO_NUMBER_VERIFY_URL, data)
            
            

    def check(self, request_id, code, ip_address=None):
        """
        https://docs.nexmo.com/index.php/verify/check
        """
        data =  {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'request_id': request_id,
            'code': code,
            'ip_address':ip_address
        }
        return self._send_request(NEXMO_NUMBER_VERIFY_CHECK_URL, data=data)

    def _send_request(self, url, data):
        r =  requests.post(url, data=data)
        print r
        if r.status_code != 200:
            raise Exception("Respone status: " + r.status_code)

        res = r.json()
        print res
        try:
            status = res.get('status')
        except:pass
        
        if '0' != status :
            raise NexmoException(get_error_msg(status), res)
        return res

# if __name__=='__main__':
#     verify = NexmoVerify(api_key='',
#                          api_secret='',
#                          brand='MyBrand')
#     print verify.verify('phone', country='')
#     print verify.check('request_id', 'code') 
