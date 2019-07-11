SELECT SPN.Name,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(SPN.LastPasswordSet)) As Integer)) as PasswordAge
FROM SPN
	LEFT OUTER JOIN Accounts
		ON Accounts.Name = SPN.Name
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDateTime}', '-90 days')
	AND NOT (SPN.Name LIKE '%*%'
		OR SPN.Name LIKE ''
		OR SPN.Name LIKE 'S-%')
	{disabled}
GROUP BY LOWER(SPN.Name)
ORDER BY PasswordAge DESC