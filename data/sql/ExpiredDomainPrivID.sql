SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	COUNT(Accounts.Name) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND Accounts.AccountType != 'Local'
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY PasswordAge DESC