## How to use

1. Put conf.json to ~/.config/mathpixsnipper/ and add your Mathpix API keys. 
(You need Mathpix account for that)

2. $ python mathpixsnipper.py
3. select area
4. done. snipper will return latex code to clipboard in case of success
and error_info in case of any problem.
5. better to wrap it in a bash script, like this: 

```bash
#!/bin/bash
cd /path/to/mathpixsnipper
python mathpixsnipper.py
```
