#!/bin/sh

cmdname=`basename $0`
cmdpath=`readlink -f $0 | xargs dirname`

if [ -z "$1" ]; then
    echo "Usage: $cmdname (go|python|ruby|php)" 1>&2
    exit 1
fi
appname=$1
old_wd=`pwd`

set -eu

cd $cmdpath
git pull

case "$appname" in
    "go" )
        cd $cmdpath/$appname
        echo Try to build $appname application...
	go build -o bin/hidakkathon ;;
    "python" )
        cd $cmdpath/$appname
        echo Try to build $appname application...
	pip install -r requirements.txt ;;
    "ruby" )
        cd $cmdpath/$appname
        echo Try to build $appname application...
	bundle install --path vendor/bundle ;;
    "php" )
        cd $cmdpath/$appname
        echo Try to build $appname application...
	composer install ;;
    * )
        echo "Usage: $cmdname (go|python|ruby|php)" 1>&2
        exit 1 ;;
esac

cd $old_wd

echo Stop apps...
systemctl stop hidakkathon-* > /dev/null 2>&1

echo Start $cmdname app...
systemctl start hidakkathon-$appname > /dev/null 2>&1

echo Success!!!

