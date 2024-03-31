<h1 align="center"> <em> Quarkdown </em> </h1>

A personalised GitHub-Flavoured Markdown to HTML renderering engine which automatically renders files in GitHub repositories and deploys them to GitHub Pages.


<br>


## Overview

A brief general overview of how *Quarkdown* works.

- My super repo [*Assort*](https://github.com/Sup2point0/Assort) has a GitHub Action configured to trigger whenever a commit is pushed to it.
- This action runs a GitHub Action in this repo ([`assort.yml`](.github/workflows/assort.yml)).
- That action then runs a Python script ([`assort.py`](scripts/assort.py)).
- This script accesses *Assort* through the GitHub API and scans for (updated) Markdown (`.md`) files.
  - For each file, it parses it for `#QUARK` flags (affectionately known as *quarks*) to extract meta data about how Quarkdown should process it.
  - It then exports the Markdown content to HTML using the GitHub-Flavoured Markdown API.
  - The final `.html` file is generated using the [`core.html`](quarkdown/resources/core.html) base.
  - Updates are logged with JSON to track which files have already been rendered, so as to avoid needlessly re-rendering files that haven’t updated.
- The rendered `.html` files are added to the `docs/` folder in *Assort*.
- GitHub Pages will then automatically deploy those to [sup2point0.github.io/Assort](https://sup2point0.github.io/Assort)!


<br>


## Rationale

Over the years I’ve created so, so many Markdown files in *Assort* that it’s gotten ridiculous – it’s basically my own personal wiki at this point. So, I thought why not give people the option to browse it through a website? Don’t get me wrong, GitHub is already fantastic at displaying Markdown files, but with an actual webpage we can make it *so* much more personalised.


<br>


## Future Features

- Check if export filepaths have changed for a file, and if so, delete the artefact file.
- Extract article title into a special `<header>` container.
- Inject MathJax without `{}` breaking Python string formatting.
- Find a way to combine commits so that a single new deployment doesn’t result in potentially hundreds of programmatically generated commits? [^combine-commits]
- Devise a way to upgrade *Assort* into a wiki-like website &ndash; i.e. with navigation. Why is this difficult? Cuz the file paths of .md files in the repo are not the same as the URLs of the .html files on the website. We’ll see.
  - Also, for a wiki you’d probably need a way to search, and... well, firstly GitHub Pages is for static sites, and secondly I have no clue how to create an efficient search engine.

[^combine-commits]: This is actually a non-trivial challenge. It involves blobs.


<br>
