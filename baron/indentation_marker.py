from .utils import FlexibleIterator


"""
Objective: add an INDENT token and a DEDENT token arround every block.

Strategy: put after every ":" that is not in a slice/dictionary declaration/lambda.

Slice and dictionary are easy: increase a number when a "[" or "{" is found,
decrease it for a "]" or "}". If the number is != 0, we are in a dictionary or
slice -> do not put a INDENT when a ":" is found.

Lambda are a bit different: increase another number when a "lambda" is found,
if the number is != 0 and a ":" is found, decrease this number, otherwise put a
INDENT.

For the DEDENT, I'm probably going to need to keep a list of indentation and
decheck the last one every time I encounter a meaningfull line. Still need to
test this idea.
"""


def mark_indentation(sequence):
    r = list(mark_indentation_generator(sequence))
    # import pdb; pdb.set_trace()
    return r


def transform_tabs_to_spaces(string):
    return string.replace("\t", " " * 8)


def get_space(node):
    """Return space formatting information of node"""
    # If the node does not have a third formatting item - like in
    # a ('ENDL', '\n') node
    if len(node) < 4 or len(node[3]) == 0:
        return ""
    return transform_tabs_to_spaces(node[3][0][1])


def mark_indentation_generator(sequence):
    iterator = FlexibleIterator(sequence)
    current = None, None
    indentations = []
    while True:
        if iterator.end():
            return

        current = next(iterator)

        if current is None:
            return

        # end of the file, I need to pop all indentations left and put the
        # corresponding dedent token for them
        if current[0] == "ENDMARKER":
            for _ in indentations:
                yield ('DEDENT', '')

        yield current

        if current[0] == "ENDL":
            new_indent = get_space(current)
            # import pdb; pdb.set_trace()

            if new_indent and (not indentations or len(new_indent) > len(indentations[-1])):
                indentations.append(new_indent)
                yield ('INDENT', '')
                # import pdb; pdb.set_trace()

            elif indentations:
                comments_and_blank_lines = list(pop_comments_and_blank_lines(iterator))
                if comments_and_blank_lines:
                    new_indent = get_space(comments_and_blank_lines[-1])
                if len(new_indent) < len(indentations[-1]):
                    next_is_clause = iterator.show_next()[0] in ("ELSE", "ELIF",
                                                                 "EXCEPT", "FINALLY")
                    if next_is_clause:
                        yield from comments_and_blank_lines

                    while indentations and len(new_indent) < len(indentations[-1]):
                        indentations.pop()
                        # include comments in body
                        yield ('DEDENT', '')
                        # comments out of body

                    if not next_is_clause:
                        yield from comments_and_blank_lines
                else:
                    yield from comments_and_blank_lines



def pop_comments_and_blank_lines(iterator):
    if iterator.show_next()[0] not in ("ENDL", "COMMENT"):
        return

    for i in iterator:
        yield i
        if iterator.show_next()[0] not in ("ENDL", "COMMENT"):
            break
