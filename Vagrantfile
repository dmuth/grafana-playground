# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    #config.vm.box = "hashicorp/bionic64"
    config.vm.box = "ubuntu/focal64" # 20.04.5 LTS

    config.vm.provider "virtualbox" do |vb|
        # Display the VirtualBox GUI when booting the machine
        #vb.gui = true
        vb.memory = "1024"
        #vb.cpus = "2"
        vb.cpus = "4"
    end

    config.vm.network "forwarded_port", guest: 3000, host: 3000, host_ip: "127.0.0.1"
    config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
    config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

    config.vm.provision "shell", path: "bin/vagrant-provision.sh"


# TODO:
# X CPUs
# X Test docker within
# Figure out Docker hanging
#   the promtail process seems to be hanging...
#   ...separate problem with Loki...?
#   ...I think the issue might be with the driver...
#
# TODO2:
# - I'll need to remove the driver from all files, and put a blurb in the README as well
# - I also need to put an info on the "docker logs" dashboard...
#
#
# - Shell script to do provisioning
# - Share directories
#   - Can I do environment variables?
#   - If not, I'll have to do a shellscript to stand it up...
# - Access Docker remotely!


end


