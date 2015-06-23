# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.define :develop do |develop|
	  develop.vm.provision :shell, :path => './init.sh'
	  develop.vm.hostname = "codeforleipzig"
  end
end
