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

To start the Django http server, just run::
    
    $ make runserver-vagrant

Manual way 
=================
It's recommened to install virtualenv, it helps to separate the build artefacts from the rest of your system. On Debian based Linux distributions, it may look like this::
    
    $ apt-get update && apt-get install -y --force-yes --no-install-recommends python-virtualenv virtualenvwrapper
    
Create the the virtualenv and enter it::

    $ mkvirtualenv luftverschmutzung_sachsen
    
To exit the environment you enter **deactivate** and to re-enter it **workon luftverschmutzung_sachsen**

Install the packages for development::

    $ make install-dev

There might be a stumbling block regarding the auth configuration in PostgreSQL. In my experiments with Ubuntu 14.04 LTS I found out the "peers" setting to be default for local access of "all users", except this doesn't work with this Django App. 
You need a user/pass auth regime aka md5 .

An example configuration in **/etc/postgersql/<version>/main/pg_hba.conf** might be:
local   all             all                                     md5


Then create the new PostgreSQL user and database, depends heavily on your PostgreSQL installation!::

    $ (sudo -u postgres) make create-db

Now create the database tables::

    $ make migrate

And start the development webserver::

    $ make runserver

To see the other targets available in the ``Makefile`` simply run::

    $ make
