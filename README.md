# depviz — pip dependency graph visualizer

Tool that builds and visualizes the dependency graph of a pip
package **without** using `pip` or third-party dependency libraries.

## 1. General description

`depviz` fetches package metadata directly from PyPI, extracts
`Requires-Dist` entries, traverses the transitive graph with a
non-recursive BFS, detects cycles and renders a D2 diagram to PNG.

## 2. Functions and settings

| Option      | Meaning                                                      |
|-------------|--------------------------------------------------------------|
| `--package` | Name of the analysed package                                 |
| `--repo`    | PyPI URL (online mode) or path to test graph file (test mode)|
| `--mode`    | `online` — query PyPI; `test` — local description file       |
| `--output`  | PNG file name (`*.png`)                                      |
| `--exclude` | Substring; packages containing it are skipped                |

Test graph format:

```
A: B C
B: D
```

## 3. Build and tests

```bash
make install
make test          # pytest
make run-demo      # example on the test graph
```

Requirements: Python 3.10+, `d2` binary (https://d2lang.com).

## 4. Usage examples

Online mode (real PyPI package):

```bash
python -m src.main \
  --package=requests \
  --repo=https://pypi.org/pypi \
  --mode=online \
  --output=out/requests.png
```

Test mode with filter:

```bash
python -m src.main \
  --package=A \
  --repo=tests/fixtures/test_repo.txt \
  --mode=test \
  --output=out/A.png \
  --exclude=E
```

## Notes on comparison with `pip`

`pip` resolves concrete versions and honours environment markers and
extras; `depviz` works with package *names* only. Therefore the load
order may differ: `pip` order is an implementation detail of the
resolver and is not required to be topological.
