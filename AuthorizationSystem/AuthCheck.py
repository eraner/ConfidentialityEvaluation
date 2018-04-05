import Utils.Database.DBHelper as DBHelper


def check_users_optimal_current(curr_users):
    """
    Compare between optimal and current Users table in authorization system.
    :param: curr_users
    :return: String with results of check
    """

    """Optimal Authorization System (From DB)"""
    conn = DBHelper.create_connection("Utils\\Database\\auth.db")
    opt_users = DBHelper.get_all_users(conn)

    opt_roles = DBHelper.get_all_roles(conn)

    status = ""
    status_change_role = ""
    status_add_remove_user = ""

    users_damage_assessment = 0.0

    max_users = max(len(curr_users), len(opt_users))
    opt_users_names = [item[1] for item in opt_users]
    opt_roles_names = [item[2] for item in opt_users]

    if len(curr_users) > len(opt_users):
        status += "\nAdded new users! \n" \
                  + str(len(curr_users) - len(opt_users)) + " new user\s were added\n"
        for curr_user in curr_users.keys():
            if curr_user not in opt_users_names:
                status_add_remove_user += "\t-" + curr_user + " was added \n"
                users_damage_assessment += float(1)/max_users

    for opt_user in opt_users:
        if opt_user[1] not in curr_users.keys():
            status_add_remove_user += "\n" + opt_user[1] + " was removed from authorization system"
            users_damage_assessment += float(1) / max_users
            continue
        elif opt_user[2] != curr_users[opt_user[1]]:
            status_change_role += "\n" + opt_user[1] + " has changed a role from: " \
                                  + opt_user[2] + " to " + curr_users[opt_user[1]]
            if opt_user[2] in opt_roles_names and curr_users[opt_user[1]] in opt_roles_names:
                index_of_opt_role = opt_roles_names.index(opt_user[2])
                index_of_curr_role = opt_roles_names.index(curr_users[opt_user[1]])
                diff = abs(float(index_of_curr_role)-float(index_of_opt_role))
            else:
                diff = 5
            users_damage_assessment += float(diff/5) / float(max_users)

    status = "\n" + "-"*10 + "Users Add/Remove" + "-"*10 + "\n" + status_add_remove_user \
             + "\n" + "-"*10 + "Roles Changes" + "-"*10 + "\n" + status_change_role
    if status == "":
        status = "No changes in Authorization system"

    retval = [status, users_damage_assessment]

    return retval


def check_roles_optimal_current(curr_roles):
    """
    Compare between optimal roles table to current roles table.
    :param curr_roles:
    :return: String with results of check
    """
    conn = DBHelper.create_connection("Utils\\Database\\auth.db")
    opt_roles = DBHelper.get_all_roles(conn)

    role_damage_assessment = 0.0

    opt_roles_names = [item[0] for item in opt_roles]

    status_change_rank = ""
    status_add_remove_role = ""

    max_roles = max(len(curr_roles), len(opt_roles))

    """If added new roles to table"""
    if len(curr_roles) > len(opt_roles):
        status_add_remove_role += "\nAdded new roles! \n" \
                  + str(len(curr_roles) - len(opt_roles)) + " new role\s were added:\n"
        for curr_role in curr_roles.keys():
            if curr_role not in opt_roles_names:
                status_add_remove_role += "\t-" + curr_role + " was added \n"
                role_damage_assessment += float(1)/float(max_roles)

    """check roles' rank changes"""
    for opt_role in opt_roles:
        if opt_role[0] not in curr_roles.keys():
            status_add_remove_role += "\n" + opt_role[0] + " was removed from authorization system"
            role_damage_assessment += float(1)/float(max_roles)
            continue
        if opt_role[1] != curr_roles[opt_role[0]]:
            status_change_rank += "\n" + str(opt_role[0]) + " has changed rank from: " \
                      + str(opt_role[1]) + " to " + str(curr_roles[opt_role[0]])
            rank_dif = abs(opt_role[1] - curr_roles[opt_role[0]])
            role_damage_assessment += abs(float(rank_dif)/5) / float(max_roles)

    status = "\n" + "-"*10 + "Roles Add/Remove" + "-"*10 + "\n" + status_add_remove_role \
             + "\n" + "-"*10 + "Rank Changes" + "-"*10 + "\n" + status_change_rank

    if status == "":
        status = "No changes in Authorization system"

    retval = [status, role_damage_assessment]

    return retval
