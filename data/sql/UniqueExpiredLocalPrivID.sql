SELECT LOWER(Accounts.Name), Machines.Address, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-90 days')
	AND Accounts.AccountType = 'Local'
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	{disabled}
GROUP BY Accounts.Id
ORDER BY LOWER(Accounts.Name) ASC