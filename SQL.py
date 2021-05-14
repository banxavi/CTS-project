#Mission management
SQLMISSION = 'select Mission_Id,Title,Description,StartDate,EndDate,State,`Limit`,Point,ROW_NUMBER() OVER(Order by mission.Mission_Id desc) as STT,curdate() from mission'

SQLVIEWMISSI = 'SELECT  ROW_NUMBER() OVER(Order by employee.Email) as STT,employee.Name, employee.Email, \
 employee.POINT, process.status from process,employee where process.Employee_Id=employee.Employee_Id   \
and Mission_Id = %s'

SQLVIEWMISS = ' SELECT  ROW_NUMBER() OVER(Order by employee.Email) as STT,employee.Name, employee.Email,\
employee.POINT,process.status,mission.Title ,employee.Image,DATEDIFF(mission.EndDate,curdate()) as FinalDay from mission, process,employee where\
 process.Employee_Id=employee.Employee_Id and mission.Mission_Id=process.Mission_Id and process.Mission_Id = %s'

SQLINSERTMISSION = 'INSERT INTO `cts`.`mission` (Mission_Id,`Title`, `Description`, `StartDate`, `EndDate`, `Limit`, `Point`,LimitDefault) \
  VALUES (%s,%s, %s, %s,%s,%s,%s,%s)'
SQLUPDATEMISS1 = 'UPDATE `cts`.`mission` SET State =%s, `Title` = %s, `Description` = %s, `StartDate` = %s, `EndDate` = %s, `Limit` = %s, `Point` = %s, \
               State=1 WHERE (`Mission_Id` = %s)'
SQLUPDATEMISS0 = 'UPDATE `cts`.`mission` SET State =%s, `Title` = %s, `Description` = %s, `StartDate` = %s, `EndDate` = %s, `Limit` = %s, `Point` = %s ,\
                State=0 WHERE (`Mission_Id` = %s)'
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
employee on employee.Employee_Id = process.Employee_Id where process.Status = %s \
and employee.Email = %s'
SQLMAXPOINT = 'SELECT max(Point) from employee'
#HOME ADMIN SQL SELECT 
SQLHOMECOUNTEMPL = 'select  count(employee.Employee_Id),sum(Point)  from Employee'
SQLHOMECOUNTMISS='select count(mission.Mission_Id) from mission'
#MANAGEMENT LOCK ACCOUNT
SQLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
SQLUNLOCKACC = 'UPDATE employee SET Status = %s WHERE Employee_Id = (%s)'
# SHOW MISSION AVAIABLE
SQLMISSION1 = 'select Mission_Id,Title,Description,StartDate,EndDate,State,`Limit`,Point,ROW_NUMBER() OVER(Order by mission.Mission_Id DESC) as STT from mission where State=1 and `Limit` > 0 and curdate() < EndDate '

# SHOW MISSION OF USER
SQLMISSIONUSER ='select   process.Process_Id, mission.Mission_Id, mission.Title \
                ,mission.Description,mission.StartDate,mission.EndDate , mission.Point , \
                process.Status,ROW_NUMBER() OVER(Order by mission.Mission_Id DESC)  as STT  from employee, mission, process\
                where process.Employee_Id=employee.Employee_Id and \
                process.Mission_Id=mission.Mission_Id \
                and employee.Email = %s' 
SQLEXPORTEXCEL = "SELECT Employee_Id,Email,Name,Point,Status FROM employee"
SQLCANCELMISSION = "UPDATE process set Status = 0 where Process_Id = %s"
SQLUPDATELIMIT = "UPDATE mission inner join process\
                        on process.Mission_Id = mission.Mission_Id\
                        set mission.Limit = mission.Limit + 1 where process.Process_Id = %s"
SQLUPDATEPOINT = "Update cts.process inner join cts.employee\
                        on employee.Employee_Id = process.Employee_Id\
                        inner join cts.mission on mission.Mission_Id = process.Mission_Id\
                        set employee.Point = employee.Point - mission.Point*0.1 where process.Process_Id = %s"
SQLCOMPLETEMISSION ="UPDATE process set Status = 2 where Process_Id = %s"
SQLUPDATEDONE_POINT = "Update cts.process inner join cts.employee\
                        on employee.Employee_Id = process.Employee_Id\
                        inner join cts.mission on mission.Mission_Id = process.Mission_Id\
                        set employee.Point = employee.Point + mission.Point where process.Process_Id = %s"
# SCHEDULE MISSION
SQLTASKSCHEDULE = "select mission.Mission_Id, Mission.Title , \
schedule.Schedule_Id, schedule.DateLoop, schedule.UnitLoop from mission ,\
 schedule where schedule.Mission_Id = mission.Mission_Id"
# UPDATE SCHEDULE
SQLUPDATESCHEDULE='update schedule set DateLoop = %s , UnitLoop = %s \
     where Mission_Id = %s'
# MAX ID
SQLMAXID='SELECT MAX(Mission_Id) AS MAXID FROM Mission'
# ADD SCHEDULE NEW TASK
SQLINSERTSCHEDULE = 'INSERT INTO `cts`.`schedule` \
     (`Mission_Id`, `DateLoop`, `UnitLoop`) VALUES (%s,%s,%s)'
#LOOP AUTO
SQLLOOP = 'select mission.Mission_Id,DateLoop*UnitLoop as NumberDay, CurrentDate,datediff(EndDate,StartDate) from Mission \
inner join Schedule where mission.Mission_Id=Schedule.Mission_Id and DateLoop >0 '
SQLUPDATETLOOPMIS = 'UPDATE `cts`.`mission` SET  startdate=%s, enddate=%s, `State` = %s, mission.Limit=mission.LimitDefault   WHERE (`Mission_Id` = %s)'
SQLCURRENTDATE = 'UPDATE `cts`.`schedule` SET `CurrentDate` = CurrentDate+1 where Mission_Id=%s '
#SHOW MISSION OF USER by ID
SQLSHOWUSERMISSION="Select ROW_NUMBER() OVER(Order by mission.Mission_Id desc) as STT , mission.Title,mission.Point, process.status\
                    ,mission.EndDate,DATEDIFF(mission.EndDate,curdate()) as FinalDay From((cts.employee\
	                    Inner join cts.process on process.Employee_Id = employee.Employee_Id )\
	                    Inner join cts.mission on process.Mission_Id = mission.Mission_Id)\
                        where employee.Employee_Id = %s"
SQLSHOWNAMEOFUSER = "Select employee.Name from cts.employee where employee.Employee_Id=%s"   

#UPDATE PASSOWRD
SQLPASSWORD = 'SELECT employee.Password FROM employee WHERE Email= %s'
SQLUPDATEPASSWORD = 'UPDATE employee SET Password= %s WHERE Email= %s'
#Take Mission and Validate
SQLTAKEMISSION = 'INSERT INTO `cts`.`process` (`Employee_Id`, `Mission_Id`, `status`) VALUES (%s,%s,%s)'
SQLVALIDATE = "SELECT Employee_Id,Mission_Id FROM cts.process WHERE Employee_Id =%s and Mission_Id=%s"
SQLVALIDATE_CANCEL = "SELECT Employee_Id,Mission_Id FROM cts.process WHERE Employee_Id =%s and Mission_Id=%s and Status =0"
SQLVALIDATE_COMPLETE = "SELECT Employee_Id,Mission_Id FROM cts.process WHERE Employee_Id =%s and Mission_Id=%s and Status =2"
SQLGETEMP_ID = "SELECT Employee_Id FROM cts.employee where Email=%s"
SQLUPDATEMISSION = "UPDATE cts.mission SET mission.Limit=mission.Limit-1 where Mission_Id=%s"  
#Show point done
SQLPOINTDONE = "select  mission.Title ,mission.EndDate , mission.Point \
            from employee, mission, process\
                where process.Employee_Id=employee.Employee_Id and \
                process.Mission_Id=mission.Mission_Id \
                and employee.Email = %s and process.Status =2"