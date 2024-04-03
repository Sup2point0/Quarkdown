# Quarkdown Terminology

A glossary of all the jargon used in Quarkdown. A lot of the words and phrases I use may be inaccurate or entirely of my own invention, so they are documented here for clarity.

***Quarkdown*** refers to this project, the GitHub repository (with its automations through GitHub Actions), and the Markdown syntax that provides special processing.

| Term | Explanation | Notes |
| :--- | :---------- | :---- |
| activate | A *context* is *activated* (opened) when its *activation requirements* have been met, and similarly *deactivated* (closed) when its *deactivation requirements* are met. For instance, `<!--` will trigger the activation of the *HTML* context, while `-->` will close it. | |
| context | A high-level representation of what the parser is currently parsing. In the code, this is represented as a stack of the currently active contexts. | |
| deploy | The parts of the *quarkup* process involving interaction with the GitHub API. | |
| quark | A `#QUARK ...` providing info for Quarkdown. | See [quarks](quarks.md) for more. |
| quarkup | The overall process of exporting Markdown files in a repository to HTML files and adding them to that repo. Involves the **deploy** processes. | The Quarkdown workflows are named `Quarkup <repo>`. |
| render | The process of parsing Quarkdown-Flavoured Github-Flavoured Markdown, matching tokens, extracting metadata and directives, and ultimately converting the text to HTML. | This is implemented across [`quarkify.py`](../quarkdown/quarkify.py) and [`textualise.py`](../quarkdown/textualise.py). |
| token | Kinds of text fragments that each ‘word’ is matched against during rendering. | Tokens are defined in [`tokens.json`](../quarkdown/resources/tokens.json). |
