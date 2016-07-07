# COBOL Static Program Analysis

cobol-spa reads a COBOL source file (or stdin), performs a static program analysis, and outputs the result in a file (or stdout). Two types of static program analysis are supported:

* control flow graph
* dependency graph

Two output formats are supported:

* JSON (for further processing)
* DOT (graph description language)

COBOL grammar is nasty. cobol-spa parses only simple statements. In control flow mode, cobol-spa searches for `SECTION <FOO>` and `PERFORM <SECTION>` statements to determine section calls. In dependency mode, cobol-spa searches for `CALL <MODULE> USING <LINKAGE>` statements to determine module calls.
