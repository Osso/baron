# pylint: disable=unused-variable


def include_control_structures(pg):
    @pg.production("try_stmt : TRY COLON suite excepts")
    def try_excepts_stmt(pack):
        (try_, colon, suite, excepts) = pack
        return [{
            "type": "try",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
            "else": {},
            "finally": {},
            "excepts": excepts,
        }]

    @pg.production("try_stmt : TRY COLON suite excepts else_stmt")
    def try_excepts_else_stmt(pack):
        (try_, colon, suite, excepts, else_stmt) = pack
        return [{
            "type": "try",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
            "else": else_stmt,
            "finally": {},
            "excepts": excepts,
        }]

    @pg.production("try_stmt : TRY COLON suite excepts finally_stmt")
    def try_excepts_finally_stmt(pack):
        (try_, colon, suite, excepts, finally_stmt) = pack
        return [{
            "type": "try",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
            "else": {},
            "finally": finally_stmt,
            "excepts": excepts,
        }]

    @pg.production("try_stmt : TRY COLON suite excepts else_stmt finally_stmt")
    def try_excepts_else_finally_stmt(pack):
        (try_, colon, suite, excepts, else_stmt, finally_stmt) = pack
        return [{
            "type": "try",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
            "else": else_stmt,
            "finally": finally_stmt,
            "excepts": excepts,
        }]

    @pg.production("try_stmt : TRY COLON suite finally_stmt")
    def try_stmt(pack):
        (try_, colon, suite, finally_stmt) = pack
        return [{
            "type": "try",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
            "else": {},
            "finally": finally_stmt,
            "excepts": [],
        }]

    @pg.production("excepts : except_stmt excepts")
    def excepts(pack):
        (except_stmt, excepts_) = pack
        return except_stmt + excepts_

    @pg.production("excepts : except_stmt")
    def excepts_except_stmt(pack):
        (except_stmt,) = pack
        return except_stmt

    @pg.production("except_stmt : EXCEPT test AS test COLON suite")
    def except_as_stmt(pack):
        (except_, test, as_, test2, colon, suite) = pack
        return [{
            "type": "except",
            "first_formatting": except_.hidden_tokens_after,
            "second_formatting": as_.hidden_tokens_before,
            "third_formatting": as_.hidden_tokens_after,
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
            "delimiter": "as",
            "target": test2,
            "exception": test,
            "value": suite
        }]

    @pg.production("except_stmt : EXCEPT test COMMA test COLON suite")
    def except_comma_stmt(pack):
        (except_, test, comma, test2, colon, suite) = pack
        return [{
            "type": "except",
            "first_formatting": except_.hidden_tokens_after,
            "second_formatting": comma.hidden_tokens_before,
            "third_formatting": comma.hidden_tokens_after,
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
            "delimiter": ",",
            "target": test2,
            "exception": test,
            "value": suite
        }]

    @pg.production("except_stmt : EXCEPT COLON suite")
    def except_stmt_empty(pack):
        (except_, colon, suite) = pack
        return [{
            "type": "except",
            "first_formatting": except_.hidden_tokens_after,
            "second_formatting": [],
            "third_formatting": [],
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
            "delimiter": "",
            "target": {},
            "exception": {},
            "value": suite
        }]

    @pg.production("except_stmt : EXCEPT test COLON suite")
    def except_stmt(pack):
        (except_, test, colon, suite) = pack
        return [{
            "type": "except",
            "first_formatting": except_.hidden_tokens_after,
            "second_formatting": [],
            "third_formatting": [],
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
            "delimiter": "",
            "target": {},
            "exception": test,
            "value": suite
        }]

    # PEP 654 - Exception Groups (except*)
    @pg.production("except_stmt : EXCEPT STAR test AS test COLON suite")
    def except_star_as_stmt(pack):
        (except_, star, test, as_, test2, colon, suite) = pack
        return [{
            "type": "except_star",
            "first_formatting": except_.hidden_tokens_after,
            "second_formatting": star.hidden_tokens_after,
            "third_formatting": as_.hidden_tokens_before,
            "fourth_formatting": as_.hidden_tokens_after,
            "fifth_formatting": colon.hidden_tokens_before,
            "sixth_formatting": colon.hidden_tokens_after,
            "target": test2,
            "exception": test,
            "value": suite
        }]

    @pg.production("except_stmt : EXCEPT STAR test COLON suite")
    def except_star_stmt(pack):
        (except_, star, test, colon, suite) = pack
        return [{
            "type": "except_star",
            "first_formatting": except_.hidden_tokens_after,
            "second_formatting": star.hidden_tokens_after,
            "third_formatting": [],
            "fourth_formatting": [],
            "fifth_formatting": colon.hidden_tokens_before,
            "sixth_formatting": colon.hidden_tokens_after,
            "target": {},
            "exception": test,
            "value": suite
        }]

    @pg.production("finally_stmt : FINALLY COLON suite")
    def finally_stmt(pack):
        (finally_, colon, suite) = pack
        return {
            "type": "finally",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
        }

    @pg.production("else_stmt : ELSE COLON suite")
    def else_stmt(pack):
        (else_, colon, suite) = pack
        return {
            "type": "else",
            "value": suite,
            "first_formatting": else_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_after,
        }

    @pg.production("for_stmt : FOR exprlist IN testlist COLON suite")
    def for_stmt(pack,):
        (for_, exprlist, in_, testlist, colon, suite) = pack
        return [{
            "type": "for",
            "async": False,
            "async_formatting": [] + for_.hidden_tokens_before,
            "value": suite,
            "iterator": exprlist,
            "target": testlist,
            "else": {},
            "first_formatting": for_.hidden_tokens_after,
            "second_formatting": in_.hidden_tokens_before,
            "third_formatting": in_.hidden_tokens_after,
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
        }]

    @pg.production("for_stmt : FOR exprlist IN testlist COLON suite else_stmt")
    def for_else_stmt(pack,):
        (for_, exprlist, in_, testlist, colon, suite, else_stmt) = pack
        return [{
            "type": "for",
            "value": suite,
            "async": False,
            "async_formatting": [] + for_.hidden_tokens_before,
            "iterator": exprlist,
            "target": testlist,
            "else": else_stmt,
            "first_formatting": for_.hidden_tokens_after,
            "second_formatting": in_.hidden_tokens_before,
            "third_formatting": in_.hidden_tokens_after,
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
        }]

    @pg.production("while_stmt : WHILE test COLON suite")
    def while_stmt(pack):
        (while_, test, colon, suite) = pack
        return [{
            "type": "while",
            "value": suite,
            "test": test,
            "else": {},
            "first_formatting": while_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
        }]

    @pg.production("while_stmt : WHILE test COLON suite else_stmt")
    def while_stmt_else(pack):
        (while_, test, colon, suite, else_stmt) = pack
        return [{
            "type": "while",
            "value": suite,
            "test": test,
            "else": else_stmt,
            "first_formatting": while_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
        }]

    @pg.production("if_stmt : IF test COLON suite")
    def if_stmt(pack):
        (if_, test, colon, suite) = pack
        return [{
            "type": "ifelseblock",
            "value": [{
                "type": "if",
                "value": suite,
                "test": test,
                "first_formatting": if_.hidden_tokens_after,
                "second_formatting": colon.hidden_tokens_before,
                "third_formatting": colon.hidden_tokens_after,
            }]
        }]

    @pg.production("if_stmt : IF test COLON suite elifs")
    def if_elif_stmt(pack):
        (if_, test, colon, suite, elifs) = pack
        return [{
            "type": "ifelseblock",
            "value": [{
                "type": "if",
                "value": suite,
                "test": test,
                "first_formatting": if_.hidden_tokens_after,
                "second_formatting": colon.hidden_tokens_before,
                "third_formatting": colon.hidden_tokens_after,
            }] + elifs
        }]

    @pg.production("elifs : ELIF test COLON suite elifs")
    @pg.production("elifs_before_else : ELIF test COLON suite elifs_before_else")
    def elifs_middle(pack,):
        (elif_, test, colon, suite, elifs) = pack
        return [{
            "type": "elif",
            "first_formatting": elif_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
            "value": suite,
            "test": test,
        }] + elifs

    @pg.production("elifs : ELIF test COLON suite")
    def elifs_final(pack,):
        (elif_, test, colon, suite) = pack
        return [{
            "type": "elif",
            "first_formatting": elif_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
            "value": suite,
            "test": test,
        }]

    @pg.production("elifs_before_else : ELIF test COLON suite")
    def elifs_before_else(pack,):
        (elif_, test, colon, suite) = pack
        return [{
            "type": "elif",
            "first_formatting": elif_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
            "value": suite,
            "test": test,
        }]

    @pg.production("if_stmt : IF test COLON suite else_stmt")
    def if_else_stmt(pack):
        (if_, test, colon, suite, else_stmt) = pack
        return [{
            "type": "ifelseblock",
            "value": [{
                "type": "if",
                "value": suite,
                "test": test,
                "first_formatting": if_.hidden_tokens_after,
                "second_formatting": colon.hidden_tokens_before,
                "third_formatting": colon.hidden_tokens_after,
            }, else_stmt]
        }]

    @pg.production("if_stmt : IF test COLON suite elifs_before_else else_stmt")
    def if_elif_else_stmt(pack):
        (if_, test, colon, suite, elifs, else_stmt) = pack
        return [{
            "type": "ifelseblock",
            "value": [{
                "type": "if",
                "value": suite,
                "test": test,
                "first_formatting": if_.hidden_tokens_after,
                "second_formatting": colon.hidden_tokens_before,
                "third_formatting": colon.hidden_tokens_after,
            }] + elifs + [else_stmt]
        }]

    # PEP 634 - Pattern Matching
    @pg.production("match_stmt : MATCH test COLON suite")
    def match_stmt(pack):
        (match, subject, colon, cases) = pack
        return [{
            "type": "match",
            "subject": subject,
            "cases": cases,
            "first_formatting": match.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
        }]

    @pg.production("case_stmt : CASE pattern COLON suite")
    def case_stmt(pack):
        (case, pattern, colon, suite) = pack
        return [{
            "type": "case",
            "pattern": pattern,
            "guard": {},
            "first_formatting": case.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
            "fourth_formatting": [],
            "fifth_formatting": [],
            "value": suite,
        }]

    @pg.production("case_stmt : CASE pattern IF test COLON suite")
    def case_guard_stmt(pack):
        (case, pattern, if_, guard, colon, suite) = pack
        return [{
            "type": "case",
            "pattern": pattern,
            "guard": guard,
            "first_formatting": case.hidden_tokens_after,
            "second_formatting": if_.hidden_tokens_before,
            "third_formatting": if_.hidden_tokens_after,
            "fourth_formatting": colon.hidden_tokens_before,
            "fifth_formatting": colon.hidden_tokens_after,
            "value": suite,
        }]

    # Pattern productions - use or_test to avoid conflicts with AS and VBAR
    # AS pattern: pattern as name
    @pg.production("pattern : or_pattern AS NAME")
    def pattern_as(pack):
        (pattern, as_, name) = pack
        return {
            "type": "pattern_as",
            "pattern": pattern,
            "name": name.value,
            "first_formatting": as_.hidden_tokens_before,
            "second_formatting": as_.hidden_tokens_after,
        }

    # OR pattern: pattern | pattern (left-recursive)
    @pg.production("or_pattern : or_pattern VBAR base_pattern")
    def pattern_or(pack):
        (or_pattern, vbar, base_pattern) = pack
        # Flatten nested OR patterns
        if isinstance(or_pattern, dict) and or_pattern.get("type") == "pattern_or":
            return {
                "type": "pattern_or",
                "patterns": or_pattern["patterns"] + [{
                    "type": "comma",
                    "first_formatting": vbar.hidden_tokens_before,
                    "second_formatting": vbar.hidden_tokens_after,
                }, base_pattern],
            }
        return {
            "type": "pattern_or",
            "patterns": [or_pattern, {
                "type": "comma",
                "first_formatting": vbar.hidden_tokens_before,
                "second_formatting": vbar.hidden_tokens_after,
            }, base_pattern],
        }

    @pg.production("or_pattern : base_pattern")
    def or_pattern_base(pack):
        (base_pattern,) = pack
        return base_pattern

    @pg.production("pattern : or_pattern")
    def pattern_or_pattern(pack):
        (or_pattern,) = pack
        return or_pattern

    # Base pattern - use or_test to avoid conflict with guard's IF keyword
    # (test includes conditional expressions like 'x if cond else y')
    @pg.production("base_pattern : or_test")
    def base_pattern_or_test(pack):
        (or_test,) = pack
        return or_test
