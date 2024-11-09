# Atari 8-bit source control experiments

This is an experimental project to test my Atari 8-bit source control setup. The text files I use for testing are mostly [Action!](https://en.wikipedia.org/wiki/Action!_(programming_language)) source files that I've been playing around with

## Current setup

I do developtment on an Atari 600XL with a FujiNet connected to my WiFi and a TNFS server running on my PC. I save my projects to an ATR image on my PC. 

I've also written some Python scripts that can translate between [ATASCII](https://en.wikipedia.org/wiki/ATASCII) and UTF-8 text files. The translation is based on Rebecca Bettencourt's [ATASCII to Unicode Mapping](https://www.kreativekorp.com/charset/map/atascii/), but since there aren't Unicode representations for most of the reverse video ATASCII characters, I use a backtick as an escape for reverse characters.

It's now mostly working, but YMMV.

## Usage

### Commit & push from the ATARI

1. From the ATARI:
   1. Save the source files to an ATR image mounted from the TNFS server
   1. When you want to commit to git, update a special text file called `COMMIT.MSG` with the desired commit message
1. On the PC, run `auto_sync`, which does the following:
    1. When the ATR image changes, automatically extract the contents to `./atascii/` using `lsatr`. See https://github.com/dmsc/mkatr.
    1. When the `./atascii/` changes, automatically translate the text files to UTF-8 and save them to `./utf8/`
    1. When the contents of `./utf8/COMMIT.MSG` changes do a `git commit` with the commit message from the file

### Pull from the ATARI

TBD