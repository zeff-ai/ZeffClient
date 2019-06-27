FROM python:3

MAINTAINER "Lance Finn Helsten" <lanhel@flyingtitans.com>

WORKDIR /usr/local/src/zeffclient

COPY . /usr/local/src/zeffclient

RUN make install && \
 rm -f "/usr/local/lib/python3.7/site-packages/ZeffClient.egg-link" && \
 rm -rf "/usr/local/src/zeffclient"

# ENV EGG_LINK_FILE="/usr/local/lib/python3.7/site-packages/ZeffClient.egg-link"
# ENV CLONEZEFFCLIENT="/codefresh/volume/ZeffClient"
# RUN if [ -f "${EGG_LINK_FILE}" ]; then \
        # rm "${EGG_LINK_FILE}"; \
	    # echo ${CLONEZEFFCLIENT} > "${EGG_LINK_FILE}"; \
	    # echo ".%" >> "${EGG_LINK_FILE}"; \
    # fi

CMD [ "bash" ]

