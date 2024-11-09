# Atari 8-bit source control experiments

This is an experimental project to test my Atari 8-bit source control setup. The text files I use for testing are mostly [Action!](https://en.wikipedia.org/wiki/Action!_(programming_language)) source files that I've been playing around with

## Current setup

I do developtment on an Atari 600XL with a FujiNet connected to my WiFi and a TNFS server running on my PC. I save my projects to an ATR image on my PC. 

I've also written some Python scripts (not committed yet) that translates between ATASCII and UTF-8.

Most of the steps mentioned below are working, but it's not automated yet.

## Goals

Eventually I want a setup that will allow me to do source control from my ATARI.

### Commit & push from the ATARI

1. From the ATARI:
   1. Save the source files to an ATR image mounted from the TNFS server
   1. When you want to commit to git, update a special text file called `COMMIT.MSG` with the desired commit message
1. On the PC:
    1. When the ATR image changes, automatically extract the contents to `./atascii/` using `lsatr`. See https://github.com/dmsc/mkatr.
    1. When the `./atascii/` changes, automatically translate the text files to UTF-8 and save them to `./utf8/`
    1. When the contents of `./utf8/COMMIT.MSG` changes do a `git commit` with the commit message from the file

### Pull from the ATARI

TBD