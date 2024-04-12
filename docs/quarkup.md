# The Quarkup Process

> [!NOTE]
> This page is currently under construction. Apologies for incomplete or inaccurate content.

[*Quarkup*](glossary.md) refers to the overall process of extracting Markdown files from a GitHub repository, rendering them to HTML, and deploying them to GitHub Pages, all executed automatically through GitHub Actions.

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


## Run

The pipeline begins with a GitHub Actions workflow, dedicated to the particular source repo. This can either be triggered manually, or by another workflow in the source repo. The workflow runs the corresponding Python script (in [`scripts/`](../scripts/) for the source repo.

For instance, [*Assort*](https://github.com/Sup2point0/Assort) has a workflow configured to run the `Quarkup Assort` workflow ([`assort.yml`](../.github/workflows/assort.yml)) in this repo, which then runs [`assort.py`](../scripts/assort.py).


<br>


## Export

This is all handled by the Python script.

### Extract
...


<br>


## Render

Quarkdown first passes through the text, checking for Quarkdown-flavoured content – in particular `#QUARK` tokens (known as [quarks](quarks.md)), which tell Quarkdown how it should render the text and deploy the file.

The actual Markdown content is then converted to HTML through the GitHub-Flavoured Markdown API.[^api]

[^api]: Yeah, originally I was planning to write my own Markdown parser, but then I discovered GitHub’s already done that, so...

The HTML file is generated using the [*core*](../quarkdown/resources/core.html) as a base. The content itself and other metadata are added in using string formatting.


<br>


## Deploy

Finally, the changed files are uploaded (once again through the GitHub API) to the `docs/` folder of the source repository. These `.html` files will then be automatically deployed by GitHub Pages!


<br>


## Log

Changes and deployments are tracked in JSON log files, which allow Quarkdown to skip files that haven’t changed in future Quarkup processes.


<br>
