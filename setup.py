from setuptools import setup

setup(
    name='hmara-signalbot',
    version='0.0.5',
    license='AGPL-3.0',
    packages=['signalbot', 'signalclidbusmock', 'signalbot.plugins', 'signalbot.plugins.pingpong'],
    entry_points={
        'console_scripts': [
            'hmara-signal-bot=signalbot.worker:main',
        ],
    }
)
