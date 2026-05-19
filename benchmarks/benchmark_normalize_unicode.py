"""
Benchmark: normalize_unicode native ArFrame path vs old pandas roundtrip.

Run with:
    python benchmarks/benchmark_normalize_unicode.py

The native path (current implementation) should be measurably faster because
it avoids:
  1. A full to_pandas() conversion (ArFrame - DataFrame).
  2. A full .copy() of the DataFrame.
  3. A per-cell Python isinstance() check inside .apply().
  4. A full from_pandas() conversion back (DataFrame - ArFrame).
"""

from __future__ import annotations

import timeit
import unicodedata

import pandas as pd

import arnio as ar
import arnio._arnio_cpp as _cpp

N_ROWS = 100_000
_DIRTY = "cafe\u0301"  # NFD precomposed - needs NFC normalisation

df_base = pd.DataFrame(
    {
        "text": [_DIRTY] * N_ROWS,
        "name": [_DIRTY] * N_ROWS,
        "score": list(range(N_ROWS)),     # numeric column - must be skipped
    }
)
frame_base = ar.from_pandas(df_base)

def _old_normalize_unicode(frame: ar.ArFrame, form: str = "NFC") -> ar.ArFrame:
    """Replicates the original slow implementation for benchmarking."""
    from arnio.convert import from_pandas, to_pandas

    df = to_pandas(frame).copy()
    columns = df.select_dtypes(include=["object", "string"]).columns
    for col in columns:
        df[col] = df[col].apply(
            lambda x: unicodedata.normalize(form, x) if isinstance(x, str) else x
        )
    return from_pandas(df)


REPEATS = 5
NUMBER = 3


def bench(fn, label: str) -> float:
    times = timeit.repeat(fn, repeat=REPEATS, number=NUMBER)
    best = min(times) / NUMBER
    print(f"  {label:<40s}  best={best * 1000:.1f} ms  ({REPEATS}×{NUMBER} runs)")
    return best


if __name__ == "__main__":
    print(f"\nnormalize_unicode benchmark   {N_ROWS:,} rows, 2 string cols + 1 int col\n")

    t_old = bench(
        lambda: _old_normalize_unicode(frame_base, form="NFC"),
        "old (pandas roundtrip)",
    )
    t_new = bench(
        lambda: ar.normalize_unicode(frame_base, form="NFC"),
        "new (native ArFrame path)",
    )

    ratio = t_old / t_new
    direction = "faster" if ratio > 1 else "slower"
    print(f"\n  Speedup: {ratio:.2f}× {direction}  (new vs old)\n")

    # Correctness check
    old_df = ar.to_pandas(_old_normalize_unicode(frame_base))
    new_df = ar.to_pandas(ar.normalize_unicode(frame_base))
    assert old_df["text"].tolist() == new_df["text"].tolist(), "Output mismatch!"
    assert old_df["name"].tolist() == new_df["name"].tolist(), "Output mismatch!"
    assert old_df["score"].tolist() == new_df["score"].tolist(), "Numeric col mismatch!"
    print("  Correctness: PASS (outputs match)\n")