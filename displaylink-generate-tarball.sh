#!/bin/sh

# https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu

VERSION=6.4.0
ZIP="DisplayLink USB Graphics Software for Ubuntu6.4-EXE.zip"

mkdir displaylink-$VERSION
pushd displaylink-$VERSION

unzip ../"$ZIP"

chmod +x run/displaylink-driver-$VERSION*.run
./run/displaylink-driver-$VERSION*.run --noexec --keep --nox11 --target .

mv run/*Release\ Notes.txt .
rm -fr run evdi.tar.gz displaylink-driver-$VERSION*.run displaylink-$VERSION.zip
find . -name "libusb*.so*" -delete

popd

tar -cvJf displaylink-$VERSION.tar.xz --remove-files displaylink-$VERSION
