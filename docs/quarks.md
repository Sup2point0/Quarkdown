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
| Section Open | `?` | `#QUARK only?` | Open a particular section for special processing – similar to `<div class="...">`. |
| Section Close | `.` | `#QUARK only.` | Close a section, equivalent of `</div>`. |
| Variable Flag | `:` | `#QUARK EXPORT:` | Set a variable to a given value. |


<br>


## Core

### Flags

| Flag | Parameters | Values | Description | Notes |
| :--- | :--------- | :----- | :---------- | :---- |
| `EXPORT` | `<path>` | | The file path to export to in the `docs/` folder of the relevant repository. | `docs/` is not needed at the start, since this is automagically prepended. No file extension is needed either, since all files will be exported to `.html`. |

### Layout

```md
<!-- #QUARK live!
EXPORT: <folder>/<file>
STYLE: <style(s)>
POLARITY: <light/dark>
INDEX: <category(s)>
DATE: <yy> <mm> <dd>
-->
```


<br>


## Cheat Sheet

```md
<!-- #QUARK live! -->

<!-- #QUARK kill? -->
This text isn’t rendered to HTML.
<!-- #QUARK kill. -->

<!-- #QUARK only?
This text won’t show up in Markdown, but is rendered to HTML.
#QUARK only. -->

<!-- #QUARK contents? -->
A hardcoded table of contents will be rendered specially by Quarkdown.
<!-- #QUARK contents. -->

<!-- #QUARK
EXPORT: folder/file
STYLE: default creative personal
POLARITY: light | dark
INDEX: category category
DATE: yy [mm dd]
-->
```
