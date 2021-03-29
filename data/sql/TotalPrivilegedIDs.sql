SELECT DISTINCT Accounts.BasePath,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON OSGroupModel.OSAccount_id = Accounts.Id
	LEFT OUTER JOIN OSAccounts
		ON OSAccounts.AccountBase_id = Accounts.Id
WHERE (OSGroupModel.Name = 'Administrators'
	OR OSGroupModel.Name = 'Power Users')
	AND NOT Accounts.Name LIKE 'S-%'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY LOWER(Accounts.Name) ASC