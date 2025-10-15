from dotenv import load_dotenv
import os

class Project:

    __TotalProjectNumber = 0
    __ProjectNamesSet = set()

    def __init__(self, ProjectName = None, ProjectDescription = None):
        load_dotenv()
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 30))
        if self.__class__.__TotalProjectNumber > max_projects:
            raise Exception(f"Cannot create more than {max_projects} projects.")

        self._ProjectName = None
        self._ProjectDescription = None

        if ProjectName:
            self.ProjectName = ProjectName
        if ProjectDescription:
            self.ProjectDescription = ProjectDescription


    @property
    def ProjectName(self):
        return self._ProjectName

    @ProjectName.setter
    def ProjectName(self, value):

        if value in self.__class__.__ProjectNamesSet:
            raise ValueError("ProjectName must be unique.")
        else:
            self.__class__.__ProjectNamesSet.add(value)
            if self._ProjectName != None:
                self.__class__.__ProjectNamesSet.remove(self._ProjectName)

        if len(value) <= 30:
            self._ProjectName = value
        else:
            raise ValueError("ProjectName must be 30 characters or fewer.")


    @property
    def ProjectDescription(self):
        return self._ProjectDescription

    @ProjectDescription.setter
    def ProjectDescription(self, value):
        if len(value) <= 150:
            self._ProjectDescription = value
        else:
            raise ValueError("ProjectDescription must be 100 characters or fewer.")



    def __str__(self):
        return "Project: " + self.ProjectName + " - " + self.ProjectDescription


    def setName(self, new_name):
        if self.ProjectName in self.__class__.__ProjectNamesSet:
            self.__class__.__ProjectNamesSet.remove(self.ProjectName)

        if new_name in self.__class__.__ProjectNamesSet:
            raise ValueError("ProjectName must be unique.")
        else:
            self.ProjectName = new_name
            self.__class__.__ProjectNamesSet.add(self.ProjectName)


    def setDescription(self, new_description):
        self.ProjectDescription = new_description


    def remove(self):
        if self.ProjectName in self.__class__.__ProjectNamesSet:
            self.__class__.__ProjectNamesSet.remove(self.ProjectName)

        self.__class__.__TotalProjectNumber -= 1
        del self


