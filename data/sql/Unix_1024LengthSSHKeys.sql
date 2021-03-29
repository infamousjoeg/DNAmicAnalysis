SELECT Accounts.Name, Machines.Address,
	COUNT(DISTINCT Machines.Address) as NumMachines
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN SshData
		ON OSAccounts.SshData_id = SshData.Id
	LEFT OUTER JOIN SshKeys
		ON SshData.Id = SshKeys.SshData_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Machines.Platform = 'Nix'
	AND Accounts.IsPrivileged = 1
	AND SshKeys.KeyType != ''
	AND (SshKeys.KeyLength = '1023' OR SshKeys.KeyLength = '1024')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Machines.Address)