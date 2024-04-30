# Quarks

Quarkdown extracts metadata and processing directives from through *quarks*. These are added to Markdown documents via HTML comments (which aren’t rendered in previews) containing a `#QUARK` token. Text containing quarks is referred to as *Quarkdown-Flavoured Markdown*.

```md
<!-- #QUARK flag? -->
This is what a Quark flag looks like!
<!-- #QUARK flag. -->
```

> [!TIP]
> For quick reference, see [§ Cheat Sheet](#cheat-sheet).


<br>


## Flavours

The behaviour of a quark is influenced by its *flavour*, indicated via a particular punctuation mark.

| Flavour | Mark | Instance | Description |
| :------ | :--- | :------- | :---------- |
| Boolean Flag | `!` | `#QUARK live!` | Set a flag to a hardcoded value determined by the parser. |
| Variable Flag | `:` | `#QUARK EXPORT: <path>` | Set a variable to a given value. |
| Section Open | `?` | `#QUARK only?` | Open a particular section for special processing – similar to `<div class="...">`. |
| Section Close | `.` | `#QUARK only.` | Close a section, equivalent of `</div>`. |
| Placeholder | `~` | `#QUARK index~` | Mark a point in the text which will be auto-filled with dynamically generated content. |


<br>


## Activity

Documents to be exported by Quarkdown must be marked as *active* with the `live!` flag. Conversely, documents can be explicitly marked as *inactive* with `#QUARK dead!`. If no `live!` quark is detected within a certain number of lines, the document is automatically flagged as inactive.

Processing is skipped for inactive files. Whichever quark is used, it should be placed as close to the top as possible (below the page title by convention) to confirm its activity as early as possible.

### Examples

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

Alongside the activity indicator is a series of metadata flags which instruct Quarkdown in how it should go about exporting the document.

> [!IMPORTANT]
> All parameters are case-insensitive, and values will be converted to lowercase for compatibility.

### Flags

| Flag | Parameters | Values | Required | Default | Description | Notes |
| :--- | :--------- | :----- | :------- | :------ | :---------- | :---- |
| `EXPORT` | `<path>` | any | yes | – | The file path to export to in the `docs/` folder of the relevant repository. | `docs/` is not needed at the start, since this is automagically prepended. No file extension is needed either, since all files will be exported to `.html`. |
| `STYLE` | `<style(s)>` | `auto` `index` `creative` `poetry` `dev` `tech` | no | `auto` | The style(s) to use. | |
| `DUALITY` | `<theme>` | `light` `dark` | no | `auto` | The colour scheme to use. | |
| `INDEX` | `<category(s)>` | any, `auto` | no | – | Index pages to add this page to. | If set to `auto` the page will be added to the index page of its parent directory. For instance, if `EXPORT` is `dir/folder/file`, this page will be indexed in `folder/index.html`. |
| `SHARD` | `<tag(s)>` | any | no | – | Topic tags (‘shards’) to mark the page with, for searching. | `INDEX` pages will automatically be also added as shards. |
| `DATE` | `<year> <month/season?> <day?>` | 1/2-digit numbers, `FALL` `WINTER` `SPRING` `SUMMER` | no | – | The date the page was created. | Used for sorting contents in index pages. |

### Structure

```md
<!-- #QUARK live!
  EXPORT: <folder?>/<file>
  STYLE: <style> <styles?>
  DUALITY: <light/dark>
  INDEX: <category> <categories?>
  SHARD: <tag> <tags?>
  DATE: <yy> <mm/s?> <dd?>
-->
```

### Example

```md
<!-- #QUARK live!
  EXPORT: testing/example
  STYLE: default dev
  DUALITY: light
  INDEX: tests special
  SHARD: testing hidden
  DATE: 24 SUMMER
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
Encloses a section that is rendered by Quarkdown but isn’t displayed in Markdown.

```md
The quick brown fox jumps over the lazy dog.

<!-- #QUARK only?
This text won’t show up in Markdown,
but will appear in the rendered HTML.
     #QUARK only. -->

The quick brown fox jumps over the lazy dog.
```

### `aside`
A section broken apart from the rest of the main body with softer colouring.

```md
The quick brown fox jumps over the lazy dog.

<!-- #QUARK aside? -->
Some mildly irrelevant but interesting tangent~
<-- #QUARK only. -->

The quick brown fox jumps over the lazy dog.
```


<br>


## Index Pages

README files can be specially handled by Quarkdown to act as *index* pages (`index.html` for a particular directory). They are marked with the `index!` flag, which usually appears after the `live!` flag.

The core section of an index page needs slightly different metadata. Since the file name must be `index.html`, only the folder path needs to be provided (a trailing `/` is optional – the engine will handle the path accordingly). Naturally, `INDEX` and `DATE` are irrelevant for an index page too. The style, if not provided or set to `auto`, will default to the `index` style.

```md
<!-- #QUARK live! index!
  EXPORT: folder/file
-->
```

To let Quarkdown automagically collect the list of indexed pages and sort them by date, use a `index~` quark to indicate where that should be inserted.

```md
Index will go here:
<!-- #QUARK index~ -->
```


<br>


## Cheat Sheet

### Standard

```md
<!-- #QUARK live!
  EXPORT: folder/file
  STYLE: default creative personal
  DUALITY: light
  INDEX: category category
  DATE: 24 04 02
-->

<!-- #QUARK ignore? -->
This text isn’t rendered or processed.
<!-- #QUARK ignore. -->

<!-- #QUARK only?
This text won’t show up in Markdown, but will appear in the rendered HTML.
     #QUARK only. -->

<!-- #QUARK synopsis? -->
This text will be incorporated into the header section.
<!-- #QUARK synopsis. -->

<!-- #QUARK contents? -->
A hardcoded table of contents will be rendered specially by Quarkdown.
<!-- #QUARK contents. -->
```

### Index

```md
<!-- #QUARK live! index!
  EXPORT: folder/
-->

<!-- #QUARK index~ -->
```
