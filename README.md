cyclee_server
=============

[![Build Status](https://secure.travis-ci.org/Cyclee/cyclee_server.png)](http://travis-ci.org/Cyclee/cyclee_server)


Getting Started
---------------

The cyclee server requires postgresql and postgis. To install these on
a debian based system, run the following command:

    apt-get install postgresql postgis postgresql-9.1-postgis

Check out the code from the repo:

    git clone git@github.com:Cyclee/cyclee_server.git

Always use a virtualenv when working on python projects, I suggest
virtualenv-wrapper. Create a new env:

    mkvirtualenv cyclee


Install the python requirements.:

    python setup.py develop

And run the development server:

    pserver development.ini --reload


Testing
--------

You need to create a test postgresql database.:

    createdb cyclee_test
   
And it must have the postgis extensions installed. To run the test
suite, use the following command: 

     python setup.py test


Production
-----------




REST API
--------
The rest api:

    GET      /traces
    POST     /traces

    GET       /traces/{id}
    POST      /traces/{id}
    DELETE    /traces/{id}

    
    GET      /rides
    POST     /rides

    
    GET      /rides/{id}
    POST     /rides/{id}
    DELETE   /rides/{id}

    GET     /rides/{id}/traces
    
