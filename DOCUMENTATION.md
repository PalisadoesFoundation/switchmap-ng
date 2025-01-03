# Documentation
Welcome to our documentation guide. Here are some useful tips you need to know!

# Table of Contents

<!-- TOC -->

- [Documentation](#documentation)
- [Table of Contents](#table-of-contents)
  - [Where to find our documentation](#where-to-find-our-documentation)
  - [How to use Docusaurus](#how-to-use-docusaurus)
  - [Other information](#other-information)

<!-- /TOC -->

## Where to find our documentation

Our documentation can be found in ONLY TWO PLACES:

1. ***Inline within the repository's code files***: We have automated processes to extract this information and place it in our documentation site [docs.switchmap-ng.io](https://docs.switchmap-ng.io/). 
2. ***In our `switchmap-ng-docs` repository***: Our [SwitchMap-NG Docs](https://github.com/PalisadoesFoundation/switchmap-ng-docs) repository contains user edited markdown files that are automatically integrated into our documentation site [docs.switchmap-ng.io](https://docs.switchmap-ng.io/) using the [Docusaurus](https://docusaurus.io/) package.

## How to use Docusaurus
The process in easy:
1. Install `switchmap-ng-docs` on your system
1. Launch docusaurus on your system according to the `switchmap-ng-docs`documentation. 
    - A local version of `docs.switchmap-ng.io` should automatically launched in your browser at http://localhost:3000/
1. Add/modify the markdown documents to the `docs/` directory of the `switchmap-ng-docs` repository
1. If adding a file, then you will also need to edit the `sidebars.js` which is used to generate the [docs.switchmap-ng.io](https://docs.switchmap-ng.io/) menus.
1. Always monitor the local website in your brower to make sure the changes are acceptable. 
    - You'll be able to see errors that you can use for troubleshooting in the CLI window you used to launch the local website.

## Other information
***PLEASE*** do not add markdown files in this repository. Add them to `switchmap-ng-docs`!
