# Build status-go in a Go builder container
FROM golang:1.18-alpine as builder

RUN apk add --no-cache make gcc g++ musl-dev linux-headers

ARG build_tags
ARG build_flags

RUN mkdir -p /go/src/github.com/status-im/status-go
WORKDIR /go/src/github.com/status-im/status-go
ADD . .
# RUN cd cmd/spiff-workflow && go build --mod=vendor
RUN cd cmd/spiff-workflow && go build --mod=vendor

# Copy the binary to the second image
FROM alpine:latest

RUN apk add --no-cache ca-certificates bash libgcc libstdc++
RUN mkdir -p /static/keys

COPY --from=builder /go/src/github.com/status-im/status-go/cmd/spiff-workflow/spiff-workflow /usr/local/bin/

# 30304 is used for Discovery v5
EXPOSE 8080 8545 30303 30303/udp 30304/udp

# ENTRYPOINT ["/usr/local/bin/statusd"]
ENTRYPOINT ["/usr/local/bin/spiff-workflow"]
CMD ["--help"]
