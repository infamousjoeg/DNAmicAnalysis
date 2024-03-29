SELECT Services.AccountName,
	MAX(Cast ((JulianDay(datetime('2019-05-21 20:57:43')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Services
	LEFT OUTER JOIN Accounts
		ON Accounts.Id = Services.IAccount_id
		COLLATE nocase
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.accountbase_id
WHERE NOT (Services.AccountName LIKE '%*%'
		OR Services.AccountName LIKE ''
		OR Services.AccountName LIKE 'S-%')
	AND OSAccounts.Enabled = 1
GROUP BY LOWER(Services.AccountName), LOWER(Services.Address)
ORDER BY LOWER(Services.AccountName) ASC