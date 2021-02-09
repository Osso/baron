def include_control_structures(pg):
    @pg.production("try_stmt : TRY COLON suite_opt_comments excepts")
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

    @pg.production("try_stmt : TRY COLON suite_opt_comments excepts_opt_comments else_stmt leading_comments")
    def try_excepts_else_stmt(pack):
        (try_, colon, suite, excepts, else_stmt, leading_comments) = pack
        return [{
            "type": "try",
            "value": suite,
            "first_formatting": colon.hidden_tokens_before,
            "second_formatting": colon.hidden_tokens_after,
            "else": else_stmt,
            "finally": {},
            "excepts": excepts,
        }] + leading_comments

    @pg.production("try_stmt : TRY COLON suite_opt_comments excepts_opt_comments finally_stmt")
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

    @pg.production("try_stmt : TRY COLON suite_opt_comments excepts_opt_comments else_stmt_opt_comments finally_stmt")
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

    @pg.production("try_stmt : TRY COLON suite_opt_comments finally_stmt")
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

    @pg.production("excepts_opt_comments : excepts leading_comments")
    def excepts_opt_comments(pack):
        (excepts, leading_comments) = pack
        excepts[-1]["value"] += leading_comments
        return excepts

    @pg.production("excepts : except_stmt leading_comments excepts")
    def excepts(pack):
        (except_stmt, leading_comments, excepts_) = pack
        except_stmt[0]["value"] += leading_comments
        return except_stmt + excepts_

    @pg.production("excepts : except_stmt")
    def excepts_except_stmt(pack):
        (except_stmt,) = pack
        return except_stmt

    @pg.production("except_stmt : EXCEPT test AS test COLON suite_opt_comments")
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

    @pg.production("except_stmt : EXCEPT test COMMA test COLON suite_opt_comments")
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

    @pg.production("except_stmt : EXCEPT COLON suite_opt_comments")
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

    @pg.production("except_stmt : EXCEPT test COLON suite_opt_comments")
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

    @pg.production("suite_opt_comments : suite leading_comments")
    def suite_opt_comments(pack):
        (suite, leading_comments) = pack
        return suite + leading_comments


    @pg.production("leading_comments : COMMENT ENDL leading_comments")
    @pg.production("leading_comments : ")
    def leading_comments(pack):
        if not pack:
            return []
        (comment, endl, more_comments) = pack
        return [{
            "type": "comment",
            "value": comment.value,
            "formatting": comment.hidden_tokens_before,
        }, {
            "type": "endl",
            "value": endl.value,
            "formatting": endl.hidden_tokens_before,
            "indent": endl.hidden_tokens_after[0]["value"] if endl.hidden_tokens_after else "",
        }] + more_comments

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

    @pg.production("else_stmt_opt_comments : else_stmt leading_comments")
    def else_stmt_opt_comments(pack):
        (else_, leading_comments) = pack
        else_["value"] += leading_comments
        return else_

    @pg.production("for_stmt : FOR exprlist IN testlist COLON suite leading_comments")
    def for_stmt(pack,):
        (for_, exprlist, in_, testlist, colon, suite, leading_comments) = pack
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
        }] + leading_comments

    @pg.production("for_stmt : FOR exprlist IN testlist COLON suite_opt_comments else_stmt")
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

    @pg.production("while_stmt : WHILE test COLON suite leading_comments")
    def while_stmt(pack):
        (while_, test, colon, suite, leading_comments) = pack
        return [{
            "type": "while",
            "value": suite,
            "test": test,
            "else": {},
            "first_formatting": while_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
        }] + leading_comments

    @pg.production("while_stmt : WHILE test COLON suite_opt_comments else_stmt")
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

    @pg.production("if_stmt : IF test COLON suite leading_comments")
    def if_stmt(pack):
        (if_, test, colon, suite, leading_comments) = pack
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
        }] + leading_comments

    @pg.production("if_stmt : IF test COLON suite_opt_comments elifs")
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

    @pg.production("elifs : ELIF test COLON suite_opt_comments elifs")
    @pg.production("elifs_before_else : ELIF test COLON suite_opt_comments elifs_before_else")
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

    @pg.production("elifs : ELIF test COLON suite leading_comments")
    def elifs_final(pack,):
        (elif_, test, colon, suite, leading_comments) = pack
        return [{
            "type": "elif",
            "first_formatting": elif_.hidden_tokens_after,
            "second_formatting": colon.hidden_tokens_before,
            "third_formatting": colon.hidden_tokens_after,
            "value": suite,
            "test": test,
        }] + leading_comments

    @pg.production("elifs_before_else : ELIF test COLON suite_opt_comments")
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

    @pg.production("if_stmt : IF test COLON suite_opt_comments else_stmt")
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

    @pg.production("if_stmt : IF test COLON suite_opt_comments elifs_before_else else_stmt")
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
