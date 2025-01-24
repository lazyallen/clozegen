.PHONY: all install clean

all:
	python main.py

install:
	pip install -r requirements.txt

clean:
	rm -rf csv/*.csv
	rm -rf tts/*.mp3