#!/bin/bash
#git clone https://github.com/chentinghao/download_google_drive.git

mob=1eGHN4KcMl6X4SAAoFOe2m8SRZLXXkWLW
bea=1M-UK5YmSYVEaClyWq3RNNkHctQ2qvQk9
fas=1nVA1iZBUS79WQghO9DXg54qgxnw9OSI3
mobf=mobile_image.tar.gz
beaf=beauty_image.tar.gz
fasf=fashion_image.tar.gz
dir=../tars/

python download_gdrive.py "$mob" "$dir$mobf"
#python download_gdrive.py "$bea" "$dir$beaf"
#python download_gdrive.py "$fas" "$dir$fasf"