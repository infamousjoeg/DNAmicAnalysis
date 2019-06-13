SELECT Accounts.Name
FROM Accounts
	LEFT OUTER JOIN OSGroupModel
		ON Accounts.Id = OSGroupModel.OSAccount_id
WHERE Accounts.AccountType = 'Domain'
	AND Accounts.Name NOT LIKE '%*%'
	AND OSGroupModel.DomainGroup LIKE '%Domain Admins%'
    AND (Accounts.Name LIKE '%svc%'
        OR Accounts.Name LIKE '%service%')
GROUP BY Accounts.Name
ORDER BY Accounts.Name ASC