#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import Config

# Pretty Print table in tabular format
def pretty_print(table, justify = "L"):
    # get width for every column
    column_widths = [0] * table[0].__len__()
    offset = 3
    for row in table:
        for index, col in enumerate(row):
            width = len(str(col).decode("utf-8"))
            if width > column_widths[index]:
                column_widths[index] = width
    outputStr = ""
    for row_index, row in enumerate(table):
        rowList = []
        for col_index, col in enumerate(row):
            if justify == "R": # justify right
                formated_column = str(col).decode("utf-8").rjust(column_widths[col_index] + offset)
            elif justify == "L": # justify left
                formated_column = str(col).decode("utf-8").ljust(column_widths[col_index] + offset)
            elif justify == "C": # justify center
                formated_column = str(col).decode("utf-8").center(column_widths[col_index] + offset)
            rowList.append(formated_column.encode("utf-8"))
        if row_index == table.__len__()-1:
            outputStr += ' '.join(rowList)
        else:
            outputStr += ' '.join(rowList) + "\n"
    return outputStr

def get_new_contact_template(addressbook_name):
    return """# new contact
# Addressbook: %s
# if you want to cancel, just leave the first or last name field blank

# first and last name
# at least enter first and last name or organisation
First name   = 
Last name    = 
Organisation = 

# phone numbers
# format: PhoneX = type: number
# allowed types: cell, home, work
Phone1 = cell: 
Phone2 = home: 

# email addresses
# format: EmailX = type: address
# allowed types: home, work
Email1 = home: 

# post addresses
# format: AddressX = type: street and house number; postcode; city; region; country
# the region is optional so the following is allowed too:
# format: AddressX = type: street and house number; postcode; city;; country
# standard types: home, work
Address1 = home: ; ; ; ; %s

# Birthday: day.month.year
Birthday = """ % (addressbook_name, Config().get_default_country())

def get_existing_contact_template(vcard):
    strings = []
    for line in get_new_contact_template(vcard.get_addressbook_name()).splitlines():
        if line == "# new contact":
            strings.append("# Edit contact: %s" % vcard.get_full_name())
        elif line.lower().startswith("# if you want to cancel"):
            continue
        elif line.lower().startswith("first name"):
            strings.append("First name   = %s" % vcard.get_first_name())
        elif line.lower().startswith("last name"):
            strings.append("Last name    = %s" % vcard.get_last_name())
        elif line.lower().startswith("organisation"):
            strings.append("Organisation = %s" % vcard.get_organisation())
        elif line.lower().startswith("phone"):
            if line.lower().startswith("phone1"):
                for index, entry in enumerate(vcard.get_phone_numbers()):
                    strings.append("Phone%d = %s: %s" % (index+1, entry['type'], entry['value']))
        elif line.lower().startswith("email"):
            if line.lower().startswith("email1"):
                for index, entry in enumerate(vcard.get_email_addresses()):
                    strings.append("Email%d = %s: %s" % (index+1, entry['type'], entry['value']))
        elif line.lower().startswith("address"):
            if line.lower().startswith("address1"):
                for index, entry in enumerate(vcard.get_post_addresses()):
                    strings.append("Address%d = %s: %s; %s; %s; %s; %s" % (index+1, entry['type'],
                            entry['street_and_house_number'], entry['postcode'], entry['city'],
                            entry['region'], entry['country']))
        elif line.lower().startswith("birthday") and vcard.get_birthday() != None:
            date = vcard.get_birthday()
            strings.append("Birthday = %.2d.%.2d.%.4d" % (date.day, date.month, date.year))
        else:
            strings.append(line)
    return '\n'.join(strings)

