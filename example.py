import asyncio
import aiorucaptcha

async def recognize(ocr, filename):
    with open(filename, 'rb') as f:
        captcha = f.read()
        result = await ocr.recognize(captcha)
        print(result)

# Вместо xxx ключ RuCaptcha
ocr = aiorucaptcha.Client('xxx')

loop = asyncio.get_event_loop()
tasks = [
    asyncio.Task(recognize(ocr, 'captcha_a.gif')),
    asyncio.Task(recognize(ocr, 'captcha_b.gif'))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()