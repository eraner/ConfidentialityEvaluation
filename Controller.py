import Utils.Database.DBHelper as DBHander
import Utils.NVD.NVD_Handler as NVD_Handler


def print_authorization_system():
    con = DBHander.create_connection("Utils\\Database\\auth.db")
    """Print Users Table"""
    print("\n\n" + "-"*10 + "Getting all Users" + "-"*10)
    allUsers = DBHander.GetAllUsers(con)
    for user in allUsers:
        print(user)

    """Print Roles Table"""
    print("\n\n" + "-"*10 + "Getting all Roles" + "-"*10)
    allRoles = DBHander.GetAllRoles(con)
    for role in allRoles:
        print(role)

    """Print Rules Table"""
    print("\n\n" + "-"*10 + "Getting all Rules" + "-"*10)
    allRules = DBHander.GetAllRules(con)
    for role in allRules:
        print(role)

    """Print Resources Table"""
    print("\n\n" + "-"*10 + "Getting all Resources" + "-"*10)
    allResources = DBHander.GetAllResources(con)
    for resource in allResources:
        print(resource)

    con.close()


if __name__ == "__main__":
    while True:
        choice = input("Menu: \n1. Print Authorization Details."
                       "        \n2. Print NVD."
                       "        \n3. Exit\n")
        if choice == 1:
            print_authorization_system()
        elif choice == 2:
            NVD_Handler.get_vulnerability_by_app_name("")
        elif choice == 3:
            print "Goodbye"
            break
        else:
            print "Wrong Input!"
