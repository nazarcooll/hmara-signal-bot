[![Build Status](https://travis-ci.org/signal-bot/signal-bot.svg?branch=master)](https://travis-ci.org/signal-bot/signal-bot)

# hmara-signal-bot

This project is in its infancy!

this bot should work in integration with Hmara project, here all the plugins should be created

# installation

pip install -i https://test.pypi.org/simple/ hmara-signalbot

# run

to run worker the signal-cli should be installed with dbus service and there has to be registered user
to start worker just run "hmara-signal-bot" in the console

## The idea

* signal-bot provides headless chat/bot/monitoring services for the [Signal][signal] messenger.
* Services are made available via plugins.
* Writing new plugins to extend functionality is easy and modular since signal-bot smoothly wraps around [signal-cli][signal-cli] in order to provide a convenient Python framework.

```python
from signalbot import Signalbot
from signalbot.signalbot import Chat

with Signalbot(is_from_worker=False) as bot:
    bot.send_message("test", [], Chat(bot, '+XXXXXXXXXXXX'))
```


[signal]: https://signal.org/
[signal-cli]: https://github.com/AsamK/signal-cli
[signal-dbus]: https://github.com/AsamK/signal-cli/blob/master/src/main/java/org/asamk/Signal.java
