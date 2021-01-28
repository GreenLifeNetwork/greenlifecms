# greenlifecms

Public content of the app GreenLife (or Greta life).

The app API will provide the content of the WeCroak style app to remind people about simple ways to live a more sustainable life.

Every content should englighten the user about the little green habits that make a big difference.

The biggest driver for mindless consumerism is living "uncounsciously" (as in "the power of now").

Simple habits and a simple life remind us about what we really are. We are children of the earth.

## Install
- Requires Python3 (<=3.8 on Windows)
- `pip -r install requirements.txt`
- `python manage.py runserver`

## Windows issues

Andy?

## Run locally with SSL

Because we're caching images with SSL. We need to run on SSL to display the image. You need to run `python manage.py runsslserver --certificate cert.pem --key key.pem` after going through the install as described on: [https://medium.com/@millienakiganda/creating-an-ssl-certificate-for-localhost-in-django-framework-45290d905b88](Creating an SSL certificate for localhost in Django framework)
