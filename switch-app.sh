#!/bin/sh

cmdname=`basename $0`
cmdpath=`readlink -f $0 | xargs dirname`
appname=$1

proxy_conf=/etc/nginx/sites-enabled/hidakkathon-proxy
fastcgi_conf=/etc/nginx/sites-enabled/hidakkathon-fastcgi

case "$appname" in
    "go" | "python" | "ruby" ) 
        echo Switch nginx setting...
        [ -e $fastcgi_conf ] && sudo unlink $fastcgi_conf
        [ ! -e $proxy_conf ] && \
            sudo ln -s /etc/nginx/sites-available/hidakkathon-proxy $proxy_conf ;;
    "php" )
        echo Switch nginx setting...
        [ -e $proxy_conf ] && sudo unlink $proxy_conf
        [ ! -e $fastcgi_conf ] && \
            sudo ln -s /etc/nginx/sites-available/hidakkathon-fastcgi $fastcgi_conf ;;
    * )
        echo "Usage: $cmdname (go|python|ruby|php)" 1>&2
        exit 1 ;;
esac

$cmdpath/deploy-app.sh $appname

echo Stop apps...
systemctl stop hidakkathon-* > /dev/null 2>&1

echo Disable apps...
systemctl disable hidakkathon-* > /dev/null 2>&1

echo Start $cmdname app...
systemctl start hidakkathon-$appname > /dev/null 2>&1

echo Enable $cmdname app...
systemctl enable hidakkathon-$appname > /dev/null 2>&1

echo Reload nginx...
systemctl reload nginx > /dev/null 2>&1

echo Success!!!

