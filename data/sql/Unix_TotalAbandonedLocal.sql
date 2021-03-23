SELECT LOWER(Accounts.Name) as UserName
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Accounts.AccountType = 'Local'
	AND NOT Accounts.Name = 'root'
	AND Machines.Platform = 'Nix'
	AND OSAccounts.Enabled = {disabled}
GROUP BY UserName
ORDER BY UserName ASC