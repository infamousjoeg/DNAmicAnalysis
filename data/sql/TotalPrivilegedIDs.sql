SELECT DISTINCT Accounts.Name
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON OSGroupModel.OSAccount_id = Accounts.Id
	LEFT OUTER JOIN OSAccounts
		ON OSAccounts.AccountBase_id = Accounts.Id
WHERE (OSGroupModel.Name = 'Administrators'
	OR OSGroupModel.Name = 'Power Users')
	AND NOT Accounts.Name LIKE 'S-%'
	{disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY LOWER(Accounts.Name) ASC