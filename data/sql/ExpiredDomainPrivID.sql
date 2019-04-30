SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('now')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge,
	AVG(Cast ((JulianDay(datetime('now')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as AvgPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE OSAccounts.LastPasswordSet >= datetime('now', '-90 days')
	AND Accounts.AccountType != 'Local'
	AND (OSGroupModel.Name = 'Administrators'
OR OSGroupModel.Name = 'Remote Desktop Users')
GROUP BY Accounts.Name