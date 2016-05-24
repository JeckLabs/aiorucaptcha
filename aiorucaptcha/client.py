import asyncio
import aiohttp
import base64
import urllib
import time

from .errors import *

__all__ = ('Client', )


class Client:
    _host = ''

    def __init__(self, key, host='rucaptcha.com', timeout=60):
        self._key = key
        self._host = host
        self._timeout = timeout
        self._step = 5


    async def recognize(self, captcha, **kwargs):

        payload = kwargs

        payload['key'] = self._key
        payload['method'] = 'base64'
        payload['body'] = base64.b64encode(captcha)

        with aiohttp.ClientSession() as client:
            task_id = await self._start(client, payload)

            start = time.time()
            while True:
                await asyncio.sleep(self._step)

                result = await self._result(client, task_id)

                if result:
                    return result

                if time.time() - start > self._timeout:
                    raise TimeoutError()


    async def _start(self, client, payload):
        payload = urllib.parse.urlencode(payload)
        action = 'http://%s/in.php' % self._host
        async with client.post(action, data=payload) as resp:
            result = await resp.text()

            if result.find('OK') != 0:
                raise self._error(result)

            return result[3:]

    async def _result(self, client, task_id):
        payload = {
            'key': self._key,
            'action': 'get',
            'id': task_id
        }
        payload = urllib.parse.urlencode(payload)
        action = 'http://%s/res.php?%s' % (self._host, payload)

        async with client.get(action) as resp:
            if resp.status != 200:
                raise HttpError('HTTP Code: %d' % resp.status)

            result = await resp.text()

            if result.find('OK') == 0:
                return result[3:]
            elif result == 'CAPCHA_NOT_READY':
                return False
            else:
                raise self._error(result)

    def _error(self, result):
        if result == 'ERROR_WRONG_USER_KEY':
            return WrongUserKeyError()
        elif result == 'ERROR_KEY_DOES_NOT_EXIST':
            return KeyDoesNotExistError()
        elif result == 'ERROR_ZERO_BALANCE':
            return ZeroBalanceError()
        elif result == 'ERROR_NO_SLOT_AVAILABLE':
            return NoSlotAvailableError()
        elif result == 'ERROR_ZERO_CAPTCHA_FILESIZE':
            return ZeroCaptchaFilesizeError()
        elif result == 'ERROR_TOO_BIG_CAPTCHA_FILESIZE':
            return TooBigCaptchaFilesizeError()
        elif result == 'ERROR_WRONG_FILE_EXTENSION':
            return WrongFileExtensionError()
        elif result == 'ERROR_IMAGE_TYPE_NOT_SUPPORTED':
            return ImageTypeNotSupportedError()
        elif result == 'ERROR_IP_NOT_ALLOWED':
            return IpNotAllowedError()
        elif result == 'IP_BANNED':
            return IpBannedError()
        elif result == 'ERROR_WRONG_ID_FORMAT':
            return WrongIdFormatError()
        elif result == 'ERROR_CAPTCHA_UNSOLVABLE':
            return CaptchaUnsolvableError()
        elif result == 'ERROR_WRONG_CAPTCHA_ID':
            return WrongCaptchaIdError()
        elif result == 'ERROR_BAD_DUPLICATES':
            return BadDuplicatesError()
        elif result == 'REPORT_NOT_RECORDED':
            return ReportNotRecordedError()
        else:
            return GeneralApiError(result)
