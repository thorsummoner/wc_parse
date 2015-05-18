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

- [x] Read wc files
- [ ] Write wc files
- [ ] Implement JSON module like interface
- [ ] Unittests
- [ ] Cleanup example WC files
- [ ] Move TODO into README

