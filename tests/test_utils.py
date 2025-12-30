import sys
from itertools import zip_longest  # noqa: F401 - re-exported for other test files

from baron.baron import parse as baron_parse
from baron.dumper import dumps
from baron.grammator import generate_parse

parse = generate_parse(False)


def parse_simple(tokens, result):
    if not tokens or tokens[-1][0] != "ENDL":
        tokens += [("ENDL", "\n")]
    assert parse(tokens + [("ENDMARKER", ""), None]) == (
        result + [{"type": "endl", "value": "\n", "formatting": [], "indent": ""}]
    )


def parse_multi(tokens, result):
    assert parse(tokens + [("ENDMARKER", ""), None]) == result


def check_dumps(source_code):
    try:
        with open("/tmp/c", "w") as f:
            f.write(source_code)
        with open("/tmp/d", "w") as f:
            f.write(dumps(baron_parse(source_code)))
    except Exception as e:
        import json
        import traceback

        traceback.print_exc(file=sys.stdout)
        sys.stdout.write(f"Warning: couldn't write dumps output to debug file, exception: {e}\n\n")
        sys.stdout.write(f"Tree: {json.dumps(baron_parse(source_code), indent=4)}" + "\n")

    assert dumps(baron_parse(source_code), strict=True) == source_code
