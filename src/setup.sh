#!/bin/bash

OS=$(uname -s)

echo "Installing Packages & Tools"
echo $(pip install -r requirements.txt)

if [ $OS = "Darwin" ]; then
    #check if brew is installed
    if ! [ -x "$(command -v brew)" ]; then
        echo "Need Homebrew to install gdal and osm2pgsql, proceed with installation? (y/n)"
        read response
        if [ $response = "y" ]; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        else
            echo "Please install Homebrew and run the script again"
            exit 1
        fi
    fi
    echo $(brew install gdal osm2pgsql)
else
    echo $(apt-get install -y gdal-bin osm2pgsql)
fi

echo "Setup Complete"



