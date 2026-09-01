# Basics Commands

```bash
pacman -Syu
yay
paru
# Just typing paru will update your aur packages and not your core packages.
paru -S


# if locked
sudo rm /var/lib/pacman/db.lck



# dangerous
gnome-terminal -- /bin/sh -c "sudo pacman -Syu ; echo Done - Press enter to exit; read _"

alacritty -e /bin/sh -c "sudo pacman -Syu ; echo Done - Press enter to exit; read _"

sudo pacman -Syuw

yay -Syu --devel

yay -Y --devel --save

aur sync -u && sudo pacman -Syu

yay -Sua

paru -Syyu (or) sudo pacman -Syyu



```

  

`.zshrc`
```
# Upgrade
alias y="yay"

# Search
alias ys="yay -Ss"

# Install
alias yi="yay -S"

# Remove
alias yr="yay -R"
```

Sudo vim bashrc  
`Alias update = ' echo "password" | sudo -S pacman -syu'`  
:wq