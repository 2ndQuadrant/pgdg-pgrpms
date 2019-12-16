#!/bin/bash
#
# Use a container to build PostGIS 2.5 for PostgreSQL 2.5 on CentOS/RHEL 6
#

SUDO=${SUDO:-sudo}

if [ "$(id -u)" -eq 0 ]
then
    echo "Do not run this script as root, run it as the owner of the"
    echo "checked out pgrpms git tree."
    exit 1
fi

if ! [ -e rpm/redhat/common/Makefile.global ]
then
    echo "rpm/redhat/common/Makefile.global not found"
    echo "Run from the root of the pgrpms directory"
    echo "(cwd is now $(pwd))"
    exit 1
fi

if ! test -O "."
then
    echo "$(pwd) is now owned by current user, run as user who owns it"
    exit 1
fi

set -e -u

if [ -n "$(which getenforce 2>/dev/null)" ]
then
    if [ "$(getenforce)" = "Enforcing" ]; then
	echo "-------------------------------------------------------"
	echo "WARNING: SELinux is in enforcing mode and may interfere"
	echo "with Docker bind mounts unless you relabel the tree."
	echo
	echo "Consider running 'setenforce 0' for the build then"
	echo "re-enabling SELinux with 'setenforce 1' afterwards."
	echo "-------------------------------------------------------"
    else
	echo "SELinux detected: $(getenforce)";
    fi
fi

sudo docker build -t build_postgis25_el6 \
    --build-arg PGRPMS_UID=$(id -u) --build-arg PGRPMS_GID=$(id -g) \
    --build-arg PGRPMS_USER=$(id -un) --build-arg PGRPMS_GROUP=$(id -gn) \
    build_postgis25_el6

sudo docker rm buildit >&/dev/null || true

sudo docker run --rm -v `pwd`:/pgrpms -it --name buildit \
    build_postgis25_el6:latest

find rpm/redhat/ -name \*.rpm
