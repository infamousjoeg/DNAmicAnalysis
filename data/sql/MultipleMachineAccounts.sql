SELECT Accounts.Name, COUNT(DISTINCT Machines.Address) as TotalFound
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND (OSGroupModel.Name LIKE 'Administrators'
		OR OSGroupModel.Name LIKE 'Power Users')
	AND Accounts.AccountType != 'Local'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
HAVING TotalFound > 1
ORDER BY TotalFound DESC