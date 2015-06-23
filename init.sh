#! /bin/sh
#
# init.sh
# Copyright (C) 2015 plumps <plumps@lobsang.local>
#
# Distributed under terms of the MIT license.
#

# --- install system packages ----

PACKAGES="npm nodejs-legacy postgresql-client postgresql python-pip python-dev python-virtualenv virtualenvwrapper libpq-dev git"

[ -n "$PACKAGES" ] && apt-get update && eval apt-get install -y --force-yes --no-install-recommends "$PACKAGES"

npm install -g bower

# ---- install user specific packages and data  ----

USER="vagrant"
VIRTUALENV="/home/$USER/.virtualenvs"  

sudo -i -u $USER env VIRTUALENV="$VIRTUALENV" HOME="/home/$USER" bash <<'EOF'
  mkdir -p $VIRTUALENV; export WORKON_HOME=$VIRTUALENV; echo $VIRTUALENV >> $HOME/.bashrc
  source /usr/share/virtualenvwrapper/virtualenvwrapper.sh; mkvirtualenv luftverschmutzung_sachsen
  cd /vagrant; make install
EOF


exit 0



