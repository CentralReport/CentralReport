# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.define "cr_debian_squeeze_64" do |cr_debian_squeeze_64|
    cr_debian_squeeze_64.vm.box = "cr_debian_squeeze_64"
    cr_debian_squeeze_64.vm.box_url = "http://static.centralreport.net/vagrant/debian_squeeze_64.box"
  end

  config.vm.define "cr_centos_6_4_64" do |cr_centos_6_4_64|
    cr_centos_6_4_64.vm.box = "cr_centos_6_4_64"
    cr_centos_6_4_64.vm.box_url = "http://static.centralreport.net/vagrant/centos_6_4_64.box"
  end

  config.vm.define "cr_ubuntu_server_12_04_64" do |cr_ubuntu_server_12_04_64|
    cr_ubuntu_server_12_04_64.vm.box = "cr_ubuntu_server_12_04_64"
    cr_ubuntu_server_12_04_64.vm.box_url = "http://static.centralreport.net/vagrant/ubuntu_server_12_04_x64.box"
  end
end
