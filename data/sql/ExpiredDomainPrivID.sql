SELECT Accounts.Name, Accounts.Address, Accounts.AccountType, Accounts.IsPrivileged,
	OSAccounts.DisplayName, OSAccounts.LastPasswordSet, OSAccounts.PasswordNeverExpires,
	OSGroupModel.Name, OSGroupModel.Address,
	OSGroupModel.DomainGroup, Machines.IpAddress, Machines.ScanResult,
	Machines.Caption as OSVersion
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet >= datetime('now', '-90 days')
	AND Accounts.AccountType != 'Local'
	AND (OSGroupModel.Name = 'Administrators'
OR OSGroupModel.Name = 'Remote Desktop Users')