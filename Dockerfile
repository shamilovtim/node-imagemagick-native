FROM dockerfile/nodejs
# https://registry.hub.docker.com/u/dockerfile/nodejs/

RUN apt-get update
RUN apt-get -y install \
 git \
 imagemagick \
 libmagick++-dev \
 node-gyp

RUN cd /data && git clone https://github.com/mash/node-imagemagick-native.git
WORKDIR /data/node-imagemagick-native

RUN npm install --unsafe-perm

CMD ["bash"]
