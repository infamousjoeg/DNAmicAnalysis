SELECT Accounts.Name, Machines.Address, OSAccounts.LastLogon,
	MAX(Cast ((JulianDay(datetime('{{scanDateTime}}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('{{scanDateTime}}', '-90 days')
	AND OSAccounts.LastLogon <= datetime('{{scanDateTime}}', '-1 year')
	AND Accounts.AccountType != 'Local'
	AND OSGroupModel.Name LIKE '%Domain Admins%'
GROUP BY Accounts.Id