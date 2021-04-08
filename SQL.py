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
SQLSELECTACCOUNT = 'SELECT Email, Password FROM employee WHERE email = %s AND password = %s'
SQLSELECTADMIN = 'SELECT * FROM employee WHERE Email = %s'
#UPDATE PASSOWRD
SQLUPDATEPSW = 'UPDATE employee SET password=%s WHERE Email=%s'
#LOCK ACCOUNT
SQLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
SQLUNLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
#LOGINACCOUNT
SQLCHECKPASS = 'SELECT Email,Password FROM employee WHERE Email = %s and Password= %s and Status = 1'
SQLCHECKBLOCK = 'SELECT Email,Password FROM employee WHERE Email = %s and Password= %s and Status = 0'
#SHOWPROFILEUSER
SQLSHOWPROFILE = 'select Name,Email,Image,Point from employee where Email = %s'
SQLUPDATEPROFILE = 'Update cts.employee set Name = %s where Email=%s'
#SESSION IMAGE
SQLIMAGE = "select Image from employee where Email=%s"
