SELECT Accounts.Name, HCPA.Name,
	COUNT(Accounts.Name) as NumMachines
FROM HardCodedPasswordAccounts AS HCPA
	LEFT OUTER JOIN Accounts
		ON Accounts.Id = HCPA.WebAppAccount_id
WHERE NOT (Accounts.Name LIKE '')
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC