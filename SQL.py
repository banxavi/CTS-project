#Mission management
SQLMISSION = 'select Mission_Id,Title,Description,StartDate,EndDate,State,`Limit`,Point,ROW_NUMBER() OVER(Order by mission.Mission_Id) as STT from mission'

SQLVIEWMISSI = 'SELECT  ROW_NUMBER() OVER(Order by employee.Email) as STT,employee.Name, employee.Email, \
 employee.POINT, process.status from process,employee where process.Employee_Id=employee.Employee_Id   \
and Mission_Id = %s'

SQLVIEWMISS = ' SELECT  ROW_NUMBER() OVER(Order by employee.Email) as STT,employee.Name, employee.Email,\
employee.POINT,process.status,mission.Title ,employee.Image from mission, process,employee where\
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
SQLUPDATEPSW = 'UPDATE employee SET Password=%s WHERE Email=(%s)'
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
SQLIMAGE = "select Image,Point from employee where Email=%s"
#USER MANAGEMENT
SQLUSERMANA = 'Select Employee_Id, Name, Email,Image,Status,Point, ROW_NUMBER() OVER(Order by employee.Name) as STT from cts.employee '
# HOME USER SELECT
SQLHOMEUSER1 ='SELECT count(process.Process_Id) \
from process inner join \
employee on employee.Employee_Id = process.Employee_Id where process.Status = "1" \
and employee.Email = %s'
SQLHOMEUSER2 ='SELECT count(process.Process_Id) \
from process inner join \
employee on employee.Employee_Id = process.Employee_Id where process.Status = "2" \
and employee.Email = %s'
#HOME ADMIN SQL SELECT 
SQLHOMECOUNTEMPL = 'select count(employee.Employee_Id) from Employee'
SQLHOMECOUNTMISS='select count(mission.Mission_Id) from mission'
#MANAGEMENT LOCK ACCOUNT
SQLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
SQLUNLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
# SHOW MISSION AVAIABLE
SQLMISSION1 = 'select Mission_Id,Title,Description,StartDate,EndDate,State,`Limit`,Point,ROW_NUMBER() OVER(Order by mission.Mission_Id) as STT from mission where State=1'
# SHOW MISSION OF USER
SQLMISSIONUSER ='select   process.Process_Id, mission.Mission_Id, mission.Title \
                ,mission.Description,mission.StartDate,mission.EndDate , mission.Point , \
                process.Status,ROW_NUMBER() OVER(Order by mission.Mission_Id)  as STT  from employee, mission, process\
                where process.Employee_Id=employee.Employee_Id and \
                process.Mission_Id=mission.Mission_Id \
                and employee.Email = %s'
<<<<<<< HEAD
#SHOW MISSION OF USER by ID
SQLSHOWUSERMISSION="Select employee.Employee_Id, mission.Mission_Id, mission.Title,mission.Point, process.status\
                        ,DATEDIFF(mission.EndDate,curdate()) as FinalDay\
	                    From((cts.employee\
	                    Inner join cts.process on process.Employee_Id = employee.Employee_Id )\
	                    Inner join cts.mission on process.Mission_Id = mission.Mission_Id)\
                        where employee.Employee_Id = %s"
SQLSHOWNAMEOFUSER = "Select employee.Name from cts.employee where employee.Employee_Id=%s"
       
=======
SQLEXPORTEXCEL = "SELECT Employee_Id,Email,Name,Point,Status FROM employee"
>>>>>>> babd344e0a532047488cf7fb5e106fd916b9109b
