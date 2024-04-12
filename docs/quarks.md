# Quarks

> [!NOTE]
> This page is currently under construction. Apologies for incomplete or inaccurate content.

Quarkdown extracts metadata and processing directives through *quarks*. These are added to Markdown documents via HTML comments (which aren’t rendered) containing a `#QUARK` flag.


<br>


## Flavours

The behaviour of a quark is influenced by its *flavour*, indicated via a particular punctuation mark.

| Flavour | Mark | Instance | Description |
| :------ | :--- | :------- | :---------- |
| Boolean Flag | `!` | `#QUARK live!` | Set a flag to a hardcoded value determined by the parser. |
| Variable Flag | `:` | `#QUARK EXPORT:` | Set a variable to a given value. |
| Section Open | `?` | `#QUARK only?` | Open a particular section for special processing – similar to `<div class="...">`. |
| Section Close | `.` | `#QUARK only.` | Close a section, equivalent of `</div>`. |


<br>


## Activity

Documents to be exported by Quarkdown must be marked as *active* with `#QUARK live!`. Conversely, documents can be explicitly marked as *inactive* with `#QUARK dead!`. If no `live!` quark is detected within a certain number of lines, the document is automatically flagged as inactive.

Processing is skipped for inactive files. Whichever quark is used, it should be placed as close to the top as possible (below the page title by convention) to confirm its activity as early as possible.

### Instance

```md
# Lorem Ipsum
<!-- #QUARK live! -->

The quick brown fox jumps over the lazy dog.
```

```md
# Lorem Ipsum
<!-- #QUARK dead! -->

The quick brown fox jumps over the lazy dog.
```


<br>


## Core

Alongside the `live` indicator is a series of metadata flags which direct Quarkdown in how to export the document.

### Flags

| Flag | Parameters | Values | Required | Description | Notes |
| :--- | :--------- | :----- | :------- | :---------- | :---- |
| `EXPORT` | `<path>` | | yes | The file path to export to in the `docs/` folder of the relevant repository. | `docs/` is not needed at the start, since this is automagically prepended. No file extension is needed either, since all files will be exported to `.html`. |
| `STYLE` | `<style(s)>` | `default` `creative` | no, defaults to `auto` | The style(s) to use. | |
| `DUALITY` | `<theme>` | `light` `dark` | no, defaults to `auto` | The colour scheme to use. | |
| `INDEX` | `<category(s)>` | any, `auto` | no | Index pages to add this page to. | If set to `auto` the page will be added to the index page of its parent directory. For instance, if `EXPORT` is `dir/folder/file`, this page will be indexed in `folder/index.html`. |
| `DATE` | `<year> <month/season?> <day?>` | | no | The date the page was created. | Used for sorting contents in index pages. |

### Layout

```md
<!-- #QUARK live!
  EXPORT: <folder>/<file>
  STYLE: <style(s)>
  POLARITY: <light/dark>
  INDEX: <category(s)>
  DATE: <yy> <mm?> <dd?>
-->
```


<br>


## Section

Section quarks indicate that the text they enclose should be processed in a particular way by Quarkdown. These always appear in pairs, with a `quark?` to open the section and `quark.` to close it.

### `leave`
Indicates that Quarkdown shouldn’t render the enclosed text.

```md
The quick brown fox jumps over the lazy dog.

<!-- #QUARK leave? -->
This text isn’t rendered or processed.
<!-- #QUARK leave. -->

The quick brown fox jumps over the lazy dog.
```

### `only`
Encloses a section that is rendered by Quarkdown but isn’t displayed otherwise.


<br>


## Cheat Sheet

```md
<!-- #QUARK live!
  EXPORT: folder/file
  STYLE: default creative personal
  POLARITY: light
  INDEX: category category
  DATE: 24 04 02
-->

<!-- #QUARK ignore? -->
This text isn’t rendered to HTML.
<!-- #QUARK ignore. -->

<!-- #QUARK only?
This text won’t show up in Markdown, but is rendered to HTML.
#QUARK only. -->

<!-- #QUARK contents? -->
A hardcoded table of contents will be rendered specially by Quarkdown.
<!-- #QUARK contents. -->
```
