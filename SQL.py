SQLCHECKPASS = 'SELECT Employee_Id,Email,Password FROM employee WHERE Email = %s and Password= %s and Status = 1'
SQLCHECKBLOCK = 'SELECT Email,Password FROM employee WHERE Email = %s and Password= %s and Status = 0'
SQLCHECKEMAIL = 'SELECT Email FROM employee WHERE Email = %s'
#Mission management
SQLMISSION = 'select Mission_Id,Title,Description,StartDate,EndDate,State,`Limit`,Point from mission'

SQLVIEWMISSI = 'SELECT  ROW_NUMBER() OVER(Order by employee.Email) as STT,employee.Name, employee.Email, \
 employee.POINT, process.status from process,employee where process.Employee_Id=employee.Employee_Id   \
and Mission_Id = %s'

SQLVIEWMISS = ' SELECT  ROW_NUMBER() OVER(Order by employee.Email) as STT,employee.Name, employee.Email,\
employee.POINT,process.status,mission.Title from mission, process,employee where\
 process.Employee_Id=employee.Employee_Id and mission.Mission_Id=process.Mission_Id and process.Mission_Id = %s'

SQLINSERTMISSION = 'INSERT INTO `cts`.`mission` (`Title`, `Description`, `StartDate`, `EndDate`, `Limit`, `Point`)  VALUES (%s, %s, %s,%s,%s,%s)'
SQLUPDATEMISS1 = 'UPDATE `cts`.`mission` SET State =%s, `Title` = %s, `Description` = %s, `StartDate` = %s, `EndDate` = %s, `Limit` = %s, `Point` = %s \
                WHERE (`Mission_Id` = %s)'
SQLUPDATEMISS0 = 'UPDATE `cts`.`mission` SET State =%s, `Title` = %s, `Description` = %s, `StartDate` = %s, `EndDate` = %s, `Limit` = %s, `Point` = %s \
                WHERE (`Mission_Id` = %s)'
SQLDELETEMISS = 'DELETE from mission WHERE Mission_Id=%s'
# REGISTER
SQLREGISTER = 'INSERT INTO employee (Email,Password) VALUES (%s,%s)'
SQLSELECTEMAIL = 'SELECT Email FROM Employee WHERE Email = %s'
#UPDATE PASSOWRD
SQLUPDATEPSW = 'UPDATE employee SET password=%s WHERE Email=%s'
#LOCK ACCOUNT
SQLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
SQLUNLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
#Mission User
SQLVIEWMISSUSER = 'SELECT Mission_Id, Title, Description, StartDate,EndDate,mission.Limit ,Point, State\
    FROM cts.Mission ORDER BY Mission_Id ASC'
SQLTAKEMISSION = 'INSERT INTO `cts`.`process` (`Employee_Id`, `Mission_Id`, `status`) VALUES (%s,%s,%s)'
SQLVALIDATE = "SELECT Employee_Id,Mission_Id FROM cts.process WHERE Employee_Id =%s and Mission_Id=%s"
SQLGETEMP_ID = "SELECT Employee_Id FROM cts.employee where Email=%s"
SQLUPDATEMISSION = "UPDATE cts.mission SET mission.Limit=mission.Limit-1 where Mission_Id=%s"
