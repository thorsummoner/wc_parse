# wc_parse
Parse Source SDK `.wc` files.


Command line example:
```
./wc_parse.py CmdSeq.wc
```


Api Example:
```
import wc_parse
from pprint import pprint

hammer_conf = wc_parse.wc_parse('./CmdSq.wc')

pprint(hammer_conf)
```

# TODO
See [./TODO.md](./TODO.md)
