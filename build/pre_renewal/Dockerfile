# rAthena server image: pre-renewal, client 2021-11-03.
# Compiles inside Docker, keeps only the servers + conf/db/npc in the final image.
# Built by duds_server/build/compose.yml (context = repo root). Configs are mounted at run time.

FROM alpine:3.23 AS build
RUN apk add --no-cache cmake make gcc g++ zlib-dev mariadb-dev linux-headers bash
WORKDIR /rathena
COPY . .
ARG CONFIGURE="--enable-prere=yes --enable-packetver=20211103"
RUN ./configure $CONFIGURE && make clean && make -j"$(nproc)" server

FROM alpine:3.23
RUN apk add --no-cache libstdc++ libgcc zlib mariadb-connector-c netcat-openbsd \
 && adduser -D -u 1000 rathena
WORKDIR /rathena
COPY --from=build /rathena/login-server /rathena/char-server /rathena/map-server /rathena/web-server ./
COPY --from=build /rathena/conf ./conf
COPY --from=build /rathena/db ./db
COPY --from=build /rathena/npc ./npc
COPY --from=build /rathena/sql-files ./sql-files
RUN mkdir -p log save && chown -R rathena:rathena /rathena
ARG CONFIGURE="--enable-prere=yes --enable-packetver=20211103"
LABEL rathena.configure="$CONFIGURE"
USER rathena
