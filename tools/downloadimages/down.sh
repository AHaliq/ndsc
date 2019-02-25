#!/bin/bash

mob=https://www.dropbox.com/s/ss2ibxu0k4x9c91/mobile_image.tar.gz?dl=1
bea=https://www.dropbox.com/s/bhy4b7bwsvvhtf6/beauty_image.tar.gz?dl=1
fas=https://www.dropbox.com/s/3jpwfbeilm22vhs/fashion_image.tar.gz?dl=1
mobf=mobile_image.tar.gz
beaf=beauty_image.tar.gz
fasf=fashion_image.tar.gz
dir=../tars/

#wget -O "$dir$mobf" "$mob"
wget -O "$dir$beaf" "$bea"
#wget -O "$dir$fasf" "$fas"