# Quarkdown Terminology

A glossary of all the jargon used in Quarkdown. A lot of the words and phrases I use may be inaccurate or entirely of my own invention, so they are documented here for clarity.

***Quarkdown*** refers to this project, the GitHub repository (with its automations through GitHub Actions), and the Markdown syntax that provides special processing.

| Term | Explanation | Notes |
| :--- | :---------- | :---- |
| activate | A *context* is *activated* (opened) when its *activation requirements* have been met, and similarly *deactivated* (closed) when its *deactivation requirements* are met. For instance, `<!--` will trigger the activation of the *HTML* context, while `-->` will close it. | |
| context | A high-level representation of what the parser is currently parsing. In the code, this is represented as a stack of the currently active contexts. | |
| deploy | The part of the *quarkup* process where exported files are uploaded to GitHub through the GitHub API. | Implemented in [`deploy.py`](../quarkdown/deploy.py). |
| export | Another term for *quarkup*. | *Export* is conveniently more natural to use as a verb. |
| extract | The part of the *quarkup* process where the Markdown files are obtained from a GitHub repo. | Implemented in [`deploy.py`](../quarkdown/deploy.py). |
| quark | A `#QUARK ...` text fragment providing info for Quarkdown. | See [quarks](quarks.md) for more. |
| quarkup | The overall process of exporting Markdown files in a repository to HTML files and uploading them to GitHub. Involves the **extract**, **render** and **deploy** processes. | The Quarkdown workflows are named `Quarkup <repo>`. |
| render | The process of parsing Quarkdown-Flavoured Github-Flavoured Markdown, matching tokens, extracting metadata and directives, and ultimately converting the text to HTML. | Implemented across [`quarkify.py`](../quarkdown/quarkify.py) and [`textualise.py`](../quarkdown/textualise.py). |
| token | Kinds of text fragments that each ‘word’ is matched against during rendering. | Tokens are defined in [`tokens.json`](../quarkdown/resources/tokens.json). |
