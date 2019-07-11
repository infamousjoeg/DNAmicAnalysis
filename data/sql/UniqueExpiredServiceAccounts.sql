SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Services
	LEFT OUTER JOIN Accounts
		ON Accounts.Name = Services.AccountName
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.accountbase_id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-90 days')
	AND NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%')
	{disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY PasswordAge DESC