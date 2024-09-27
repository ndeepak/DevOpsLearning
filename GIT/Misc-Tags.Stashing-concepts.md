# List all the tags
$ git tag -l

#
Create a new lightweight tag
$ git tag dev-123-release-tag

#
Push the tag to remote
$ git push origin dev-123-release-tag

# See more information about the tag
$ git show dev-123-release-tag

Create Annonatated tag
#
$ git tag -a dev-123-release-tag -m "creating it for NASA client"

# See Tag information of Annotated tag
$ git show dev-124-release-tag
        tag dev-124-release-tag
        Tagger: user...
        Date:   Wed May 20 09:17:53 2020 +0530
        creating it for NASA client
        
# Creating a tag from particular commint ID (Old commit ID is - 838ccf6)
$ git tag -a relase-123-tag -m "creating old release tag" 838ccf6
$ git show relase-123-tag --> abserve that this tag has commits till '838ccf6'.

#
Deletng a tag
$ git tag -d v1.4-lw

# How do you checkout the code from a tag?
$ git checkout v1.4-lw

# Creating a branch from a tag
$ git branch dev129 relase-123-tag


Stashing
============
# Stashing the changes
$ git stash

# Un-stashing the changes
$ $ git stash pop



