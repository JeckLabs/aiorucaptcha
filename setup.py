from setuptools import setup

install_requires = ['aiohttp>=0.21']

setup(name='aiorucaptcha',
      version='0.1',
      description='Rucaptcha.com asyncio client',
      url='https://github.com/JeckLabs/aiorucaptcha',
      author='Evgeniy Baranov',
      author_email='i@jeck.ru',
      license='Apache 2',
      packages=['aiorucaptcha'],
      install_requires=install_requires,
      zip_safe=False)