#!/usr/bin/env bash


cd $1
vlc $3 -f "$(ls | grep -E "[^0-9]($2)[^0-9]")"