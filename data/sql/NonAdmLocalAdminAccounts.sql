SELECT Accounts.Name, COUNT(Machines.Address) AS TotalMachines
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
WHERE Machines.ProductType = 'Server'
	AND NOT (Accounts.Name = ''
		OR Accounts.Name LIKE '%*%')
	AND NOT ({whereStmt})
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
	{disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY TotalMachines DESC