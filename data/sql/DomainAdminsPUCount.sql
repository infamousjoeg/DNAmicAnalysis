SELECT CAST(COUNT(Accounts.Name) as INTEGER) as Count
FROM Accounts
	LEFT JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE Accounts.AccountType != 'Local'
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
GROUP BY Accounts.Id, Accounts.Name
ORDER BY Count DESC