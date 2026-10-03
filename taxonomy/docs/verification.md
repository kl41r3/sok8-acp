# Verification of this local candidate

The retained private comparison matched all 5241 current source-row selections/bases, all 5208 identifier selections, the exact 1301 included-key set, each source count and the current flow's numerical claims. Every staged aggregate input matches the upstream delivery manifest. All 5242 retained immutable snapshots (1385292629 bytes) and 20 staged aggregate files passed SHA-256 and byte-size checks; no primary source was changed.

The documented workflow was tested in a new temporary copy with only `public/`, using Python 3.14.7 with `-I -S` (isolated mode, no site packages):

```sh
python3 -I -S -B code/reproduce.py --check-only
python3 -I -S -B code/reproduce.py --output outputs/run
```

Both commands succeeded, and five regenerated outputs matched `expected/` byte-for-byte. Reusing the output directory, appending a byte to throwaway records.csv, adding an unmanifested file, and replacing the input directory with a symlink were correctly rejected. Bytecode generation was disabled. Clean-copy private receipts retain commands, stdout/stderr, exit codes and timings. No new scientific review, search or experiment ran.

The package checksums bind only this staged public byte set. The original query counts, processing receipt and gate scope text are frozen projections whose source hashes are in data/provenance.json; they are not recomputed native query/review experiments. No quoted primary text, abstracts, screenshots, internal conversations or private paths are included. The public tree passed field-whitelist, text/file-type and common private-path/credential/internal-message scans; the private local receipt lists their exact scope. This is not anonymous-review or Git-history verification.

Publication has not happened. Redistribution/licensing decisions for the derived dataset and newly staged code remain unresolved. Scientific, coverage and work/version acceptance remains Partial. See licensing-and-release-readiness.md and method-boundaries.md before treating any result as publication ready.
