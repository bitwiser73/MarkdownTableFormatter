# Markdown Table Formatter

Sublime Text 3 markdown plugin that offers table formatting.

Inspired by the [Atom's version](https://atom.io/packages/markdown-table-formatter) from fcrespo82 (Fernando).

markdowntableformatter[at]gmail[.]com

[![MIT licensed][img-mit]](./LICENSE)
[![Donate][img-paypal]][donate-paypal]

![Example](mtf_show_off_small.gif)


## Usage

There are two basic ways of using this plugin. Select what you want to format and hit **Ctrl+Alt+Shift+T** or use the same shortcut without selection to format the entire document.  

## Configuration

```
{
	// make plugin verbose in debug console
	"verbose": false,

	// scan document to format tables when saving
	"autoformat_on_save": false,

	// spaces between "|" and cell's text
	"margin": 1,

	// additional spaces before/after cell's text (depending on justification)
	"padding": 0,

	// how text should be justified when not specified [LEFT, RIGHT, CENTER]
	"default_justification": "LEFT"
}
```

# Support it!
[![Donate][img-paypal]][donate-paypal]


[donate-paypal]: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WAQUTBM9K8246

[img-mit]: https://img.shields.io/badge/license-MIT-blue.svg
[img-paypal]: https://img.shields.io/badge/Donate-PayPal-blue.svg
