from typing import List
import requests

urlAPI = "https://5f768ad6fdffe3001637fd5f.mockapi.io/api/TaskDummy"
req = requests.get(urlAPI)
Myreq = req.json()

class DTOMission:
    def __init__(self,Id,Title,Description,StartDate,EndDate,State,Limit,Point):
        self.Id = Id
        self.Title = Title
        self.Description = Description
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.StartDate = StartDate
        self.State = State
        self.Limit = Limit
        self.Point = Point
# for dto in Myreq:
#     dto1 = DTOMission(dto['id'],dto['Title'],dto['Description'],dto['StartDate'],dto['EndDate'], \
#        dto['State'],dto['Limit'],dto['Point'] )
#     print(dto1.Id)

