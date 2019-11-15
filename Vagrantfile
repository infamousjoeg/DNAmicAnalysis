Vagrant.configure("2") do |config|

  # Local VM deployment
  config.vm.define "local" do |local|
    local.vm.box = "centos/7"
    local.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
    local.vm.provision "shell", privileged: false, inline: <<-SHELL
      echo "[ Updating CentOS 7 ]"
      echo "This may take a few minutes..."
      sudo yum install epel-release -y -q -e 0
      sudo yum update -y -q -e 0
      echo "[ Installing Python 3.6 ]"
      sudo yum install python36 -y -q -e 0
      echo "[ Upgrading pip ]"
      sudo python3 -m pip install --upgrade pip
      echo "[ Installing DNAmic Analysis Dependencies ]"
      sudo python3 -m pip install -r /vagrant/requirements.txt
    SHELL
  end

  # AWS EC2 Instance deployment
  config.vm.define "ec2" do |ec2|
    ec2.vm.box = "dummy"
    ec2.vm.provider :aws do |aws, override|
      aws.keypair_name = ENV["AWS_KEY_PAIR"]
      aws.subnet_id = ENV["AWS_SUBNET_ID"]
      aws.security_groups = [ENV["AWS_SECURITY_GROUP"]]
      aws.region = ENV["AWS_REGION"]
      aws.ami = "ami-02eac2c0129f6376b"
      aws.instance_type = "t2.micro"
      aws.tags = {
        'Name' => 'DNAmic Analysis',
        'role' => 'test'
      }
      override.ssh.username = "centos"
      override.ssh.private_key_path = ENV["AWS_PRIVATE_KEY_PATH"]
    end
    config.vm.synced_folder ".", "/vagrant", disabled: false, type: 'rsync'
  end
end
