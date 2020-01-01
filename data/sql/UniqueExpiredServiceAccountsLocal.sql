SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge,
	Services.Address
FROM Services
	LEFT OUTER JOIN Accounts
		ON Services.AccountName = Accounts.Name
		COLLATE nocase
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.accountbase_id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-90 days')
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%')
	AND NOT Accounts.AccountType = 'Domain'
	{disabled}
GROUP BY LOWER(Accounts.Name), LOWER(Services.Address)
ORDER BY PasswordAge DESC