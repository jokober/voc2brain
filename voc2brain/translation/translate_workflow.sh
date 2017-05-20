#!/bin/bash
tx pull -s -f
tx pull -a -f


cd ..
pylupdate4 uebersetzen.pro
cd translation 
cd translations
cd Voc2brain.Voc2brainDesktop
lrelease *.ts
cp *.qm ../..
cd ..
cd ..

tx push -s -f
tx push -t -f --skip