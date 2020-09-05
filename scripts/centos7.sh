sudo yum groupinstall "Development Tools"
sudo yum install git python3 gcc gmp gmp-devel gmp-status python3-devel mpfr-devel libmpc-devel -y
cd gflags
git checkout v2.0
./configure && make && sudo make install
cd ..
set CPATH=/usr/local/include
set LIBRARY_PATH=/usr/local/lib
sudo yum install snappy snappy-devel
sudo yum install zlib zlib-devel
sudo yum install bzip2 bzip2-devel
sudo yum install lz4-devel
wget https://github.com/facebook/zstd/archive/v1.1.3.tar.gz
mv v1.1.3.tar.gz zstd-1.1.3.tar.gz
tar zxvf zstd-1.1.3.tar.gz
cd zstd-1.1.3
make && sudo make install
cd ..