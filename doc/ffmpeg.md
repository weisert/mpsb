#### FFMPEG installation

```bash
sudo apt-get install yasm libx264-dev zlib1g-dev pkg-config
cd /tmp
wget http://ffmpeg.org/releases/ffmpeg-3.0.1.tar.bz2
tar xf ffmpeg-3.0.1.tar.bz2
cd ffmpeg-3.0.1
./configure --enable-pthreads --enable-shared --enable-gpl --enable-libx264 --enable-encoder=png
make -j
sudo make install
sudo ldconfig
```
