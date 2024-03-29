SELECT BasePath,
	COUNT(Name) as NumMachines,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(LastPasswordSet)) As Integer)) as PasswordAge
FROM SPN
WHERE LastPasswordSet <= datetime('{scanDateTime}', '-{expirationDays} days')
	AND NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%')
	AND Enabled = {disabled}
GROUP BY LOWER(Name)
ORDER BY LOWER(Name) ASC