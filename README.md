# codelog.telegram-login

Example: https://codelog-telegram-login.aws-hknsidwoow.luzi82.com/

## Requirements

1. AWS account: this example based on AWS.
1. Web domain under AWS route 53: Telegram require domain for callback.
1. Telegram account.

## How-to

1. Create new Telegram bot.  https://core.telegram.org/bots
1. In Telegram botfather, use /setdomain to link the bot with your domain.  https://core.telegram.org/widgets/login
1. Copy conf/conf.json.sample to conf/conf.json.
1. Modify conf/conf.json.
1. Run `./aws-deploy.sh`
1. Go to https://your.domain.com to test.
