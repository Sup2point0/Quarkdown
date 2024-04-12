<h1 align="center"> <em> Quarkdown </em> </h1>

<div align="center">
<img src="https://github.com/Sup2point0/Quarkdown/actions/workflows/tests.yml/badge.svg">
<img src="https://github.com/Sup2point0/Quarkdown/actions/workflows/assort.yml/badge.svg">
</div>

![quarkdown-title](.assets/title.png)

A personalised GitHub-Flavoured Markdown to HTML renderering engine, which automatically exports files in GitHub repositories and deploys them to GitHub Pages.


<br>


## Overview

[Quarkdown](docs/glossary.md) is an engine for extracting Markdown files from a GitHub repo, exporting them to HTML, and adding those files to the repo to be deployed by GitHub Pages.

I like to give my projects their own little bit of jargon for character, so if you’d like to understand the terms used, refer to the [glossary](docs/glossary.md).

> [!TIP]
> For more, see the [docs](docs/).


<br>


## Features

- A customised Markdown parser which handles Quarkdown-Flavoured Markdown
- An engine for extracting and uploading files through the GitHub API
- Automation through GitHub Actions for automatically exporting and deploying GitHub repositories


<br>


## Rationale

Over the years I’ve created so, so many Markdown files in *Assort* that it’s gotten ridiculous – it’s basically my own personal wiki at this point. So, I thought why not give people the option to browse it through a website? Don’t get me wrong, GitHub is already fantastic at displaying Markdown files, but with an actual webpage we can make it *so* much more personalised.


<br>


## Future Features

- Add special index pages.
- Check if export filepaths have changed for a file, and if so, delete the artefact file.
- Extract article title into a special `<header>` container.
- Inject MathJax without `{}` breaking Python string formatting.
- Find a way to combine commits so that a single new deployment doesn’t result in potentially hundreds of programmatically generated commits? [^combine-commits]
- Devise a way to upgrade *Assort* into a wiki-like website &ndash; i.e. with navigation. Why is this difficult? Cuz the file paths of .md files in the repo are not the same as the URLs of the .html files on the website. We’ll see.
  - Also, for a wiki you’d probably need a way to search, and... well, firstly GitHub Pages is for static sites, and secondly I have no clue how to create an efficient search engine.

[^combine-commits]: This is actually a non-trivial challenge. It involves blobs.


<br>
