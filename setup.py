from setuptools import setup


setup(
    name='hmara-signalbot',
    version='0.0.1',
    url='https://signal-bot.github.io',
    license='AGPL-3.0',
    packages=['signalbot', 'signalclidbusmock'],
    entry_points={
        'console_scripts': [
            'hmara-signal-bot=signalbot.cli:main',
        ]
    }
)
