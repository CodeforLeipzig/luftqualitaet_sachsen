#! /bin/sh
#
# init.sh
# Copyright (C) 2015 plumps <plumps@lobsang.local>
#
# Distributed under terms of the MIT license.
#

# ---- install system packages ----

PACKAGES="cython daemontools npm nodejs-legacy postgresql-client postgresql python-pip python-dev python-virtualenv virtualenvwrapper libpq-dev git"

[ -n "$PACKAGES" ] && apt-get update && eval apt-get install -y --force-yes --no-install-recommends "$PACKAGES"

npm install -g bower

# ---- configuration of system packages ----

#add user vagrant to pg_hba.conf and define the auth mechanism as md5
sudo su -c "echo -e \"local\tall\t\tvagrant\t\t\t\t\tmd5\" >> /etc/postgresql/*/main/pg_hba.conf"

# ---- install user specific packages and data  ----

USER="vagrant"
VIRTUALENV="/home/$USER/.virtualenvs"  

sudo -i -u $USER env VIRTUALENV="$VIRTUALENV" HOME="/home/$USER" bash <<'EOF'
  mkdir -p $VIRTUALENV; export WORKON_HOME=$VIRTUALENV; echo WORKON_HOME=$VIRTUALENV >> $HOME/.bashrc
  source /usr/share/virtualenvwrapper/virtualenvwrapper.sh; mkvirtualenv luftverschmutzung_sachsen

  cd /vagrant; make install-dev; sudo -u postgres make create-db; make migrate 
EOF


exit 0



