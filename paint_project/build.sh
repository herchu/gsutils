#!/bin/bash
#
# Arma varios tableros de ejemplo con img2board, y empaqueta el proyecto
# (cuyo template esta en 'contents') en un proyecto Gobstones: Paint.gbp
#

PRJ=Paint.gbp
DIR=contents
IMG_TOOL="python ../img2board/img2board.py"
SKIN_FILE=rgb64_v1.zip

B=1
while read IMG; do
  echo "Creando tablero Board$B.gbb de imagen $IMG..."
  BOARD=$DIR/assets/boards/Board$B.gbb
  $IMG_TOOL $IMG $BOARD
  ((B=B+1))
done <boards.txt

echo "Copiando vestimenta"
SKIN_DIR=$DIR/attires/RGB
mkdir -p $SKIN_DIR
pushd $SKIN_DIR
rm *.png *.yml
unzip ../../../$SKIN_FILE
popd

echo "Empaquetando proyecto $PRJ"
[ -f $PRJ ] && rm $PRJ
pushd $DIR
zip ../$PRJ * -r -x '*.git'
popd
