class CollegeSearchResult:
    def __init__(self, name, location, characteristics, graduation_rate, apy, sat):
        self.name = name
        self.location = location
        self.characteristics  = characteristics 
        self.graduation_rate = graduation_rate
        self.apy = apy
        self.sat = sat

    def __str__(self):
        return f"Name: {self.name}\nLocation: {self.location}\nCharacteristics: {self.characteristics}\nGraduation Rate: {self.graduation_rate}\nAPY: {self.apy}\nSAT: {self.sat}"

class CollegeProfile:
    def __init__(self, url, name, location, characteristics, graduation_rate, apy, sat, description, boardCode, similarColleges):
        self.url = url
        self.name = name
        self.location = location
        self.characteristics = characteristics
        self.graduation_rate = graduation_rate
        self.apy = apy
        self.sat = sat
        self.description = description
        self.boardCode = boardCode
        self.similarColleges = similarColleges

    def __str__(self):
        return f"Name: {self.name}\nLocation: {self.location}\nDescription: {self.description}"
