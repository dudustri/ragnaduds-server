# Browser client image: roBrowserLegacy (robrowser/ submodule) + its game file server and WebSocket proxy
# (roBrowserLegacy-RemoteClient-JS). No game files inside: they're mounted at run time (deploy/compose.yml "browser").
# Same steps as robrowser/Dockerfile.remoteclient, on Node 24: upstream's Node 20 is too old for both projects.
# Built by build/compose.yml (context = repo root).

FROM --platform=$BUILDPLATFORM node:24-slim AS build
WORKDIR /rb
COPY robrowser/package*.json ./
RUN npm install --no-audit --no-fund   # shortcut: upstream lockfile is out of sync (npm ci fails); build-time only, output is static JS
COPY robrowser/ .
RUN npm run build:all

FROM node:24-slim
RUN apt-get update -qq && apt-get install -y -qq git && rm -rf /var/lib/apt/lists/* \
 && groupadd -r robrowser && useradd -r -g robrowser -d /app robrowser
WORKDIR /app
ARG REMOTE_CLIENT_COMMIT=0dd3a3fa71733c0c88ac1beb117039174eb2a7b0
RUN git clone -q https://github.com/FranciscoWallison/roBrowserLegacy-RemoteClient-JS.git . \
 && git checkout -q "$REMOTE_CLIENT_COMMIT" && npm ci --ignore-scripts --omit=dev --no-audit --no-fund && rm -rf .git \
 && mkdir -p resources data logs
COPY --from=build /rb/dist/Web /robrowser
RUN chown -R robrowser:robrowser /app /robrowser
ENV PORT=3338 NODE_ENV=production ENABLE_WSPROXY=true ENABLE_STATIC_SERVE=true ROBROWSER_PATH=/robrowser \
    CACHE_WARM_UP=false
EXPOSE 3338
USER robrowser
CMD ["npm", "run", "start:prod"]
