#!/usr/bin/env bash


vlc -f "$1""$(ls "$1"| grep -E "[^0-9]($2)[^0-9]")"