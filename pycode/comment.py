class Comment:

    #all the information concerning a comment
    def __init__(self, beer, grades, listOfWords, date):
        self.comment = listOfWords
        self.username = grades[0]
        self.grade = float(grades[1])
        self.look = float(grades[3])
        self.smell = float(grades[4])
        self.taste = float(grades[5])
        self.feel = float(grades[6])
        self.overall = float(grades[7])
        self.date = date
        self.beer = beer

class SparseComment:
    
    #remembers a grade for the given category
    def __init__(self, grade, listOfWords):
        self.comment = listOfWords
        self.grade = grade
