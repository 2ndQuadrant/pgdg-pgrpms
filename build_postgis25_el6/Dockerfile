FROM centos:6

# usage: ./build_postgis25_el6/run_docker_build.sh

VOLUME /pgrpms

ADD epel-release-latest-6.noarch.rpm /root/
RUN yum -y clean all && \
    rpm -i /root/epel-release-latest-6.noarch.rpm && \
    yum -y check-update; ecode=$?; if [ $ecode != 0 && $ecode != 100 ]; then exit 1; fi; \
    yum -y install yum-utils git make gcc gcc-c++ rpmbuild fakeroot spectool

# from https://download.postgresql.org/pub/repos/yum/reporpms/EL-6-x86_64/pgdg-redhat-repo-latest.noarch.rpm
ADD pgdg-redhat-repo-latest.noarch.rpm /root/
RUN rpm -i /root/pgdg-redhat-repo-latest.noarch.rpm && \
    yum -y check-update; ecode=$?; if [ $ecode != 0 && $ecode != 100 ]; then exit 1; fi; \
    yum-builddep -y postgresql12

ARG PGRPMS_UID
ARG PGRPMS_GID
ARG PGRPMS_USER
ARG PGRPMS_GROUP
RUN groupadd -g ${PGRPMS_GID:?} ${PGRPMS_GROUP} && \
    useradd -u ${PGRPMS_UID:?} -g ${PGRPMS_GID:?} ${PGRPMS_USER:?}

ADD entrypoint_build_postgis25_el6.sh /entrypoint_build_postgis25_el6.sh
RUN chmod 0555 /entrypoint_build_postgis25_el6.sh

WORKDIR /pgrpms/rpm/redhat/12/postgis25/EL-6
RUN echo '%pgmajorversion 12' >> /root/.rpmmacros
CMD ["/bin/bash", "-c", "/entrypoint_build_postgis25_el6.sh"]
