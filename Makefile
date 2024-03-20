ARGS=--movie_duration 200 --loop 200 pattern/puffer_train.life

samples: sample/sharpness5.gif sample/sharpness4.gif sample/sharpness3.gif sample/sharpness2.gif sample/sharpness1.gif

sample/sharpness1.gif:
	python3 life.py --sharpness 1 --movie_file sample/sharpness1.gif $(ARGS)
sample/sharpness2.gif:
	python3 life.py --sharpness 2 --movie_file sample/sharpness2.gif $(ARGS)
sample/sharpness3.gif:
	python3 life.py --sharpness 3 --movie_file sample/sharpness3.gif $(ARGS)
sample/sharpness4.gif:
	python3 life.py --sharpness 4 --movie_file sample/sharpness4.gif $(ARGS)
sample/sharpness5.gif:
	python3 life.py --sharpness 5 --movie_file sample/sharpness5.gif $(ARGS)
