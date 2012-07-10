__author__ = 'janos'
import re

def full_name(author_dict):
    first_name_initial = author_dict["first_name_initial"]
    if "middle_name_initial" in author_dict:
        middle_name_initial = author_dict["middle_name_initial"]
    else:
        middle_name_initial = ""

    full_name = first_name_initial + middle_name_initial + " " + author_dict["last_name"]
    author_dict["full_name"] = full_name.strip()
    return author_dict

def author_process_abbreviated(author):
    author_dict = {"author_original" : author}
    author_split = [part.strip() for part in author.split(",")]
    last_name = author_split[0]
    if len(author_split) == 2:
        initials = author_split[1]
        if len(initials) == 2:
            first_name_initial = initials[0]
            middle_name_initial = initials[1]
        else:
            first_name_initial = initials[0]
            middle_name_initial = ""
    else:
        first_name_initial = ""
        middle_name_initial = ""

    author_dict["last_name"] = last_name
    author_dict["first_name_initial"] = first_name_initial
    author_dict["middle_name_initial"] = middle_name_initial
    author_dict = full_name(author_dict)

    return author_dict

def author_process_full(author):
    author_dict = {"author_original" : author}

    author_split = author.split(",")
    author_dict["last_name"] = author_split[0]

    if len(author_split) > 1:
        author_second_part = author_split[1]
        author_dict["first_name_initial"] = author_second_part[1].strip()
        re_two_initials = re.compile("^ [A-Z][A-Z]")
        if re_two_initials.match(author_second_part):
            author_dict["middle_name_initial"] = author_second_part[2]
        else:
            author_given_name_split = author_second_part.split()
            author_dict["first_name"] = author_given_name_split[0]
            if len(author_given_name_split) > 1:
                author_dict["middle_name_initial"] = author_given_name_split[1][0]

        author_dict = full_name(author_dict)
    return author_dict