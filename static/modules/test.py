from alchemy.users                    import User
from alchemy.jobs                     import Jobs
from alchemy.session                  import global_init, create_session

 
def readColonists(rule={}):
    class Jobz(Jobs):
        import sqlalchemy
        user = sqlalchemy.orm.relation('User')

    session = create_session()
    session.query(User).filter(User.address == "module_1",
                               User.age < 21).update({User.address: "module_3"})
    session.commit()


if __name__ == '__main__':
    name = "../db/db.sqlite"
    global_init(name)  # init BaseName
    readColonists()
