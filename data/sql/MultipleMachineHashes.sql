SELECT Accounts.Name,
	(SELECT COUNT(Machines.Address) FROM Machines
		LEFT OUTER JOIN Accounts AS A1
			ON Machines.Id = A1.Machine_id
		WHERE A1.Name = Accounts.Name) AS MachineCount,
	(SELECT SUM(IsPrivileged) FROM Accounts AS A1 WHERE A1.Name = Accounts.Name) AS PrivilegedCount,
	COUNT(Accounts.Name) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	OUTER LEFT JOIN WindowsAccounts
		ON WindowsAccounts.OSAccount_id = Accounts.Id
	OUTER LEFT JOIN OSAccounts
		ON WindowsAccounts.OSAccount_id = OSAccounts.AccountBase_id
	OUTER LEFT JOIN Machines
		ON Accounts.Machine_id = Machines.Id
	LEFT OUTER JOIN OSGroupModel
		ON OSGroupModel.OSAccount_id = Accounts.Id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE '')
	AND WindowsAccounts.CausesVulnerabilityOnXOfMachines > 0
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
	AND PrivilegedCount > 0
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name)
ORDER BY LOWER(Accounts.Name) ASC