SELECT Accounts.Name, Machines.Address
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE Accounts.AccountType = 'Local'
	AND NOT (OSAccounts.Description LIKE 'Built-in account for administering the computer/domain'
		OR Accounts.Name = 'Administrator')
	AND (OSGroupModel.Name LIKE 'Administrators'
		OR OSGroupModel.Name LIKE 'Power Users')
	{disabled}
GROUP BY LOWER(Accounts.Name)