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

    @pg.production("excepts : excepts except_stmt")
    def excepts(pack):
        (excepts_, except_stmt) = pack
        return excepts_ + except_stmt

    @pg.production("excepts : except_stmt")
    def excepts_except_stmt(pack):
        (except_stmt,) = pack
        return except_stmt

    @pg.production("except_stmt : leading_comments EXCEPT test AS test COLON suite")
    def except_as_stmt(pack):
        (leading_comments, except_, test, as_, test2, colon, suite) = pack
        return [{
            "type": "except",
            "leading_comments": leading_comments,
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

    @pg.production("except_stmt : leading_comments EXCEPT test COMMA test COLON suite")
    def except_comma_stmt(pack):
        (leading_comments, except_, test, comma, test2, colon, suite) = pack
        return [{
            "type": "except",
            "leading_comments": leading_comments,
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

    @pg.production("except_stmt : leading_comments EXCEPT COLON suite")
    def except_stmt_empty(pack):
        (leading_comments, except_, colon, suite) = pack
        return [{
            "type": "except",
            "leading_comments": leading_comments,
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

    @pg.production("except_stmt : leading_comments EXCEPT test COLON suite")
    def except_stmt(pack):
        (leading_comments, except_, test, colon, suite) = pack
        return [{
            "type": "except",
            "leading_comments": leading_comments,
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

    @pg.production("leading_comments : COMMENT ENDL leading_comments")
    @pg.production("leading_comments : ")
    def leading_comments(pack):
        if not pack:
            return []
        (comment, endl, more_comments) = pack
        return [{
            "type": "comment",
            "value": comment.value,
        }, {
            "type": "endl",
            "value": endl.value,
            "formatting": endl.hidden_tokens_before,
            "indent": endl.hidden_tokens_after[0]["value"] if endl.hidden_tokens_after else "",
        }] + more_comments

    @pg.production("finally_stmt : leading_comments FINALLY COLON suite")
    def finally_stmt(pack):
        (leading_comments, finally_, colon, suite) = pack
        return {
            "type": "finally",
            "value": suite,
            "leading_comments": leading_comments,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
        }

    @pg.production("else_stmt : leading_comments ELSE COLON suite")
    def else_stmt(pack):
        (leading_comments, else_, colon, suite) = pack
        return {
            "type": "else",
            "value": suite,
            "leading_comments": leading_comments,
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

    @pg.production("elifs : elifs leading_comments ELIF test COLON suite")
    def elifs_elif(pack,):
        (elifs, leading_comments, elif_, test, colon, suite) = pack
        return elifs + [{
            "type": "elif",
            "leading_comments": leading_comments,
            "first_formatting": elif_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
            "value": suite,
            "test": test,
        }]

    @pg.production("elifs : leading_comments ELIF test COLON suite")
    def elif_(pack,):
        (leading_comments, elif_, test, colon, suite) = pack
        return [{
            "type": "elif",
            "leading_comments": leading_comments,
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

    @pg.production("if_stmt : IF test COLON suite elifs else_stmt")
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
