from . import UnityPoco


if __name__ == '__main__':
    p = UnityPoco(("10.254.46.45", 5001))
    p("Player").offspring("Mesh").click()
