# Browser client image: roBrowserLegacy (robrowser/ submodule) + its game file server and WebSocket proxy
# (roBrowserLegacy-RemoteClient-JS). No game files inside: they're mounted at run time (deploy/compose.yml "browser").
# Same steps as robrowser/Dockerfile.remoteclient, on Node 24: upstream's Node 20 is too old for both projects.
# Built by build/compose.yml (context = repo root).

FROM --platform=$BUILDPLATFORM node:24-slim AS build
WORKDIR /rb
COPY robrowser/package*.json ./
RUN npm install --no-audit --no-fund   # shortcut: upstream lockfile is out of sync (npm ci fails); build-time only, output is static JS
COPY robrowser/ .
COPY patches/robrowser/ /patches/
COPY build/browser/preloader.html /preloader.html
# our fixes on top of the pinned roBrowser (like patches/ for rAthena); a patch that no longer fits stops the build
# (git apply, not patch: some roBrowser files have Windows line endings, which git's diffs leave out)
RUN apt-get update -qq && apt-get install -y -qq git >/dev/null \
 && for p in /patches/*.patch; do git apply --ignore-whitespace --whitespace=nowarn "$p" || exit 1; done
RUN npm run build:all \
 && sed -i -e 's|<title>[^<]*</title>|<title>RagnaDuds</title>|' \
           -e 's|<link rel="icon"[^>]*>|<link rel="icon" href="/img/favicon.ico">|' dist/Web/*.html \
 && node -e 'const fs = require("fs"), p = "dist/Web/api.html", r = /<div id="ro-preloader">[\s\S]*?<\/p>\s*<\/div>/; \
      let s = fs.readFileSync(p, "utf8"); if (!r.test(s)) process.exit(1); \
      fs.writeFileSync(p, s.replace(r, () => fs.readFileSync("/preloader.html", "utf8")))' \
 && grep -q 'rd-title' dist/Web/api.html   # our tab name, the site's icon, and our loading screen (build/browser/preloader.html)

FROM node:24-slim
RUN apt-get update -qq && apt-get install -y -qq git && rm -rf /var/lib/apt/lists/* \
 && groupadd -r robrowser && useradd -r -g robrowser -d /app robrowser
WORKDIR /app
ARG REMOTE_CLIENT_COMMIT=0dd3a3fa71733c0c88ac1beb117039174eb2a7b0
RUN git clone -q https://github.com/FranciscoWallison/roBrowserLegacy-RemoteClient-JS.git . \
 && git checkout -q "$REMOTE_CLIENT_COMMIT" && npm ci --ignore-scripts --omit=dev --no-audit --no-fund && rm -rf .git \
 && mkdir -p resources data logs \
 # shortcut: kRO 2026 GRFs start with "Event Horizon" instead of "Master of Magic" (same 0x300 format otherwise);
 # accept both until @chicowall/grf-loader / RemoteClient-JS support it upstream
 && sed -i 's/if(t!==\([A-Za-z]*\))throw new \([A-Za-z]*\)("INVALID_MAGIC"/if(t!==\1\&\&!t.startsWith("Event Horizon"))throw new \2("INVALID_MAGIC"/' node_modules/@chicowall/grf-loader/dist/index.js node_modules/@chicowall/grf-loader/dist/index.cjs \
 && sed -i 's/if (signature !== "Master of Magic")/if (signature !== "Master of Magic" \&\& !signature.startsWith("Event Horizon"))/' src/validators/startupValidator.js \
 && grep -q 'Event Horizon' node_modules/@chicowall/grf-loader/dist/index.js && grep -q 'Event Horizon' node_modules/@chicowall/grf-loader/dist/index.cjs \
 && grep -q 'Event Horizon' src/validators/startupValidator.js \
 # serve SystemEN/ too: roBrowser reads the English sign/town/quest tables from there
 && sed -i "s/const SERVABLE_ROOTS = \['data', 'bgm', 'system', 'ai'\];/const SERVABLE_ROOTS = ['data', 'bgm', 'system', 'systemen', 'ai'];/" src/controllers/clientController.js \
 && grep -q "'systemen'" src/controllers/clientController.js
COPY --from=build /rb/dist/Web /robrowser
RUN chown -R robrowser:robrowser /app /robrowser
ENV PORT=3338 NODE_ENV=production ENABLE_WSPROXY=true ENABLE_STATIC_SERVE=true ROBROWSER_PATH=/robrowser \
    CACHE_WARM_UP=false
EXPOSE 3338
USER robrowser
CMD ["npm", "run", "start:prod"]
