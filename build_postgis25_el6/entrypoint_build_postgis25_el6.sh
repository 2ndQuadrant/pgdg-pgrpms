# Some of the prep used:
#
#   git checkout caf2197d48ac8ee2fcb18a3ceaf3f9162c086aae^1 -- rpm/redhat/master/proj49/{master,EL-6}
#   cp -a rpm/redhat/11/geos36/EL-6 rpm/redhat/12/geos36/EL-6
#   cp -a rpm/redhat/11/postgis25/EL-6 rpm/redhat/12/postgis25/EL-6

pushd rpm/redhat/master/proj49/EL-6/
yum-builddep -y *.spec && make NO_GIT=1 rpm12
yum install ./x86_64/proj49-4.9.3-3.rhel6.1.x86_64.rpm ./x86_64/proj49-devel-4.9.3-3.rhel6.1.x86_64.rpm
popd

pushd rpm/redhat/12/geos36/EL-6
yum-builddep -y *.spec && make NO_GIT=1 rpm12
yum install ./x86_64/geos36-3.6.3-1.rhel6.1.x86_64.rpm ./x86_64/geos36-devel-3.6.3-1.rhel6.1.x86_64.rpm
popd

pushd rpm/redhat/12/postgis25/EL-6
# Requires patched spec file to change required geos and proj, disable SFCGAL and change gdaldir to /usr
yum-builddep -y *.spec && make NO_GIT=1 rpm12
popd
