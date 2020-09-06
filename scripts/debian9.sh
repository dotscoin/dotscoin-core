sudo apt-get install -y make build-essential libssl-dev zlib1g-dev
sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
sudo apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev
cd /home
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar xvf Python-3.6.4.tgz
cd Python-3.6.4
./configure --enable-optimizations
make -j8
sudo make altinstall
sudo apt install libgmp-dev libmpfr-dev libmpc-dev -y
sudo apt install build-essential -y