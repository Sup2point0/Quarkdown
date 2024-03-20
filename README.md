<h1 align="center"> <em> Quarkdown </em> </h1>

A personalised GitHub-Flavoured Markdown to HTML renderering engine which automatically renders files in GitHub repositories and deploys them to GitHub Pages.


<br>


## Overview

A brief general overview of how *Quarkdown* works.

- My super repo [*Assort*](https://github.com/Sup2point0/Assort) has a GitHub Action configured to trigger whenever a commit is pushed to it.
- This action runs a GitHub Action in this repo ([`assort.yml`](.github/workflows/assort.yml)).
- That action then runs a Python script ([`assort.py`](source/assort.py)).
- This script accesses *Assort* through the GitHub API and scans for (updated) Markdown (`.md`) files.
  - For those files, it exports the Markdown content to HTML using the GitHub-Flavoured Markdown API.
  - It then develops and restructures this with special Quarkdown-Flavoured Markdown parsing ([`quarkdown.py`](source/quarkdown.py)) to apply special formatting, using the [`core.html`](source/resources/core.html) template and various stylesheets.
  - Updates are logged with JSON to track which files have already been rendered, so as to avoid needlessly re-rendering files that haven’t updated.
- The rendered `.html` files are added to the `docs/` folder in *Assort*, and a single commit is made with all the updates.[^combine-commits]
- GitHub Pages will then deploy those to [sup2point0.github.io/Assort](https://sup2point0.github.io/Assort)!

[^combine-commits]: This is actually a non-trivial challenge. It involves blobs.


<br>


## Rationale

Over the years I’ve created so, so many Markdown files in *Assort* that it’s gotten ridiculous – it’s basically my own personal wiki at this point. So, I thought why not give people the option to browse it through a website? Don’t get me wrong, GitHub is already fantastic at displaying Markdown files, but with an actual webpage we can make it *so* much more personalised.


<br>


## Future Features

- Devise a way to upgrade *Assort* into a wiki-like website &ndash; i.e. with navigation. Why is this difficult? Cuz the file paths of .md files in the repo are not the same as the URLs of the .html files on the website. We’ll see.
  - Also, for a wiki you’d probably need a way to search, and... well, firstly GitHub Pages is for static sites, and secondly I have no clue how to create an efficient search engine.


<br>
