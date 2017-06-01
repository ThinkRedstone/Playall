#!/usr/bin/env bash


cd "$1"
vlc -I qt --extraintf rc --rc-host=localhost:8080 $3 -f "$(ls | head -n$2 | tail -n1)"