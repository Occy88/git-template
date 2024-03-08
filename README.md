# git-templates
Welcome to git-templates a project for using multiple template repositories, to quickly setup new projects & their standard dependencies.\
After adding multiple repositories via `git templates add` on `git templates update` the contents of these repo's are coppied
over to the root of your project. \
This allows you to pull updates when templates are modified and manage common code in different repositories without relying on submodules or subtrees.

## Usage
`git templates add <git-url> --branch <Optional|branch> --ref <Optional|ref>` \
`git templates update` \
`git templates remove <ref>|<git-url> \
