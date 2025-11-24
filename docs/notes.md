# IRIS#1 - Notes & TODOs

Free-form notes, questions, and TODOs for the project.

## Questions / Ideas

- [ ] How to handle different lighting conditions in iris detection?
- [ ] Should we normalize iris size before FFT?
- [ ] What's the best way to connect frontend to backend? (JSON polling? WebSocket?)
- [ ] Should Digital Iris patterns be more abstract or more representational?

## TODOs

### Backend
- [ ] Add real pupil detection (Hough circles or deep learning?)
- [ ] Improve feature extraction (more sophisticated statistics)
- [ ] Add error handling and logging
- [ ] Test with real camera photos

### Frontend
- [ ] Connect frontend to read latest latent code from `data/codes/`
- [ ] Improve Digital Iris rendering (more interesting patterns)
- [ ] Add sound effects for state transitions?
- [ ] Make UI more polished (better typography, animations)

### Integration
- [ ] Set up automatic pipeline (watch_folder.py → full processing)
- [ ] Test end-to-end flow with real photos
- [ ] Performance optimization if needed

## Reference Links

- p5.js documentation: https://p5js.org/reference/
- OpenCV Python: https://docs.opencv.org/
- NumPy FFT: https://numpy.org/doc/stable/reference/routines.fft.html

