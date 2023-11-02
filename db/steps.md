To load the JSON with apoc, you needed to setup conf/apoc.conf with
```
apoc.import.file.enabled=true
```

The desktop client keeps the db files under:
```
~/.config/Neo4j\ Desktop/Application/relate-data/dbmss/$ID
```

You also need to move the Clara json file into the`imports`
folder under the above path.
