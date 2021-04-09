SELECT DISTINCT LOWER(Machines.Address) as MachineAddress
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Machines.Platform = 'Nix'
	AND Accounts.Name = 'root'
	AND OSAccounts.Enabled = {disabled}
GROUP BY MachineAddress
ORDER BY MachineAddress ASC