# -*- coding: utf-8 -*-
"""
   hotp,totp是用于身份验证的算法，客户端和服务端事先协商好一个密钥k，用于一次性密码生成，客户端和服务端
   各有一个计数器c，并且事先将计数值同步。验证时，客户端对密钥和计数器的组合使用hmac算法计算一次性密码。
   totp用时间戳作为计算器的值，每30秒跟换一次。
   
   此项目地址：'https://github.com/lepture/otpauth'
   
"""
import sys
import time
import hmac
import base64
import struct
import hashlib
import warnings


if sys.version_info[0] == 3:
    PY2 = False
    string_type = str
else:
    PY2 = True
    string_type = unicode
    range = xrange
	
	
__all__ = []


HOTP = 'hotp'
TOTP = 'totp'


class OtpAuth(object):
    def __init__(self, secret):
	    self.secret = secret
		
    def hotp(self, count=4):
	return generate_hotp(self.secret, count)
	    
    def totp(self, count=4):
	return generate_totp(self.secret, period=30, timestamp=None)
	    
    def valid_hotp(self, code, last=0, trials=100):
	if not valid_code(code):
	    return False
    
	code = bytes(int(code))
	for i in range(last + 1, last + trials + 1):
	    if compare_digest(bytes(self.hotp(count=i)), code):
		return i
	return False
	    
    def valid_totp(self, code, period=30, timestamp=None):
	if not valid_code(code):
		return False
	return compare_digest(
            bytes(self.totp(period, timestamp)),
                bytes(int(code))
        
        )
	    
    @property
    def encode_secret(self):
	secret = base64.b32encode(to_bytes(self.secret))
	secret = secret.encode('utf-8')
	return secret.strip('=')
	    
    def to_uri(self, _type, label, issuer, count=None):
	_type = _type.lower()
	    
	if _type not in ('hotp', 'totp'):
	    raise ValueError('type must be hotp or totp')
	
	if _type == 'hotp' and not count:
	    raise ValueError('HOTP type authentication need counter')
	
	url = ('otpauth://%(_type)s/%(label)s?secret=%(secret)s'
       '&issuer=%(issuer)s')
	dct = dict(
            _type=_type, label=label, issuer=issuer,
            secret=self.encode_secret, count=count
        )
	ret = url % dct
	if _type == 'hotp':
	    ret = '%s&count=%s' % (ret, count)
	return ret
	    
    def to_google(self, _type, label, issuer, count=None):
	warnings.warn('deprecated, use to_uri instead', DeprecationWarning)
        return self.to_uri(_type, label, issuer, count)
		

def generate_hotp(secret, count=4):
    msg = struct.pack('>Q', count)
    digest = hmac.new(to_bytes(secret), msg, hashlib.sha1).digest() # 默认使用md5算法，但sha1算法更好。携带了与计数器有关的初始信息。
	
    ob = digest[19]
    if PY2:
	ob = ord(ob)
	
    pos = ob & 15
    base = struct.unpack('>I', digest[pos:pos + 4])[0] & 0x7fffffff 
    token = base % 1000000
    return token
	
	
def generate_totp(secret, period=30, timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    count = int(timestamp) // period
    return generate_hotp(secret, count)


def to_bytes(text):
    if isinstance(text, string_type):
        text = text.encode('utf-8')
    return text


def valid_code(code):
    code = string_type(code)
    return code.isdigit() and len(code) <= 6


def compare_digest(a, b):
    func = getattr(hmac, 'compare_digest', None)
    if func:
        return func(a, b)

    if len(a) != len(b):
        return False

    rv = 0
    if PY2:
        from itertools import izip
        for x, y in izip(a, b):
            rv |= ord(x) ^ ord(y)
    else:
        for x, y in zip(a, b):
            rv |= x ^ y
    return rv == 0
	
		
if __name__ == "__main__":
    t = OtpAuth('secret')
    print t.hotp()
    print t.valid_hotp(330810)
    print t.to_uri('hotp', 'label', 'zhang', 4)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
			
	
