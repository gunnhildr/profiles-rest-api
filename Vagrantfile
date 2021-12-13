# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
 # The most common configuration options are documented and commented below.
 # For a complete reference, please see the online documentation at
 # https://docs.vagrantup.com.

 # Every Vagrant development environment requires a box. You can search for
 # boxes at https://vagrantcloud.com/search.
 config.vm.box = "ubuntu/bionic64"
 config.vm.box_version = "~> 20191107.0.0"

  # create a shared folder for the top-level project directory at /vagrant
  # normally already configured but for some reason it isn't on these boxes
  # https://www.vagrantup.com/docs/synced-folders/virtualbox.html#automount
  # http://www.virtualbox.org/manual/ch04.html#sf_mount_auto
  config.vm.synced_folder ".", "/vagrant", id: "vagrant", automount: true
  config.vm.provision "shell", inline: "usermod -a -G vboxsf vagrant"
  config.vm.provision "shell", inline: "ln -sf /media/sf_vagrant /vagrant"

 config.vm.network "forwarded_port", guest: 8000, host: 8000

 config.vm.provision "shell", inline: <<-SHELL
   systemctl disable apt-daily.service
   systemctl disable apt-daily.timer
   sudo apt-get update
   sudo apt-get install -y python3-venv zip
   mount -a
   touch /home/vagrant/.bash_aliases
   if ! grep -q PYTHON_ALIAS_ADDED /home/vagrant/.bash_aliases; then
     echo "# PYTHON_ALIAS_ADDED" >> /home/vagrant/.bash_aliases
     echo "alias python='python3'" >> /home/vagrant/.bash_aliases
   fi
 SHELL
end