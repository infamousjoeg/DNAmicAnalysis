SELECT Services.AccountName
FROM Services
	LEFT OUTER JOIN Accounts
		ON Accounts.Name = Services.AccountName
		COLLATE nocase
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.accountbase_id
WHERE NOT (Services.AccountName LIKE '%*%'
		OR Services.AccountName LIKE ''
		OR Services.AccountName LIKE 'S-%')
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Services.AccountName), LOWER(Services.Address)
ORDER BY LOWER(Services.AccountName) ASC