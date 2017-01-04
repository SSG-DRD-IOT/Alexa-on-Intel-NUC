#install pip
wget https://bootstrap.pypa.io/get-pip.py
python ./get-pip.py

pip install requests
pip install pymata
pip install AWSIoTPythonSDK

npm install mraa

smart install python-dev
smart install alsa-lib-dev

# install memechached
wget https://pypi.python.org/packages/f7/62/14b2448cfb04427366f24104c9da97cf8ea380d7258a3233f066a951a8d8/python-memcached-1.58.tar.gz
tar xf python-memcached-1.58.tar.gz
cd python-memcached-1.58
python setup.py build
python setup.py install
cd ..

#Install pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py


#install pyalsaaudio
smart channel --add Intel_Repository type=rpm-md baseurl=https://download.01.org/iotgateway/rcpl13/x86_64/
smart update
smart install python-distribute
smart channel --add corei7_64 type=rpm-md baseurl=https://distro.windriver.com/release/idp-3-xt/public_feeds/WR-IDP-3-XT-Intel-Baytrail-public-repo/RCPL13/corei7_64/
easy_install --install-dir /usr/lib64/python2.7/site-packages/ pyalsaaudio

#install mpg123
wget http://downloads.sourceforge.net/mpg123/mpg123-1.23.8.tar.bz2
tar xf mpg123-1.23.8.tar.bz2
cd mpg123-1.23.8
./configure --prefix=/usr --with-module-suffix=.so
make
make install
cd ..
