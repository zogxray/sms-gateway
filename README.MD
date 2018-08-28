## About SMS-gateway

SMS-gateway is a web application to send and receive SMS and USSD cotes thought Goip device. That app has SPA interface to create SMS and USSD and lists of sent and received SMS and USSD codes. In other hand app has modern and simple API.

## Installation

#### Back
```console
$ pip install pipreqs
```

#### Front
```console
$ cd frontend && npm install && npm run build && cd ../
```
## Run for dev

#### Back
Execute migrations
```console
$ python db.py migrate
```
Seed test data
```console
$ python db.py db:seed
```
Run dev application
```console
$ python app.py
```
Run SMS recive proccess
```console
$ python server.py
```
Run SMS send process
```console
$ python sms.py
```
Run USSD send process
```console
$ python ussd.py
```

#### Docker install
```console
docker-compose up
docker exec -it id python db.py migrate --seed --force
```
#### Docker run
```console
docker exec -it id python smpp_send.py
docker exec -it id python smpp_recieve.py
```


## Setup on goip device

Setup SMS-gateway address, port, SMS Client ID and Password on Goip device in Configurations->SMS. Add rows in SMS-gateway channels to listen that.

## Security Vulnerabilities

If you discover a security vulnerability within SMS-gateway, please send an e-mail to Viktor Pavlov via [zogxray@gmail.com](mailto:zogxray@gmail.com). All security vulnerabilities will be promptly addressed.

## License

The SMS-gateway is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).