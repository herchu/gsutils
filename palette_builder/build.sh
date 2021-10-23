#!/bin/bash

python palette.py
pushd out
zip ../RGB.zip *
popd
