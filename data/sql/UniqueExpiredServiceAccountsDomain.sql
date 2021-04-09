SELECT Accounts.BasePath, OSAccounts.LastPasswordSet, Machines.Address,
	COUNT(DISTINCT Machines.Address) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Services
	LEFT OUTER JOIN Accounts
		ON Services.IAccount_id = Accounts.Id
		COLLATE nocase
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.accountbase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%')
	AND (Services.AccountType = 'Domain'
		OR Accounts.AccountType = 'Domain')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Machines.Address), LOWER(Accounts.Name)
ORDER BY PasswordAge DESC