Grammar reference
=================

This page is here to serve as a reference for the grammar implementation. Baron
started as a python2.7 grammar implementation following `the official
specification for that <https://docs.python.org/2/reference/grammar.html>`_ and
supporting both :file:`print statement` and :file:`print function`.

The evolution path regarding python3* is the adopt the same strategy that
lib2to3 and try to support a combination of both grammar as much as possible.

This page describe the decisions taken regarding this dual support and it's
progress. Hopefully there will be very few conflicting situations.

Current goal is `python 3.6 specification <https://docs.python.org/3.6/reference/grammar.html>`_.

Python 2 and python 3.6 grammar differences
===========================================

As a reference and an overview, here is screenshot of vimdiff showing the difference between python 2.7 and python 3.6 grammar differences.

.. image:: grammar-python-2.7-3.6-diff-1.png

.. image:: grammar-python-2.7-3.6-diff-2.png

.. image:: grammar-python-2.7-3.6-diff-3.png

List of differences
===================

**Some of the diff have been edited to isolate the focused difference of the
section**

Python 3.3 is the based grammar I've started diffing with, some of the grammar
differences marked as 3.3 are actually from older python version.

Current status
==============

Grammar diff has been done up to python 3.6.2.

Still, some stuff for the lexer are probably missing in this list like:

* fstrings
* adding _ in numbers

I need to got through all release notes to see that.

Done
====

Print function
--------------

Python 3.3 or earlier

.. image:: ./grammar_diff/print_function.png

Already done since the start.

This is handle at the parser initialisation level, is activate or not the
print_function rule.

TODO
====

Typed arguments
---------------

Python 3.3 or earlier

.. image:: ./grammar_diff/typed_args.png

Action:

::

    # parameters
    # this is mixed with the removal of def a((b, c)): style
    # which will probably need to continue supporting

    CHANGE parameters: '(' [varargslist] ')'
                               ^
    TO parameters: '(' [typedargslist] ')'
                             ^

::

    # CHANGE
    varargslist: ((fpdef ['=' test] ',')*
                  ('*' NAME [',' '**' NAME] | '**' NAME) |
                  fpdef ['=' test] (',' fpdef ['=' test])* [','])
    fpdef: NAME | '(' fplist ')'
    fplist: fpdef (',' fpdef)* [',']

    # TO
    typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [',' [
            '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
          | '**' tfpdef [',']]]
      | '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
      | '**' tfpdef [','])
    tfpdef: NAME [':' test]
    varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [',' [
            '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
          | '**' vfpdef [',']]]
      | '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
      | '**' vfpdef [',']
    )
    vfpdef: NAME



Function return type
--------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/function_return_type.png

Action:

::

    ADD '->' to the lexer
    ADD ['->' test] to funcdef rule
    funcdef: 'def' NAME parameters ['->' test] ':' suite

Nonlocal statement
------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/nonlocal_statement.png

Action:

::

    ADD 'nonlocal' to lexer
    ADD 'nonlocal_stmt' to 'small_stmt'

    ADD new rule:
    nonlocal_stmt: 'nonlocal' NAME (',' NAME)*

Exec function
-------------

Python 3.3 or earlier

.. image:: ./grammar_diff/exec_function.png

Like print_function but for 'exec'.

No one seems to be using that.

*var generalisation
-------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/testlist_start_expressiong.png

.

.. image:: ./grammar_diff/star_expr.png

.

.. image:: ./grammar_diff/star_expr_in_testlist_comp.png

.

.. image:: ./grammar_diff/star_expr_in_expr_list.png

Raise from
----------

Python 3.3 or earlier

.. image:: ./grammar_diff/raise_from.png

Action:

::

    # 2.7
    raise_stmt: 'raise' [test [',' test [',' test]]]

    # 3.3
    raise_stmt: 'raise' [test ['from' test]]

    # merge
    raise_stmt: 'raise' [test [(',' test [',' test]] | 'from' test)]

Ellipsis in from import
-----------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/ellipsis_in_from_import.png

New lambda grammar
------------------

Python 3.3 or earlier

I have no idea on what to do with this one yet.

.. image:: ./grammar_diff/new_lambda_grammar.png

.. image:: ./grammar_diff/new_grammar_for_if_cond.png

Remove old list comprehension syntax
------------------------------------

Python 3.3 or earlier

I'm not sure on how to handle both situations (and it is needed? Old list
comprehension syntax is like super edgy, I really wonder if anyonne has
actually used that one that?)

.. image:: ./grammar_diff/remove_old_list_comprehension_syntax.png

.. image:: ./grammar_diff/no_more_list_for_rule.png

False|True|None|... are now atoms in the grammar
------------------------------------------------

Python 3.3 or earlier

Do I need to do anything about that?

.. image:: ./grammar_diff/more_atoms.png

Inheritance in class definition uses arglist now
------------------------------------------------

Python 3.3 or earlier

I have no idea on why this is here but that's easy to change.

.. image:: ./grammar_diff/class_inherit_is_arglist_now.png

Yield From
----------

Python 3.3 or earlier

.. image:: ./grammar_diff/yield_from.png

Async Funcdef
-------------

Python 3.5

Before:

::

    decorated: decorators (classdef | funcdef)

After:

::

    decorated: decorators (classdef | funcdef | async_funcdef)
    async_funcdef: ASYNC funcdef


Await atom
----------

Python 3.5

Before:

::

    power: atom trailer* ['**' factor]

After:

::

    power: atom_expr ['**' factor]
    atom_expr: [AWAIT] atom trailer*

Matrix operator
---------------

Python 3.5

::

    ADD '@' and '@=' to the lexer
    ADD '@=' in augassign
    ADD '@' in term

::

    augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' |
                '<<=' | '>>=' | '**=' | '//=')

    term: factor (('*'|'@'|'/'|'%'|'//') factor)*

Kwargs expressions
------------------

Python 3.5

Before:

::

    dictorsetmaker: ( (test ':' test (comp_for | (',' test ':' test)* [','])) |
                      (test (comp_for | (',' test)* [','])) )

    arglist: (argument ',')* (argument [',']
                             |'*' test (',' argument)* [',' '**' test]
                             |'**' test)

    # The reason that keywords are test nodes instead of NAME is that using NAME
    # results in an ambiguity. ast.c makes sure it's a NAME.
    argument: test [comp_for] | test '=' test

After:

::

    dictorsetmaker: ( ((test ':' test | '**' expr)
                       (comp_for | (',' (test ':' test | '**' expr))* [','])) |
                      ((test | star_expr)
                       (comp_for | (',' (test | star_expr))* [','])) )

    # can be simplified apparently
    arglist: argument (',' argument)*  [',']

    # The reason that keywords are test nodes instead of NAME is that using NAME
    # results in an ambiguity. ast.c makes sure it's a NAME.
    # "test '=' test" is really "keyword '=' test", but we have no such token.
    # These need to be in a single rule to avoid grammar that is ambiguous
    # to our LL(1) parser. Even though 'test' includes '*expr' in star_expr,
    # we explicitly match '*' here, too, to give it proper precedence.
    # Illegal combinations and orderings are blocked in ast.c:
    # multiple (test comp_for) arguments are blocked; keyword unpackings
    # that precede iterable unpackings are blocked; etc.
    argument: ( test [comp_for] |
                test '=' test |
                '**' test |
                '*' test )



Variables annotations
---------------------

Python 3.6

Before:

::

    expr_stmt: testlist_star_expr (augassign (yield_expr|testlist) |
                         ('=' (yield_expr|testlist_star_expr))*)

After:

::

    expr_stmt: testlist_star_expr (annassign | augassign (yield_expr|testlist) |
                         ('=' (yield_expr|testlist_star_expr))*)
    annassign: ':' test ['=' test]

async for loop
--------------

Python 3.6

Before:

::

    comp_for: 'for' exprlist 'in' or_test [comp_iter]

After:

::

    comp_for: [ASYNC] 'for' exprlist 'in' or_test [comp_iter]


Refactoring in typedargslist ?
------------------------------

I think this is for asynchronous generator and comprehension:

* https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep525
* https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep530

Before:

::

    typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [','
           ['*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef]]
         |  '*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
    varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [','
           ['*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef]]
         |  '*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef)

After:

::

    typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [','
           ['*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
          | '**' tfpdef [',']]]
      | '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
      | '**' tfpdef [','])
    varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [','
           ['*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
         | '**' vfpdef [',']]]
      | '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
      | '**' vfpdef [',']
    )














Nothing to do
=============

Those are things that have been removed from python3 grammar but we still need
to support (and we already do) so we don't have to do anything.

No more commat syntax in except close
-------------------------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/no_more_commat_in_execption_close.png

No more backquote syntax
------------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/no_more_backquote_syntax.png

No more '.' '.' '.' in the grammar
----------------------------------

Python 3.3 or earlier

.. image:: ./grammar_diff/ellipsis_is_first_class_now_not_needed_anymore.png