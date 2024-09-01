# PayCoreLib
PayCoreLib is built using [Core-Lib](https://github.com/shay-te/core-lib).

## Example

```python
import hydra
from track_core_lib import TrackCoreLib

hydra.core.global_hydra.GlobalHydra.instance().clear()
hydra.initialize(config_path='../../track_core_lib/config')

# Create a new PayCoreLib using hydra (https://hydra.cc/docs/next/advanced/compose_api/) config
track_core_lib = TrackCoreLib(hydra.compose('track_core_lib.yaml'))
```

## License
Core-Lib in licenced under [MIT](https://github.com/shay-te/core-lib/blob/master/LICENSE)
