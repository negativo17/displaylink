#!/bin/sh

# https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu

VERSION=6.1.1
ZIP="DisplayLink USB Graphics Software for Ubuntu6.1.1-EXE.zip"

mkdir displaylink-$VERSION
pushd displaylink-$VERSION

unzip ../"$ZIP"

chmod +x displaylink-driver-$VERSION*.run
./displaylink-driver-$VERSION*.run --noexec --keep --target .

rm -fr evdi.tar.gz displaylink-driver-$VERSION*.run displaylink-$VERSION.zip
find . -name "libusb*.so*" -delete

popd

tar -cvJf displaylink-$VERSION.tar.xz --remove-files displaylink-$VERSION
