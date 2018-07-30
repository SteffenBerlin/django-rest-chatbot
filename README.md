# Django REST Chatbot

A chatbot API with the RASA chatbot built into a Django REST Boilerplate

## Getting Started

The following README.md is copied from https://github.com/nils-wisiol/django-rest-boilerplate
All credits for this great work go to https://github.com/nils-wisiol/ !!

The info about the built-in chatbot API is not yet addressed in this Readme.

### Docker 
This project uses Docker CE and Docker Compose to run all services. [Installing Docker](https://docs.docker.com/engine/installation/#supported-platforms)
depends on the platform and is hence not included here. Docker Compose has to be [installed separately](https://docs.docker.com/compose/install/).
 
### Source Code
To obtain the source code of the Django Rest Boilerplate, please clone this repository.

    git clone https://github.com/nils-wisiol/django-rest-boilerplate

### Running
Runnig django-rest-boilerplate requires a fully configured `.env` file. A template for `.env` can be found in `.env.default`. Below, all values are documented.

 - `BOILERPLATE_DOMAIN`: the domain name of the service provided
 - `BOILERPLATE_IPV4_16PREFIX`: internal network IPv4 address prefix. The default value `172.16` will suit most users.
 - `BOILERPLATE_IPV6_SUBNET`: internal network IPv6 subnet. The default value `bade:affe:dead:beef:b011::/80` will suit most users. 
 - `BOILERPLATE_IPV6_ADDRESS`: internal network IPv6 address. The default value `bade:affe:dead:beef:b011:0642:ac10:0080` will suit most users.
 - `BOILERPLATE_WWW_CERTS`: location of the required SSL certificates in PEM format. This folder can contain the following four files, named after the domain name they will be used for. For example, if your `BOILERPLATE_DOMAIN` is `boilerplate.local`, then name your certificates files:
    * `boilerplate.local.cer`, `boilerplate.local.key`: certificate and private key for `BOILERPLATE_DOMAIN`.
    * `www.boilerplate.local.cer`, `www.boilerplate.local.key`: certificate and private key for www. `BOILERPLATE_DOMAIN`.
    
    The certificates can be obtained any way (and can also be the same). Please [see below for an convenient way](#dedyn.io-cert) to obtain debug certificates for `BOILERPLATE_DOMAIN` (but lacking a valid certificate for www.`BOILERPLATE_DOMAIN`).
    If you don't provide certificates, the `www` container will generated short-term self-signed certificates on startup.
 - `BOILERPLATE_API_SECRETKEY`: needs to be set to an instance-specific [random secret value](https://www.random.org/passwords/?num=5&len=24&format=html&rnd=new).
 - `BOILERPLATE_DB_PASSWORD`: the database user password, should also be set to an instance-specific random secret value.

After populating `.env` with all appropriate values, the service can be started with

    docker-compose up
    
and be reached at your chosen domain name. Remember to have your domain name point at `$BOILERPLATE_IPV4_16PREFIX`.0.128 (for the default configuration this is 172.16.0.128). At http://example.com/api/admin/, the generic django administration backend is available.

### Django Management Console

Many development tasks require the django management console, which can be reached though the `exec` command of docker-compose. A typical example includes creating the django superuser to first login to Django.

    docker-compose exec api python manage.py createsuperuser
    
To see a list of available management commands, call

    docker-compose exec api python manage.py 
    
### Database

To access the database directly, use

    docker-compose exec db mysql -u root
  
(No password required.)

The database is stored in a Docker volume and hence persistent even if containers or images are newly built. To reset the database, use the docker-compose `down` command with the appropriate flag(s) to remove all containers, images, networks, and volumes:

    docker-compose down -v
    
## Project Design

This project consists of a Docker Compose project with four Docker containers; it follows the "one service per container" pattern.

The containers are arranged as shown in this diagram. Inter-service communication is only permitted along the connections shown:

    (user) --- www --- api --- db
                  \--- static

  - **The `www` container** accepts all incoming connections. It handles
    * forwarding the request to either the API or static servers,
    * transport layer security, and
    * rate limits.
    
    It is currently implemented using an `nginx` webserver.
  - **The `static` container** serves static files. This can be a basic website advertising the API service or an involved JavaScript application designed for usage with the API. (It can also be easily removed entirely.)
  - **The `api` container** contains the Django-implemented RESTful API implementation. As such, it handles
    * routing of all requests with URL beginning with `https://$BOILERPLATE_DOMAIN/api/`,
    * authentication of these requests, and
    * providing requested data and/or updating the database accordingly.

    It communicates with `www` through an `uwsgi` interface.
  - **The `db` container** provides the MySQL (MariaDB) database used by the `api`. It is the only container in our setup that uses a Docker volume to persistently store data.

There is an additional container for testing:

  - **The `test-e2e` container** mocks an user and executes the defined end-to-end tests. (Cf. test/e2e/spec/*_spec.js.)

The detailed design of the single containers is quite involved. Please refer to their individual READMEs.

## Deployment

Docker enables you to deploy binary identical software from your development machine to the production servers.
This enables you to make sure that all dependencies will be shipped with your Docker image to the server,
minimizing the chance of a botched deployment.
To deploy, we build all images on your local machine, push them to a Docker image server (Docker Hub).
Afterwards, we instruct the production server to download the images and start containers.

### Step by Step Guide

To deploy your project to the production server, first customize the `image` options in `docker-compose.yml` with a proper name and register it with [Docker Hub](https://hub.docker.com/).
After logging in to Docker Hub, compile all images on your development machine using

    docker-compose build --no-cache --pull
    
The `pull` option will update any dependencies (within the version stated in our Dockerfiles).
Afterwards, publish your images with 

    docker-compose push
    
Note that your code will be publicly available on Docker Hub.
(Alternatively, you can sign up for a paid plan or use your own hub.)

On your production machine, make sure that `.env` and `docker-compose.yml` are available (as well as any dependencies, such as SSL certificates) and run

    docker-compose pull
    docker-compose up
    
For updating the production server, the procedure is the same (with the exception that the registration with Docker Hub does not need to be repeated.)
Note that environment and database will be different on production and hence can cause complications during database migration upon service restart after the update.

## Tests

Currently, the boilerplate only ships e2e tests. Those are implemented in [chakram](http://dareid.github.io/chakram/). The test spects can be found in `test/e2e/spec`. Please refer to the chakram documentation on how to write specs.

To run the tests, ensure the project is already up and running (especially the database takes some time to boot for the first time) by running

    docker-compose up --build www
    
To run the actual tests, use

    docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build test-e2e
    
The `.travis.yml` contains instructions for travis on how to bootstrap the entire system from scratch.



## Development

As the entire project runs across several Docker containers, usage of any python just in time (JIT) debugger is quite involved.
We appreciate all contributions integrating easy usage of JIT debuggers!



<a name="dedyn.io-cert"></a>
## Obtain Debug Certificates With dedyn.io 

dedyn.io provides an easy way to obtain Let's Encrypt certificates without the need of running your own HTTP server, as it utilizes DNS owner verification rather than HTTP owner verification.

Register a domain name of your choice at desec.io. After registration, you will receive an email with your credentials to update the domain name's IP address. To use the domain for development on your machine, let the domain name point to the IP address of the `www` service (`$BOILERPLATE_IPV4_16PREFIX`.0.128) by sending an HTTP request to 

<pre>
https://update.dedyn.io/update?username=<em>example.dedyn.io</em>&amp;password=<em>yourpassword</em>&amp;ip=172.16.0.128
</pre>

Then follow [their guide to obtain a Let's Encrypt certificate](https://desec.io/#!/en/docs/certbot). Notice that dedyn.io currently only supports certificates for `example.dedyn.io`, but not for any subdomains.

After successfully obtaining the LE certificate, it will be placed in PEM format in `/etc/letsencrypt/live/example.dedyn.io/` and needs to be moved to the location specified above in `.env`. (Be sure to use `fullchain.pem` as most clients will otherwise not accept the certificate.)

As dedyn.io currently does not support issuance of certificates for subdomains, we recommend using the (then invalid) main certificate also for the www subdomain. This will result in a security warning when browsing to www.`BOILERPLATE_DOMAIN`. (However, the www container will fall back to self-signed certificates when you do not provide a certificate for every domain.)

## Getting Help
Any Django questions are best answered by [their documentation and support channels](https://docs.djangoproject.com/en/1.11/). If there is anything related directly to this project, please open an issue or pull request on GitHub.

## Security Updates
This projects contains Django 1.11 LTS, which will receive mainstream updates until December 2017 and 
security updates until at least April 2020. 
It also relies on [restframework](http://www.django-rest-framework.org/) which does not specify any maintenance cycle,
but is an active project on [GitHub](https://github.com/encode/django-rest-framework).

## License

All work in this repository is licensed under the MIT license. For details, see the LICENSE file.

## Acknowledgements
Much of the techniques used in this project is courtesy of the [deSEC project](https://desec.io), some changes were backported after the [eID project of Freie Universität Berlin](https://github.com/swp-fu-eid/eid-fu-swp) used the boilerplate to bootstrap their project.
