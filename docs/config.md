# Configuring Quarkup for a Repository

Repositories can influence how their files are exported by providing files within a `.quarkdown/` directory at the root of the project, analogous to `.github/` or `.vscode/`. Quarkdown will check for this directory when initialising quarkup, and if found, will apply the configurations to all files when exporting.


<br>


## `config.json`

Supplies the repository-level configurations.

### Configurations

| Flag | Parameters | Values | Required | Default | Description | Notes |
| :--- | :--------- | :----- | :------- | :------ | :---------- | :---- |
| `repo-source` | `<repo-name>` | any | yes | `auto` | The repository to quarkup. | |
| `repo-export` | `<repo-name>` | any | yes | `repo-source` | The repository to commit exported files to. | |
| `root-path` | `<folder-path>` | any | no | `docs` | The root directory to commit exported files to. | No trailing backslash `\` is needed. |
| `fonts` | `[<font-name(s)>]` | any | no | `none` | Font styles to import from Google Fonts. | |

### Example

```json
{
  "repo-source": "Quarkdown",
  "repo-export": "Assort",
  "root-path": "docs/external"
  "fonts": ["Abel", "Montserrat"],
}
```


<br>


## `nav.html` / `nav.css`

Supplies the HTML and CSS for a specific navigation bar that Quarkdown will inject into every page when rendering. If not supplied, no navigation bar will be added to pages.

### Example

```html
<nav>
  ...
</nav>
```

```css
nav {
  ...
}
```
