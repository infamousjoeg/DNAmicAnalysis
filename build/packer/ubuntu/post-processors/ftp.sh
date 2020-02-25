ftp -n $FTP_HOSTNAME <<EOF
quote USER $FTP_USERNAME
quote PASS $FTP_PASSWORD
passive
binary
cd csworld/CSD
put $FILE_NAME
cd ../../seworld/vapp_distribution/DNAmic_Analysis
put $FILE_NAME
quit
EOF
exit 0