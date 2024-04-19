# lc-wiki-graph

## License

DO WHAT THE FUCK YOU WANT TO.

## General settings

All the scripts use the result from [AssetRipper](https://github.com/AssetRipper/AssetRipper).

Simply extract all the files from `Lethal Company_Data` to a folder, for example `X:/Game Extract`.

Then, create a `.env` file. Specify the `GAME_EXTRACT_ROOT` variable to the path of the extracted files. For example,

```
GAME_EXTRACT_ROOT=X:/Game Extract
```

Finally, ensure there are folders named `outputs` and `caches` in the project root directory. You're now good to go.

## Radar pip sizes graph

Simply run `radarPipSizes.py`. The output is located at `outputs/radarPipSizes.png`.
