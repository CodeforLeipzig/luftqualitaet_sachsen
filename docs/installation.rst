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
    
    $ cd /vagrant

All the upstream code is persistenly mounted to /vagrant    

**Hint**: Until now the vagrant file only finishes the **create-db** target, as there is a problem with the migrate target as of yet

Manual way 
=================
It's recommened to install virtualenv, it helps to separate the build artefacts from the rest of your system. On Debian based Linux distributions, it may look like this::
    
    $ apt-get update && apt-get install -y --force-yes --no-install-recommends python-virtualenv virtualenvwrapper
    
Create the the virtualenv and enter it::

    $ mkvirtualenv luftverschmutzung_sachsen
    
To exit the environment you enter **deactivate** and to re-enter it **workon luftverschmutzung_sachsen**

Install the packages for development::

    $ make install-dev
    

The interactive part
====================

As of now you have a system with all prerequisties running, whether this is a vagrant instance or a custom system shouldn't matter. In the case of vagrant you need to enter all the following commands within the vagrant instance. (e.g. to enter it **vagrant ssh** )

Then create the new PostgreSQL user and database::

    $ make create-db

Now create the database tables::

    $ make migrate

And start the development webserver::

    $ make runserver

To see the other targets available in the ``Makefile`` simply run::

    $ make
