Basic Usage
===========

Baron provides two main functions:

* :file:`parse` to transform a string into Baron's FST;
* :file:`dumps` to transform the FST back into a string.

.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

.. ipython:: python

    from baron import parse, dumps

    source_code = "def f(x = 1):\n    return x\n"
    fst = parse(source_code)
    generated_source_code = dumps(fst)
    generated_source_code
    source_code == generated_source_code

Like said in the introduction, the FST keeps the formatting unlike ASTs.
Here the following 3 codes are equivalent but their formatting is
different. Baron keeps the difference so when dumping back the FST, all
the formatting is respected:

.. ipython:: python

    dumps(parse("a = 1"))

    dumps(parse("a=1"))

    dumps(parse("a   =   1"))


Exploring the FST
-----------------

The FST is a JSON-serializable data structure. You can use Python's
built-in :file:`json` module to pretty-print it for exploration:

.. ipython:: python

    import json

    fst = parse("a = 1")
    print(json.dumps(fst, indent=4))

    fst = parse("a +=  b")
    print(json.dumps(fst, indent=4))
