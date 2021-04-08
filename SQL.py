#Mission management
SQLMISSION = 'select Mission_Id,Title,Description,StartDate,EndDate,State,`Limit`,Point from mission'
SQLVIEWMISS = 'select employee.Name, employee.email from process,employee where  process.Employee_Id=employee.Employee_Id \
        and Mission_Id = %s'
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

#USER
SQLSHOWUSERMISSION = 'SELECT process.Process_Id, mission.Mission_Id, mission.Title\
          ,mission.Description,mission.Startdate,mission.Enddate , mission.Point , \
           process.Status  from process\
           inner join employee on employee.Employee_Id = process.Employee_Id\
           inner join mission on process.Mission_Id = mission.Mission_Id\
           where employee.Email = (%s)'