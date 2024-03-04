#write a class for student with the following attributes: id, name, key, lab1, lab2, lab3, lab4, midterm, exam1, exam2, exam3, exam4
class Student:
    def __init__(self, name, student_id, key, lab1, lab2, lab3, lab4, midterm, exam1, exam2, exam3, exam4):
        self.student_id = student_id
        self.name = name
        self.key = key
        self.lab1 = int(lab1)
        self.lab2 = int(lab2)
        self.lab3 = int(lab3)
        self.lab4 = int(lab4)
        self.midterm = int(midterm)
        self.exam1 = int(exam1)
        self.exam2 = int(exam2)
        self.exam3 = int(exam3)
        self.exam4 = int(exam4)

    @classmethod
    def from_csv_row(cls, csv_row):
        return cls(
            name=csv_row['Name'],
            student_id=csv_row['ID Number'],
            key=csv_row['Key'],
            lab1=csv_row['Lab 1'],
            lab2=csv_row['Lab 2'],
            lab3=csv_row['Lab 3'],
            lab4=csv_row['Lab 4'],
            midterm=csv_row['Midterm'],
            exam1=csv_row['Exam 1'],
            exam2=csv_row['Exam 2'],
            exam3=csv_row['Exam 3'],
            exam4=csv_row['Exam 4'] 
        )
    
    def get_mt_avg(self)-> str :
        return self.midterm
    
    def get_exam_avg(self) -> str :
        return (self.exam1 + self.exam2 + self.exam3 + self.exam4)/4
    
    def get_grades(self) -> str :
        return ("lab1:{}, lab2:{}, lab3:{}, lab4:{}, midterm:{}, exam1:{}, exam2:{}, exam3:{}, exam4:{}".format(self.lab1, self.lab2, self.lab3, self.lab4, self.midterm, self.exam1, self.exam2, self.exam3, self.exam4))
