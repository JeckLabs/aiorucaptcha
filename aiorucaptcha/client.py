import asyncio
import aiohttp
import base64
import urllib
import time

from .errors import *
from .result import ResultObject

__all__ = ('Client', )


class Client:
    _host = ''

    def __init__(self, key, host='rucaptcha.com', timeout=60):
        self._key = key
        self._host = host
        self._timeout = timeout
        self._step = 5

    async def recognize_image(self, captcha, **kwargs):
        payload = kwargs
        payload['method'] = 'base64'
        payload['body'] = base64.b64encode(captcha)
        return await self._recognize(payload)

    # For backward compatibility
    recognize = recognize_image

    async def recognize_recaptcha(self, googlekey, pageurl, **kwargs):
        payload = kwargs
        payload['method'] = 'userrecaptcha'
        payload['googlekey'] = googlekey
        payload['pageurl'] = pageurl
        return await self._recognize(payload)

    async def _recognize(self, payload):
        with aiohttp.ClientSession() as client:
            task_id = await self._start(client, payload)
            payload = {'id':task_id, 'action':'get'}
            start = time.time()
            while True:
                await asyncio.sleep(self._step)
                result = await self._result(client, payload)
                if result.find('OK') == 0:
                    return ResultObject(result[3:], task_id)
                if time.time() - start > self._timeout:
                    raise TimeoutError()
                if result == 'CAPCHA_NOT_READY':
                    continue
                raise GeneralApiError(result)

    async def complain(self, task_id):
        with aiohttp.ClientSession() as client:
            payload = {'id':task_id, 'action':'reportbad'}
            result = await self._result(client, payload)
        if result == 'OK_REPORT_RECORDED':
            return True
        raise GeneralApiError(result)

    async def get_balance(self):
        with aiohttp.ClientSession() as client:
            payload = {'action':'getbalance'}
            result = await self._result(client, payload)
        try:
            return float(result)
        except ValueError:
            raise GeneralApiError(result)

    async def _start(self, client, payload):
        payload['key'] = self._key
        payload = urllib.parse.urlencode(payload)
        action = 'http://%s/in.php' % self._host
        async with client.post(action, data=payload) as resp:
            result = await resp.text()
        if result.find('OK') != 0:
            self._raise_if_error(result)
        return result[3:]

    async def _result(self, client, payload):
        payload['key'] = self._key
        payload = urllib.parse.urlencode(payload)
        action = 'http://%s/res.php?%s' % (self._host, payload)
        async with client.get(action) as resp:
            if resp.status != 200:
                raise HttpError('HTTP Code: %d' % resp.status)
            result = await resp.text()
        self._raise_if_error(result)
        return result

    def _raise_if_error(self, result):
        if result == 'ERROR_WRONG_USER_KEY':
            raise  WrongUserKeyError()
        elif result == 'ERROR_KEY_DOES_NOT_EXIST':
            raise KeyDoesNotExistError()
        elif result == 'ERROR_ZERO_BALANCE':
            raise ZeroBalanceError()
        elif result == 'ERROR_NO_SLOT_AVAILABLE':
            raise NoSlotAvailableError()
        elif result == 'ERROR_ZERO_CAPTCHA_FILESIZE':
            raise ZeroCaptchaFilesizeError()
        elif result == 'ERROR_TOO_BIG_CAPTCHA_FILESIZE':
            raise TooBigCaptchaFilesizeError()
        elif result == 'ERROR_WRONG_FILE_EXTENSION':
            raise WrongFileExtensionError()
        elif result == 'ERROR_IMAGE_TYPE_NOT_SUPPORTED':
            raise ImageTypeNotSupportedError()
        elif result == 'ERROR_IP_NOT_ALLOWED':
            raise IpNotAllowedError()
        elif result == 'IP_BANNED':
            raise IpBannedError()
        elif result == 'ERROR_WRONG_ID_FORMAT':
            raise WrongIdFormatError()
        elif result == 'ERROR_CAPTCHA_UNSOLVABLE':
            raise CaptchaUnsolvableError()
        elif result == 'ERROR_WRONG_CAPTCHA_ID':
            raise WrongCaptchaIdError()
        elif result == 'ERROR_BAD_DUPLICATES':
            raise BadDuplicatesError()
        elif result == 'REPORT_NOT_RECORDED':
            raise ReportNotRecordedError()
