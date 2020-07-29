SELECT Accounts.Name, WindowsAccounts.CausesVulnerabilityOnXOfMachines, Machines.Address,
	CASE Machines.ProductType WHEN 'Workstation' THEN 1 ELSE 0 END AS Workstation,
	CASE Machines.ProductType WHEN 'Server' THEN 1 ELSE 0 END AS Server,
	(SELECT SUM(IsPrivileged) FROM Accounts AS A1 WHERE A1.Name = Accounts.Name) AS PrivilegedCount,
	COUNT(Accounts.Name) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(OSAccounts.LastPasswordSet)) As Integer)) as PasswordAge
FROM Accounts
	LEFT OUTER JOIN WindowsAccounts
		ON WindowsAccounts.OSAccount_id = Accounts.Id
	LEFT OUTER JOIN OSAccounts
		ON WindowsAccounts.OSAccount_id = OSAccounts.AccountBase_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE NOT (Accounts.Name LIKE '%*%'
		OR Accounts.Name LIKE ''
		OR Accounts.Name LIKE 'S-%')
	AND WindowsAccounts.CausesVulnerabilityOnXOfMachines > 0
	AND PrivilegedCount > 0
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
	AND OSAccounts.Enabled = {disabled}
GROUP BY LOWER(Accounts.Name) 
ORDER BY LOWER(Accounts.Name) ASC