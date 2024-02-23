import unittest

from app import make_applicant
from app import Applicant
from faker import Faker
ff = Faker()

class Tests(unittest.TestCase):
    def test_make_applicant(self):
        for i in [0, 15, 20, 5555]:
            Faker.seed(i)
            name = ff.name()
            citystate = ff.city() +', '+ ff.state_abbr()
            email = ff.ascii_safe_email()
            college = ff.state() + ff.random.choice([' University', ' State', ' Polytech', ', University of'])
            grade = ff.random.choice(['A','A+','A-','B','B+','B-','F'])
            job = ff.job()
            ap = Applicant(name = name, citystate= citystate,
                                email = email, college= college, grade=grade,
                                job = job)
            self.assertEqual(ap.name, name)
            self.assertEqual(ap.college, college)



if __name__ == "__main__":
    unittest.main()
