mkdir -p /home/${VAGRANT_USERNAME:=vagrant}/DNAmicAnalysis
git clone https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/infamousjoeg/DNAmicAnalysis.git /home/$VAGRANT_USERNAME/DNAmicAnalysis
sudo apt-get install python3.7 python3-pip -y
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
sudo update-alternatives --config python3 <<< 2
export PATH=/home/$VAGRANT_USERNAME/.local/bin:$PATH
pip3 install --upgrade pip
pip3 install -r /home/$VAGRANT_USERNAME/DNAmicAnalysis/requirements.txt