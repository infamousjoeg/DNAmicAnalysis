SELECT Name,
	MAX(Cast ((JulianDay(datetime('{scanDateTime}')) - JulianDay(LastPasswordSet)) As Integer)) as PasswordAge
FROM SPN
WHERE Compliant = 1
	AND NOT (Name LIKE '%*%'
		OR Name LIKE ''
		OR Name LIKE 'S-%')
	{disabled}
GROUP BY LOWER(Name)
ORDER BY PasswordAge DESC