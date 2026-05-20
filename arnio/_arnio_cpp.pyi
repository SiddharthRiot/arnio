from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, overload
import numpy as np

__all__ = [
    "DType",
    "Column",
    "Frame",
    "CsvConfig",
    "CsvReader",
    "CsvChunkReader",
    "CsvWriteConfig",
    "CsvWriter",
    "cast_types",
    "clip_numeric",
    "safe_divide_columns",
    "drop_duplicates",
    "drop_nulls",
    "fill_nulls",
    "normalize_case",
    "rename_columns",
    "strip_whitespace",
]


class DType:
    STRING: "DType"
    INT64: "DType"
    FLOAT64: "DType"
    BOOL: "DType"
    NULL_TYPE: "DType"


class Column:
    def __init__(self, name: str, dtype: DType) -> None: ...

    def name(self) -> str: ...

    def dtype(self) -> DType: ...

    def size(self) -> int: ...

    def is_null(self, idx: int) -> bool: ...

    def memory_usage(self) -> int: ...

    def push_null(self) -> None: ...

    def push_back(self, value: Any) -> None: ...

    def at(self, idx: int) -> Any: ...

    def to_numpy_float(self) -> np.ndarray: ...

    def to_numpy_int(self) -> np.ndarray: ...

    def to_numpy_bool(self) -> np.ndarray: ...

    def to_python_list(self) -> list: ...

    def get_null_mask(self) -> np.ndarray: ...

    def data(self) -> Any: ...

    def null_mask(self) -> List[bool]: ...

    def clone(self) -> "Column": ...


class Frame:
    def __init__(self) -> None: ...

    def shape(self) -> Tuple[int, int]: ...

    def num_rows(self) -> int: ...

    def num_cols(self) -> int: ...

    def column_names(self) -> List[str]: ...

    def dtypes(self) -> Dict[str, DType]: ...

    def memory_usage(self) -> int: ...

    def has_column(self, name: str) -> bool: ...

    def column_by_index(self, idx: int) -> Column: ...

    def column_by_name(self, name: str) -> Column: ...

    def add_column(self, col: Column) -> None: ...

    def clone(self) -> "Frame": ...

    @staticmethod
    @overload
    def from_dict(cols: Mapping[str, Sequence[Any]]) -> "Frame": ...

    @staticmethod
    @overload
    def from_dict(
        cols: Mapping[str, Sequence[Any]],
        dtype_hints: Mapping[str, DType],
    ) -> "Frame": ...


class CsvConfig:
    delimiter: str
    has_header: bool
    encoding: str
    trim_headers: bool
    thousands_separator: Optional[str]
    mode: str
    null_values: Optional[list[str]]
    usecols: Optional[list[str]]
    nrows: Optional[int]
    skip_rows: int
    sample_size: Optional[int]

    def __init__(self, **kwargs: Any) -> None: ...


class CsvChunkReader:
    def __init__(self, config: CsvConfig) -> None: ...

    def open(self, path: str) -> None: ...

    def next_chunk(self, chunk_size: int) -> Optional[Frame]: ...

    def close(self) -> None: ...


class CsvReader:
    def __init__(self, config: CsvConfig) -> None: ...

    def read(self, path: str) -> Frame: ...

    def scan_schema(self, path: str) -> Dict[str, str]: ...


class CsvWriteConfig:
    delimiter: str
    write_header: bool
    line_terminator: str

    def __init__(self, **kwargs: Any) -> None: ...


class CsvWriter:
    def __init__(self, config: CsvWriteConfig) -> None: ...

    # C++ writer expects (frame, path)
    def write(self, frame: Frame, path: str) -> None: ...


def cast_types(frame: Frame, mapping: Mapping[str, str], coerce: bool) -> Frame: ...


def clip_numeric(
    frame: Frame,
    *,
    lower: Optional[float] = None,
    upper: Optional[float] = None,
    subset: Optional[Sequence[str]] = None,
) -> Frame: ...


def safe_divide_columns(
    frame: Frame,
    numerator: str,
    denominator: str,
    output_column: str,
    fill_value: float = 0.0,
) -> Frame: ...


def drop_duplicates(frame: Frame, subset: Optional[Sequence[str]] = None, keep: str = "first") -> Frame: ...


def drop_nulls(frame: Frame, subset: Optional[Sequence[str]] = None) -> Frame: ...


def fill_nulls(frame: Frame, value: Any, subset: Optional[Sequence[str]] = None) -> Frame: ...


def normalize_case(frame: Frame, *, subset: Optional[Sequence[str]] = None, case_type: str = "lower") -> Frame: ...


def rename_columns(frame: Frame, mapping: Mapping[str, str]) -> Frame: ...


def strip_whitespace(frame: Frame, *, subset: Optional[Sequence[str]] = None) -> Frame: ...

def combine_columns(frame: Frame, subset: Sequence[str], separator: str, output_column: str) -> Frame: ...
