FROM docker.io/node:16 as build-frontend
WORKDIR /app/src
ADD src/mafiasi_link_shortener/frontend/mafiasi_link_shortener/package.json src/mafiasi_link_shortener/frontend/mafiasi_link_shortener/package-lock.json /app/src/
RUN npm ci
ADD src/mafiasi_link_shortener/frontend/mafiasi_link_shortener/ /app/src/
RUN npm run build



FROM docker.io/python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt-get install -y --no-install-recommends git && \
    pip3 install --no-cache-dir pipenv gunicorn

ARG UID=10001
ARG GID=10001
ENV TINI_VERSION=v0.19.0

# create app-user so as to not run as root
WORKDIR /app/src
RUN groupadd -g $GID app-group && \
    useradd --home-dir /app -g $GID -u $UID app-user

# use tini as entrypoint for better signal handling
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/local/bin/
ADD docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/*

# install app dependencies
ADD Pipfile Pipfile.lock /app/src/
RUN pipenv install --system --deploy

# cleanup
RUN pip3 uninstall --no-cache-dir -y pipenv && \
    apt-get purge -y git && \
    apt-get autoremove -y && \
    apt-get clean -y

# install app source
ADD src /app/src/src/
COPY --from=build-frontend /app/src/dist/ /app/src/src/mafiasi_link_shortener/frontend/mafiasi_link_shortener/dist/
ENV PYTHONPATH=$PYTHONPATH:/app/src/src/
RUN mkdir /app/static
RUN chown $UID:$GID -R /app &&\
    chmod u=rX,g=rX,o=rX -R /app/src &&\
    chmod u=rwX,g=rwX,o=r -R /app/static &&\
    chmod u+w,g+w -R /app/src/src/mafiasi_link_shortener/frontend/mafiasi_link_shortener/dist/

# configure docker-specifc application settings
ENV SHORTLINK_STATIC_ROOT=/app/static

# configure image metadata
USER $UID:$GID
ENTRYPOINT ["/usr/local/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=4", "--threads=4", "mafiasi_link_shortener.wsgi:application"]
EXPOSE 8000/tcp
