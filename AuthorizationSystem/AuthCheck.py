import Utils.Database.DBHelper as DBHelper


def check_auth_optimal_current():
    """
    Compare between optimal and current Authorization system.
    :return: String with results of check
    """
    """Current Authorization System (Fictive)"""
    curr_users = {"Eran Laudin": "Manager",
                  "Ohad Cohen": "Cleaner",
                  "Yael Gershenshtein": "Guard",
                  "Nir Levi": "Developer",
                  "Omri Koresh": "QA"}

    conn = DBHelper.create_connection("Utils\\Database\\auth.db")
    opt_users = DBHelper.GetAllUsers(conn)

    status=""

    if len(curr_users) > len(opt_users):
        status += "\nAdded new users! Check who was added! " \
                  + str(len(curr_users) - len(opt_users)) + " new user\s added"

    for opt_user in opt_users:
        if opt_user[1] not in curr_users.keys():
            status += "\n" + opt_user[1] + " was removed from authorization system"
            continue
        if opt_user[2] != curr_users[opt_user[1]]:
            status += "\n" + opt_user[1] + " has changed a role from: " + opt_user[2] + "to " + curr_users[opt_user[1]]

    if status == "":
        status = "No changes in Authorization system"
    return status



