SELECT Accounts.Name, HCPA.Name
FROM HardCodedPasswordAccounts AS HCPA
	LEFT OUTER JOIN Accounts
		ON Accounts.Id = HCPA.WebAppAccount_id
WHERE NOT (Accounts.Name LIKE '')
GROUP BY LOWER(Accounts.Name)
ORDER BY Accounts.Name ASC