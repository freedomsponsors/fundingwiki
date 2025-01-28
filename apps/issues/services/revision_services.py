from django.db import models
import json

class RevisionStandard:
    '''
    Model to standarize revisions class
    Used for diff system
    '''

    def __init__(self, eventDate=None, key=0):
        # Key pair values to compare. Where key is the field name to compare
        # For example if you want to compare a solution you can add:
        # from: "Title": "title"
        # to: "Title": "title"
        # Then will compare on the frontend each key.
        self.changes = dict()

        self.eventDate = models.DateTimeField()
        self.eventDate=eventDate
        self.key=key

    def addChange(self, key, val):
        self.changes[key] = val

    # Compare self with another revision standard and return an object with the comparations
    # This merge the two changes dicts creating a json like:
    # {
    #     changeTitle: {from: blahblah, to: blihblih}
    #     thisOnlyOnFrom: {from: blahblah}
    #     thisOnlyOnTo: {from: blihblih}
    # }
    def compare(self, revisionStandard):
        comparations = dict()
        for change in self.changes:
            comparations[change] = {"from": self.changes[change]}
        for change in revisionStandard.changes:
            if change in self.changes:
                comparations[change].update({"to": revisionStandard.changes[change]})
            else:
                comparations[change] = {"to": self.changes[change]}
        return comparations


# Get standard revision class for TechSolutionObjects
def getTechSolutionToStandard(techSolution):
    # Instantiate the revision standard class
    revision = RevisionStandard(
        eventDate=techSolution.creationDate,
        key=techSolution.id
    )
    # Add the changes to show on the diff
    revision.addChange("title", techSolution.title)
    revision.addChange("content", techSolution.content)
    return revision

# Get standard revision class for IssueObjects
def getIssueToStandard(issue):
    revision = RevisionStandard(
        eventDate=issue.creationDate,
        key=issue.id
    )
    revision.addChange("Description", issue.description)
    return revision


# Return serialized object from specific Serializer class from a serialized json object
def serializeJson(jsonObj, Serializer, pk=None):
    serializer = Serializer(data=json.loads(jsonObj))
    if serializer.is_valid():
        obj = serializer.generate()
        if pk is not None: obj.id = pk
        return obj