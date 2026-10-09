# RagnaDuds portal (Go): account requests, website login, password set/reset, admin approvals.
# One static binary (pure-Go SQLite, no cgo) on a tiny Alpine; data in /data/portal.db (volume).
FROM --platform=$BUILDPLATFORM golang:1.26-alpine AS build
ARG TARGETOS TARGETARCH
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -trimpath -ldflags="-s -w" -o /portal .

FROM alpine:3.23
RUN apk add --no-cache ca-certificates   # SMTP over TLS
COPY --from=build /portal /usr/local/bin/portal
ENV PORTAL_DB=/data/portal.db LISTEN=:8000
EXPOSE 8000
ENTRYPOINT ["portal"]
CMD ["serve"]
