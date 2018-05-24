import Utils.Database.DBHelper as DBHandler
import Utils.NVD.NVD_Handler as NVD_Handler
import AuthorizationSystem.AuthCheck as AuthCheck
import Utils.HistoryManagement.history_manage as history_manage

def add_user(username, role, main_window):
    #print "Please insert the required data: \n"
    #username = raw_input("Username: ")
    #role = raw_input("Role: ")

    if DBHandler.add_user(username, role, main_window):
        main_window.print_to_log("Controller", "Added " + username + " successfully!")
    else:
        main_window.print_to_log("Controller", "Something went wrong!")


def delete_user(username, main_window):
    #username = raw_input("Please insert User to delete: ")
    if DBHandler.delete_user(username, main_window):
        main_window.print_to_log("Controller", username + " was removed")


def add_role(role_name, rank, main_window):
   # print "Please insert the required data: \n"
   # role_name = raw_input("Role name: ")
   # rank = raw_input("Rank (1-5): ")
    if DBHandler.add_role(role_name, rank, main_window):
        main_window.print_to_log("Controller", role_name + " was added")


def delete_role(role_name, main_window):
    #role_name = raw_input("Role name: ")
    DBHandler.delete_role(role_name, main_window)


def add_resource(resource_name, resource_type, main_window):
  #  print "Please insert the required data: \n"
  #  resource_name = raw_input("Resource name: ")
  #  resource_type = raw_input("Resource type: ")
    if DBHandler.add_resource(resource_name, resource_type, main_window):
        main_window.print_to_log("Controller", "Resource: " + resource_name + " was added")


def delete_resource(resource_id, main_window):
 #   resource_id = raw_input("Please insert resource ID to remove: ")
    if DBHandler.delete_resource_by_id(resource_id, main_window):
        main_window.print_to_log("Controller", "Resource id: " + resource_id + " was removed")


def add_rule(role, resource_id, permission, main_window):
#    print "Please insert the required data: \n"
#    permissions = ["rw", "r", "x", "rwx"]
#    role = raw_input("Role name: ")
#    resource_id = raw_input("Resource id: ")
#    for i in range(len(permissions)):
#        print str(i) + ". " + permissions[i]
#    perm_index = raw_input("Please choose the permission index: ")
#    if int(perm_index) not in range(len(permissions)):
#        print "Invalid permission index!"
#        return
    print permission
    if DBHandler.add_rule(role, resource_id, permission, main_window):
        main_window.print_to_log("Controller", "Rule was added")


def delete_rule(role, resource_id, main_window):
   # print "Please insert the required data: \n"
   # role = raw_input("Role: ")
   # resource_id = raw_input("Resource ID: ")
    if DBHandler.delete_rule(role, resource_id, main_window):
        main_window.print_to_log("Controller", "Rule was removed!")


def insert_result_to_history(final_result, damaged_apps, main_window):
    history_manage.insert_result_to_DB(final_result, damaged_apps, main_window)


def get_prediction(current_damaged_apps, main_window):
    return history_manage.evaluate_prediction(current_damaged_apps, main_window)


def check_auth_system(main_window):
    # # No change to opt auth state
    # curr_users = {"Eran Laudin": "Manager",
    #               "Ohad Cohen": "Cleaner",
    #               "Yael Gershenshtein": "Guard",
    #               "Nir Levi": "Developer",
    #               "Omri Koresh": "QA"}
    # curr_roles = {"Manager": 1,
    #               "Cleaner": 5,
    #               "Developer": 3,
    #               "Team Leader": 2,
    #               "Guard": 4,
    #               "QA": 4}


    #  # Minor change to opt auth state
    # curr_users = {"Eran Laudin": "Manager",
    #                "Ohad Cohen": "Cleaner",
    #                "Yael Gershenshtein": "Guard",
    #                "Nir Levi": "Developer",
    #                "Omri Koresh": "QA"}
    # curr_roles = {"Manager": 1,
    #                "Cleaner": 4,
    #                "Developer": 4,
    #                "Team Leader": 2,
    #                "Guard": 4,
    #                "QA": 4}

    # # Medium change to opt auth state
    # curr_users = {"Eran Laudin": "Manager",
    #               "Ohad Cohen": "Developer",
    #               "Yael Gershenshtein": "Guard",
    #               "Nir Levi": "Developer",
    #               "Omri Koresh": "QA"}
    # curr_roles = {"Manager": 5,
    #               "Cleaner": 4,
    #               "Developer": 1,
    #               "Team Leader": 2,
    #               "Guard": 4,
    #               "QA": 1}

    # Major change to opt auth state
    curr_users = {"Eran Laudin": "Manager",
                 "Ohad Cohen": "Developer",
                 "Yael Gershenshtein": "Guard",
                 "Nir Levi": "Developer",
                 "Avi": "Developer",
                 "Or": "Developer",
                 "Omri Koresh": "QA"}
    curr_roles = {"Manager": 5,
                 "Cleaner": 1,
                 "Developer": 1,
                 "Team Leader": 5,
                 "Guard": 1,
                 "QA": 1}

    # # Worst change to opt auth state
    # curr_users = {"Eran Laudin": "Manager",
    #               "Nir Levi": "Developer",
    #               "Avi": "Developer",
    #               "Or": "Developer",
    #               "Oren": "Developer",
    #               "Idan": "Cleaner",
    #               "Yossi": "Guard",
    #               "Omri Koresh": "QA"}
    # curr_roles = {"Manager": 5,
    #               "Cleaner": 1,
    #               "Developer": 1,
    #               "Team Leader": 5,
    #               "Guard": 1,
    #               "QA": 1}

    result = ""

    main_window.print_to_log("Controller", "#"*15 + "Users" + "#"*15)
    main_window.print_to_log("Controller", "Comparing current Users with optimal Users..")
    results = AuthCheck.check_users_roles_optimal_current(curr_users, curr_roles, main_window)
    main_window.print_to_log("Controller", "Results: Damage assessment to Users' table: " + str(results))

    # result += "\n" + "#"*15 + "Roles" + "#"*15 + "\n\n"
    # result += "Comparing current Roles with optimal Roles..\n"
    # results = AuthCheck.check_roles_optimal_current(curr_roles)
    # result += "Results: Damage assessment to roles' table: " + str(results[1])
    return results


def update_NVD_file(main_window):
    main_window.print_to_log("Controller", "Getting the latest NVD version..")
    NVD_Handler.update_nvd_file(main_window)


def get_list_of_apps():
    #app_list = ["word"]
    #app_list = ["big_brother"]
    app_list = ["big_brother", "net-snmp", "safari", "skype"]
    return app_list


def find_nvd_vulnerabilities(main_window):
    app_list = get_list_of_apps()

    return NVD_Handler.get_vulnerability_impact(app_list, main_window)


def print_auth_system(main_window):
    main_window.print_to_log("Controller", "Printing Auth System")
    DBHandler.print_authorization_system(main_window)


