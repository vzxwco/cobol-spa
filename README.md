# COBOL Static Program Analysis

cobol-spa reads a COBOL source file (or stdin), performs a static program analysis, and outputs the result in a file (or stdout).

The following types of static program analysis are supported:

* control flow graph
* dependency graph

The following output formats are supported:

* JSON (for further processing)
* DOT (graph description language)
* SQL (INSERT statements)
* PYTHON (builtin PrettyPrinter)

COBOL grammar is nasty. cobol-spa parses only simple statements. In control flow mode, cobol-spa searches for `SECTION <FOO>` and `PERFORM <SECTION>` statements to determine section calls. In dependency mode, cobol-spa searches for `CALL <MODULE>` statements to determine module calls.
