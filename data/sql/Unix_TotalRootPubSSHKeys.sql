SELECT LOWER(Accounts.Name) as UserName
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
	AND SshKeys.SshKeyType = 'Public'
	AND Accounts.Name = 'root'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Machines.Address)
ORDER BY UserName ASC