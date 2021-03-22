SELECT Accounts.Name, Machines.Address,
	COUNT(DISTINCT Machines.Address) as NumMachines
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN UnixAccounts
		ON OSAccounts.AccountBase_id = UnixAccounts.OSAccount_id
	LEFT OUTER JOIN SudoPrivileges
		ON UnixAccounts.OSAccount_id = SudoPrivileges.UnixAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Machines.Platform = 'Nix'
	AND SudoPrivileges.MisconfigurationReason != '0'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Machines.Address)