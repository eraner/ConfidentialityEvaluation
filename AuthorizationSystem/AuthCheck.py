import Utils.Database.DBHelper as DBHelper


def check_users_roles_optimal_current(curr_users, curr_roles, main_window):
    """
    Compare between optimal and current Users&Roles tables in authorization system.
    :param curr_users:
    :param curr_roles:
    :param main_window:
    :return:
    """
    """Optimal Authorization System (From DB)"""
    conn = DBHelper.create_connection("Utils\\Database\\auth.db")
    opt_users = DBHelper.get_all_users(conn)

    opt_roles = DBHelper.get_all_roles(conn)

    users_damage_assessment = 0.0

    max_users = max(len(curr_users), len(opt_users))
    opt_users_names = [item[1] for item in opt_users]

    opt_roles_names = [item[0] for item in opt_roles]
    opt_roles_ranks = [item[1] for item in opt_roles]

    if len(curr_users) > len(opt_users):
        main_window.print_to_log("DBHelper", "New users were added!")
        for curr_user in curr_users.keys():
            if curr_user not in opt_users_names:
                main_window.print_to_log("DBHelper", curr_user + " was added")
                users_damage_assessment += float(1)/max_users

    for opt_user in opt_users:
        if opt_user[1] not in curr_users.keys():
            main_window.print_to_log("DBHelper", opt_user[1] + " was removed from authorization system")
            users_damage_assessment += float(1) / max_users
            continue
        elif opt_user[2] != curr_users[opt_user[1]]:
            main_window.print_to_log("DBHelper", opt_user[1] + " has changed a role from: "
                                     + opt_user[2] + " to " + curr_users[opt_user[1]])

        if opt_user[2] in opt_roles_names and curr_users[opt_user[1]] in opt_roles_names:
            index_of_opt_role = opt_roles_names.index(opt_user[2])
            curr_role_rank = curr_roles[curr_users[opt_user[1]]]
            diff = abs(float(curr_role_rank)-float(opt_roles_ranks[index_of_opt_role]))
            if float(curr_role_rank) != float(opt_roles_ranks[index_of_opt_role]):
                main_window.print_to_log("DBHelper", "Role: " + opt_user[2] + " changed rank from "
                                         + str(opt_roles_ranks[index_of_opt_role]) + " to " + str(curr_role_rank))
        else:
            diff = 5
        users_damage_assessment += float(diff/5) / float(max_users)

    return 10 if users_damage_assessment*10 > 10 else users_damage_assessment*10


# def check_roles_optimal_current(curr_roles):
#     """
#     Compare between optimal roles table to current roles table.
#     :param curr_roles:
#     :return: String with results of check
#     """
#     conn = DBHelper.create_connection("Utils\\Database\\auth.db")
#     opt_roles = DBHelper.get_all_roles(conn)
#
#     role_damage_assessment = 0.0
#
#     opt_roles_names = [item[0] for item in opt_roles]
#
#     status_change_rank = ""
#     status_add_remove_role = ""
#
#     max_roles = max(len(curr_roles), len(opt_roles))
#
#     """If added new roles to table"""
#     if len(curr_roles) > len(opt_roles):
#         status_add_remove_role += "\nAdded new roles! \n" \
#                   + str(len(curr_roles) - len(opt_roles)) + " new role\s were added:\n"
#         for curr_role in curr_roles.keys():
#             if curr_role not in opt_roles_names:
#                 status_add_remove_role += "\t-" + curr_role + " was added \n"
#                 role_damage_assessment += float(1)/float(max_roles)
#
#     """check roles' rank changes"""
#     for opt_role in opt_roles:
#         if opt_role[0] not in curr_roles.keys():
#             status_add_remove_role += "\n" + opt_role[0] + " was removed from authorization system"
#             role_damage_assessment += float(1)/float(max_roles)
#             continue
#         if opt_role[1] != curr_roles[opt_role[0]]:
#             status_change_rank += "\n" + str(opt_role[0]) + " has changed rank from: " \
#                       + str(opt_role[1]) + " to " + str(curr_roles[opt_role[0]])
#             rank_dif = abs(opt_role[1] - curr_roles[opt_role[0]])
#             role_damage_assessment += abs(float(rank_dif)/5) / float(max_roles)
#
#     status = "\n" + "-"*10 + "Roles Add/Remove" + "-"*10 + "\n" + status_add_remove_role \
#              + "\n" + "-"*10 + "Rank Changes" + "-"*10 + "\n" + status_change_rank
#
#     if status == "":
#         status = "No changes in Authorization system"
#
#     retval = [status, role_damage_assessment]
#
#     return retval
