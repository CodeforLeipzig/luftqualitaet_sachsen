************
Installation
************

NEW alternative setup with Vagrant
================================

Just clone the repo and start the virtual machine with the help of vagrant::
    
    $ vagrant up --provider=virtualbox

When it's finished you may enter the machine and the Python environment with the following commands::
    
    $ vagrant ssh
    
    $ workon luftverschmutzung_sachsen

All the upstream code is persistenly mounted to /vagrant    

**Hint**: Until now the vagrant file only finishes the install-dev target, as there is a problem with the createdb target as of yet

Development Setup (manual way)
=================
You should install virtualenv, to separate the build artefacts from the rest of your system. On Debian based Linux distributions, it may look like this::
    
    $ apt-get update && eval apt-get install -y --force-yes --no-install-recommends python-virtualenv virtualenvwrapper
    
Create the the virtualenv and enter it::

    $ mkvirtualenv luftverschmutzung_sachsen

Install the packages for development::

    $ make install-dev

And install the frontend dependencies using `Bower <http://bower.io/>`_::

    $ bower install

Then create the new PostgreSQL user and database::

    $ make create-db

Now create the database tables::

    $ make migrate

And start the development webserver::

    $ make runserver

To see the other targets available in the ``Makefile`` simply run::

    $ make
