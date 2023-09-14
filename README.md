# pngcrush-brute-mt
This script lets you utilize an arbitrary number of threads to brute force PNG compression of an image.  
By default, it will make a new, recompressed version of `image.png` called `image_brute.png`.

This requires a pngcrush executable for your system. Edit brute-mt.py to point to this executable.

```
usage: brute-mt.py [-h] -i INPUT -t THREADS [--overwrite]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        PNG input filename
  -t THREADS, --threads THREADS
                        # of pngcrush instances
  --overwrite           Overwrite original PNG
```

If you want to exceed the compression possible with brute force, you can look into [quantizing your PNG](https://pngquant.org/) before running `brute-mt.py`.
