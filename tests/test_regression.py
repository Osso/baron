import pytest

from baron import (dumps,
                   parse)


def test_regression_trailing_comment_after_colon():
    assert parse("def a(): # pouf\n    pass")


def test_regression_trailing_comment_after_colon_no_space():
    assert parse("def a():# pouf\n    pass")


def test_regression_trailing_comment_after_colon_dump():
    code = "def a(): # pouf\n    pass\n"
    assert dumps(parse(code)) == code


def test_regression_trailing_comment_after_colon_no_space_dump():
    code = "def a():# pouf\n    pass\n"
    assert dumps(parse(code)) == code


def test_comment_in_middle_of_ifelseblock():
    code = 'if a:\n    pass\n# comment\nelse:\n    pass\n'
    assert dumps(parse(code)) == code


def test_comment_in_middle_of_try():
    code = 'try:\n    pass\n# comment\nexcept:\n    pass\n'
    assert dumps(parse(code)) == code


def test_comment_before_if():
    code = """
if cond:
    pass

# comment
if cond:
    pass
"""
    assert dumps(parse(code)) == code


def test_comment_before_while():
    code = """
while cond:
    pass

# comment
while cond:
    pass
"""
    assert dumps(parse(code)) == code


def test_comment_before_for():
    code = """
for var in iter:
    pass

# comment
for var in iter:
    pass
"""
    assert dumps(parse(code)) == code


def test_comment_before_try():
    code = """
try:
    pass
except:
    pass

# comment
try:
    pass
except:
    pass
"""
    assert dumps(parse(code)) == code


def test_comment_after_try_else():
    code = """
try:
    pass
except:
    pass
else:
    pass
# comment
call()
"""
    assert dumps(parse(code)) == code


def test_elif_with_empty_lines():
    code = """
if cond:
    pass

# ******************
# comment
# ******************

elif cond:
    pass

# ****************
# comment
# ****************

else:
    pass
"""
    assert dumps(parse(code)) == code
