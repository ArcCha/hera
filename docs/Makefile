all: build/index.html

SLATE:=../deps/slate

deps:
	cd deps/slate; bundle install

build:
	mkdir -p build

pre: build
	convert $(shell pwd)/../logo/icon.png -border 40 -resize 230 $(SLATE)/source/images/logo.png
	ln -sf $(shell pwd)/index.md $(SLATE)/source/index.md

serve: pre
	cd $(SLATE); bundle exec middleman server

build/index.html: pre index.md
	cd $(SLATE); rake build
	rsync --delete -a $(SLATE)/build build

upload: build/index.html
	cd build; rsync -a . "zlmch@users:WWW/hera"

.PHONY: deps pre serve
