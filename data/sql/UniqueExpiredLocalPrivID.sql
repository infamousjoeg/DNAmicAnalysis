SELECT Accounts.Name, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('now')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge,
	AVG(Cast ((JulianDay(datetime('now')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as AvgPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet >= datetime('now', '-90 days')
	AND Accounts.AccountType = 'Local'
	AND OSGroupModel.Name = 'Administrators'
GROUP BY Accounts.Name