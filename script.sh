if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
    echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
    echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
    echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
