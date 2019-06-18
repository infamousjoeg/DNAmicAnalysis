SELECT Accounts.Name, Machines.Address, OSAccounts.LastPasswordSet,
	MAX(Cast ((JulianDay(datetime('2019-05-21 20:57:43')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as MaxPasswordAge,
	AVG(Cast ((JulianDay(datetime('2019-05-21 20:57:43')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as AvgPasswordAge
FROM Accounts
	LEFT OUTER JOIN OSAccounts
		ON Accounts.Id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE OSAccounts.LastPasswordSet <= datetime('2019-05-21 20:57:43', '-90 days')
	AND Accounts.AccountType = 'Domain'
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
GROUP BY Accounts.Name