mkdir -p /home/${VAGRANT_USERNAME:=vagrant}/DNAmicAnalysis
git clone https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/infamousjoeg/DNAmicAnalysis.git /home/$VAGRANT_USERNAME/DNAmicAnalysis
chown -R $VAGRANT_USERNAME:$VAGRANT_USERNAME /home/$VAGRANT_USERNAME/DNAmicAnalysis
apt-get install python3-pip -y
pip3 install -r /home/$VAGRANT_USERNAME/DNAmicAnalysis/requirements.txt --user