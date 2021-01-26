FROM docker.io/python:3.9-slim
RUN apt-get update
RUN apt-get install -y --no-install-recommends git
RUN pip3 install --no-cache-dir pipenv

ARG UID=10001
ARG GID=10001
ENV TINI_VERSION=v0.19.0

# create app-user so as to not run as root
WORKDIR /app/src
RUN groupadd -g $GID app-group
RUN useradd --home-dir /app -g $GID -u $UID app-user

# use tini as entrypoint for better signal handling
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/local/bin/
ADD docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/*

# install app dependencies
ADD Pipfile Pipfile.lock /app/src/
RUN pipenv install --system --deploy

# cleanup
RUN pip3 uninstall --no-cache-dir -y pipenv
RUN apt-get purge -y git
RUN apt-get autoremove -y
RUN apt-get clean -y

# install app source
ADD src /app/src/src/
ENV PYTHONPATH=$PYTHONPATH:/app/src/src/
RUN mkdir /app/static
RUN chown $UID:$GID -R /app
RUN chmod u=rX,g=rX,o=r -R /app/src
RUN chmod u=rwX,g=rwX,o=r -R /app/static

# configure docker-specifc application settings
ENV DJANGO_CONFIGURATION=Prod
ENV DJANGO_STATIC_ROOT=/app/static

# configure image metadata
USER $UID:$GID
ENTRYPOINT ["/usr/local/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]
CMD ["runserver", "0.0.0.0:8000"]
EXPOSE 8000/tcp
