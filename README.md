# pewmulator
And emulator for running PewPew games on desktop computers

To use it clone this repository, install the dependencies from the `requirements.txt` and work in the directory.
```
git clone https://github.com/pewpew-game/pew-pygame.git
cd pew-pygame
python -m pip install -r requirements.txt
```

Typically you want to start with a `code.py` that you can later copy to your hardware.

The keys of the PewPew can be emulated by the arrow keys and `x` and `z`.

The emulator does not support brightness.

You can change the display size by setting the `PEWPEW_SCALE` environment variable to an integer according to your screen resolution. If you want 4 times the initial size, set it to 4.

If you want to have the autoreload-on-save functionality of the 
physical device you can run `autoloader.py`. It will watch the file 
`code.py` in the current folder and restart the process if the file 
is saved. `autoloader.py` will accept a filename as a  
command-line-argument, in case you want to watch and execute some  
other file.
