#!/usr/bin/env bash


cd "$1"
vlc $3 -f "$(ls | head -n$2 | tail -n1)"