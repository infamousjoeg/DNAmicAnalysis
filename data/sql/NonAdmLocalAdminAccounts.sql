SELECT Accounts.Name, COUNT(Machines.Address) AS TotalMachines
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
	LEFT OUTER JOIN Machines
		ON Accounts.Machine_id = Machines.Id
WHERE NOT (Accounts.Name = ''
	OR Accounts.Name LIKE '%*%')
	AND NOT ({whereStmt})
	AND (OSGroupModel.Name = 'Administrators'
		OR OSGroupModel.Name = 'Power Users')
GROUP BY Accounts.Name
ORDER BY TotalMachines DESC