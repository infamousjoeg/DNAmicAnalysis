SELECT Services.AccountName
FROM Services
	LEFT OUTER JOIN Accounts
		ON Accounts.Name = Services.AccountName
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.accountbase_id
WHERE NOT (Services.AccountName LIKE '%*%'
		OR Services.AccountName LIKE ''
		OR Services.AccountName LIKE 'S-%')
	{disabled}
GROUP BY LOWER(Services.AccountName)
ORDER BY LOWER(Services.AccountName) ASC