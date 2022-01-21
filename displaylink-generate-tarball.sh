#!/bin/sh

# https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu

VERSION=5.5.0
ZIP=https://www.synaptics.com/sites/default/files/exe_files/2021-12/DisplayLink%20USB%20Graphics%20Software%20for%20Ubuntu%20%28Beta%295.5%20Beta-EXE.zip

mkdir displaylink-$VERSION
pushd displaylink-$VERSION

wget $ZIP -O displaylink-$VERSION.zip
unzip displaylink-$VERSION.zip

chmod +x displaylink-driver-$VERSION*.run
./displaylink-driver-$VERSION*.run --noexec --keep --target .

rm -f evdi.tar.gz displaylink-driver-$VERSION*.run displaylink-$VERSION.zip
find . -name "libusb*.so*" -delete

popd

tar -cvJf displaylink-$VERSION.tar.xz --remove-files displaylink-$VERSION