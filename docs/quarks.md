# Quarks

Quarkdown extracts metadata and processing directives through *quarks*. These are added to Markdown documents via HTML comments (which aren’t rendered) containing a `#QUARK` flag.


<br>


## Flavours

The behaviour of a quark is influenced by its *flavour*, indicated via a particular punctuation mark.

| Flavour | Mark | Description |
| :------ | :--- | :---------- |
| Boolean Flag | `!` | Set a flag to a hardcoded value determined by the parser. |
| Section Open | `?` | Open a particular section for special processing – similar to `<div class="...">`. |
| Section Close | `.` | Close a section, equivalent of `</div>`. |
| Variable Flag | `:` | Set a variable to a given value. |


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
