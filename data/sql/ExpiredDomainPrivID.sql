SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('{scanDate}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge,
	AVG(Cast ((JulianDay(datetime('{scanDate}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as AvgPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE OSAccounts.LastPasswordSet <= datetime('{scanDate}', '-90 days')
	AND Accounts.AccountType != 'Local'
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
GROUP BY Accounts.Name