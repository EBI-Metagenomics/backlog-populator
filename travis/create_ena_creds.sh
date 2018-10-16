#!/usr/bin/env bash
configpath="$TRAVIS_BUILD_DIR/ena_creds.yml";
touch $configpath;
echo "USERNAME: $ENA_USERNAME" >> $configpath;
echo "PASSWORD: $ENA_PASSWORD" >> $configpath;