# Quarkdown Walkthrough

> [!NOTE]
> This document is a guided walkthrough on how to use *Quarkdown*. For a general reference of all available features, see [quarks](quarks.md).

Quarkdown is an engine for taking Markdown files from a GitHub repo, and exporting them to HTML files which are then deployed to a GitHub Pages site. Unlike [Jekyll<sup>↗</sup>](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll), Quarkdown gives you much more fine-grained control over how a document is exported, unlocking way more flexibility and customisability.[^flex]

[^flex]: Whether the webpage really needs to be different from the Markdown file or why the Markdown file is on GitHub at all are... irrelevant questions, heh.


<br>


## Export Configuration

Let’s say we have a wonderful piece of writing in `masterpiece.md` which we’d like to export.

First, to mark the file as *active* we’ll need to add a `#QUARK live!` near the start. This tells Quarkdown *Hey, you should export this!* when it parses the file. I personally find the line below the page title to be the most logical place for this.

```diff
  # Quarkdown is Cool
+ <!-- #QUARK live! -->
```

Within this block we’ll also provide the export metadata for Quarkdown. This is a series of properties we define that tell Quarkdown exactly how to render and deploy the file.

All files, by default, will export to the `docs/` folder of the repo with a sanitised version of their original file name. However, we can specify a deeper path and/or a different file name with the `EXPORT` flag. Let’s export to `docs/examples/master-piece.html`.

```diff
  # Quarkdown is Epic
  <!-- #QUARK
+   EXPORT: examples/master-piece
  -->
```

Note that no `.html` extension is needed, since this is appended automatically.

> [!NOTE]
> Changing the root export directory (such as from `docs/` to `gh-pages`) requires passing a different `root` parameter in the Python script, so isn’t configured through the files themselves.

We might want to apply different styling depending on what kind of file it is, so we use `STYLE`. This can even take multiple styles, which are simply separated by spaces.

```diff
  # Quarkdown is Based
  <!-- #QUARK
    EXPORT: examples/master-piece
+   STYLE: dev tech
  -->
```


<br>


## Divergent Rendering

When exporting to HTML, there may be parts of the page we don’t want to include. Conversely, there might be content we want to have in the webpage that don’t show up in the Markdown.

Quarkdown has many kinds of **section quarks** to help achieve this.

For instance, to exclude a section from processing, enclose it with the `leave` quark.

```md
  <!-- #QUARK leave? -->
  wassup github nerds
  <!-- #QUARK leave. -->
```
