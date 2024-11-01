import subprocess as sp
import pymysql
from prettytable import PrettyTable
from time import sleep


DEFAULT = "\33[0m"
BOLD = "\33[1m"
RED = "\33[31m"
BLUE = "\33[34m"
YELLOW = "\33[33m"


inp_types = {
    "int": "A standard integer: ",
    "varchar": "A variable-length character string: ",
    "time": "A time value in " + BOLD + "HH:MM:SS" + DEFAULT + " format: ",
    "date": "A date value in " + BOLD + "YYYY-MM-DD" + DEFAULT + " format: "
}


def cls():
    sp.call("clear", shell=True)


def take_input(attr, values):
    for j in attr:
        print(BOLD + j["Field"] + DEFAULT)
        inp = input(inp_types[j["Type"]])
        if inp == "":
            values.append("NULL")
        elif j["Type"] == "int":
            values.append(inp)
        else:
            values.append("'" + inp + "'")
        print()


def take_update_input(attr, old_values, new_values):
    for i, j in enumerate(attr):
        print(BOLD + j["Field"] + DEFAULT)
        inp = input(inp_types[j["Type"]])
        if inp == "" and old_values[i] == None:
            new_values.append("NULL")
        elif inp == "" and j["Type"] == "int":
            new_values.append(str(old_values[i]))
        elif inp == "":
            new_values.append("'" + str(old_values[i]) + "'")
        elif inp == "NULL" or inp == "null":
            new_values.append("NULL")
        elif j["Type"] == "int":
            new_values.append(inp)
        else:
            new_values.append("'" + inp + "'")


def print_table(json_dump, attr):
    x = PrettyTable()
    attr_names = list()
    for i in attr:
        attr_names.append(i["Field"])
    x.field_names = attr_names
    for row in json_dump:
        x.add_row(row.values())
    print(x)


class entity_type:
    def __init__(self, name, pk):
        self.name = name
        self.pk = pk
        query = "select * from " + self.name
        try:
            cur.execute(query)
            self.curr_state = cur.fetchall()
        except Exception as e:
            print(RED + str(e) + DEFAULT)
            print(BLUE + "Press ENTER to continue" + DEFAULT)
            input("")
            return
        con.commit()
        query = "desc " + self.name
        cur.execute(query)
        self.attr = cur.fetchall()
        for i in self.attr:
            # varchars of all lengths are input similarly and handled similarly
            if i["Type"].startswith("varchar"):
                i["Type"] = "varchar"
        con.commit()


    def begin(self):
        print_table(self.curr_state, self.attr)
        print("""
        0. EXIT
        1. Add a new etry
        2. Update an entry
        3. Delete an entry
        """)
        inp = input("select an option: ")
        try:
            inp = int(inp)
        except:
            return

        if inp == 1:
            values = list()
            take_input(self.attr, values)
            query = "insert into " + self.name + " values ("
            for i, j in enumerate(values):
                query = query + j
                if i != len(values) - 1:
                    query = query + ", "
            query = query + ")"
            try:
                cur.execute(query)
                self.curr_state = cur.fetchall()
                con.commit()
            except Exception as e:
                print(RED + str(e) + DEFAULT)
                print(BLUE + "Press ENTER to continue" + DEFAULT)
                input("")
                return

        elif inp == 2:
            inps = list()
            for pk in self.pk:
                inp = input("Enter the " + pk +
                            " of the record that you wish to edit: ")

                for i in self.attr:
                    if i["Field"] == pk:
                        if i["Type"] == "int":
                            try:
                                inp = int(inp)
                            except:
                                print(RED + "Please enter a valid " + pk + "!" + DEFAULT)
                                print(BLUE + "Press ENTER to continue" + DEFAULT)
                                input("")
                                return
                        inps.append(inp)
                        break

            update_record = dict()
            for record in self.curr_state:
                the_one = True
                for i, pk in enumerate(self.pk):
                    if record[pk] != inps[i]:
                        the_one = False
                        break
                if the_one:
                    update_record = record
                    break
                        
            if len(update_record) == 0:
                print(RED + "No matching entries found!" + DEFAULT)
                print(BLUE + "Press ENTER to continue" + DEFAULT)
                input("")
                return
            
            new_values = list()
            take_update_input(self.attr, list(update_record.values()), new_values)

            query = "update " + self.name + " set "
            attr_names = list()
            for i in self.attr:
                attr_names.append(i["Field"])

            cnt = 0
            for i, j in zip(attr_names, new_values):
                query = query + i + " = " + j
                cnt = cnt + 1
                if cnt != len(self.attr):
                    query = query + ", "
            
            query = query + " where "
            for i, pk in enumerate(self.pk):
                query = query + pk + " = " + str("'") + str(inps[i]) + str("'")
                if i != len(self.pk) - 1:
                    query = query + " and "

            try:
                cur.execute(query)
                con.commit()
                print(cur.fetchall(), self.attr)
            except Exception as e:
                print(RED + str(e) + DEFAULT)
                print(BLUE + "Press ENTER to continue" + DEFAULT)
                input("")
                return
        
        elif inp == 3:
            inps = list()
            for pk in self.pk:
                inp = input("Enter the " + pk +
                            " of the record that you wish to edit: ")

                for i in self.attr:
                    if i["Field"] == pk:
                        if i["Type"] == "int":
                            try:
                                inp = int(inp)
                            except:
                                print(RED + "Please enter a valid " + pk + "!" + DEFAULT)
                                print(BLUE + "Press ENTER to continue" + DEFAULT)
                                input("")
                                return
                        inps.append(inp)
                        break
            
            query = "delete from " + self.name + " where "
            for i, pk in enumerate(self.pk):
                query = query + pk + " = " + str("'") + str(inps[i]) + str("'")
                if i != len(self.pk) - 1:
                    query = query + " and "
            try:
                cur.execute(query) 
                con.commit()
            except Exception as e:
                print(RED + str(e) + DEFAULT)
                print(BLUE + "Press ENTER to continue" + DEFAULT)
                input("")
                return

def restaurants_having_item():
    inp = input("Enter the item name that you wish to search for: ")
    upper = input("Enter the upper bound on the price: ")
    inp = "'" + inp + "'"
    query = "select R.Restaurant_Name, R.Open_Time, R.Close_Time, R.Contact, R.State, R.District, R.City from Restaurant R, Menu M where M.RestaurantID = R.RestaurantID and M.Item_Name = " + inp + " and M.Price - M.Price * M.Discount / 100 <= " + upper 
    try:
        cur.execute(query)
        con.commit()
        json_dump = cur.fetchall()
        if len(json_dump) == 0:
            print("Empty set")
            print(BLUE + "Press ENTER to continue" + DEFAULT)
            input("")
            return 
        x = PrettyTable()
        x.field_names = list(json_dump[0].keys())
        for row in json_dump:
            x.add_row(row.values())
        print(x)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
        return

    except Exception as e:
        print(RED + str(e) + DEFAULT)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
        return

def max_profit():
    inp = input("Enter the RestaurantID of the Restaurant whose profits you wish to track: ")

    print(YELLOW + "Most Profitable Month" + DEFAULT)
    query = "select E.Month as 'Most Profitable Month' from Expenditure E where E.RestaurantID = " + inp + " order by E.Month desc limit 1"
    try:
        cur.execute(query)
        con.commit()
        json_dump = cur.fetchall()
        if len(json_dump) == 0:
            print("Empty set")
            print(BLUE + "Press ENTER to continue" + DEFAULT)
            input("")
            return 
        x = PrettyTable()
        x.field_names = list(json_dump[0].keys())
        for row in json_dump:
            x.add_row(row.values())
        print(x)

    except Exception as e:
        print(RED + str(e) + DEFAULT)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
        return
    
    print(YELLOW + "Total Profit" + DEFAULT)
    query = "select sum(E.Total_Profit) 'Total Profit' from Expenditure E where E.RestaurantID = " + inp
    try:
        cur.execute(query)
        con.commit()
        json_dump = cur.fetchall()
        if len(json_dump) == 0:
            print("Empty set")
            print(BLUE + "Press ENTER to continue" + DEFAULT)
            input("")
            return
        x = PrettyTable()
        x.field_names = list(json_dump[0].keys())
        for row in json_dump:
            x.add_row(row.values())
        print(x)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
    except Exception as e:
        print(RED + str(e) + DEFAULT)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
        return

def order_details():
    inp = input("Enter your CustomerID: ")
    query = "select OD.OrderID, OD.Order_Time, OD.Order_Type, OD.Total_Price, R.Restaurant_Name, OI.ItemID, M.Item_Name from Order_Details OD, Order_Items OI, Menu M, Restaurant R where OD.RestaurantID = R.RestaurantID and OI.OrderID = OD.OrderID and M.ItemID = OI.ItemID and OD.CustomerID = " + inp
    try:
        cur.execute(query)
        con.commit()
        json_dump = cur.fetchall()
        if len(json_dump) == 0:
            print("Empty set")
            print(BLUE + "Press ENTER to continue" + DEFAULT)
            input("")
            return
        x = PrettyTable()
        x.field_names = list(json_dump[0].keys())
        for row in json_dump:
            x.add_row(row.values())
        print(x)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")

    except Exception as e:
        print(RED + str(e) + DEFAULT)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
        return

def top_dish():
    inp = input("Enter the RestaurantID of the Restaurant: ")
    query = "select M.Item_Name, count(*) as 'Number of Orders' from Order_Items OI, Order_Details OD, Menu M where OI.OrderID = OD.OrderID and OI.ItemID = M.ItemID and OD.RestaurantID = " + inp + " group by M.ItemID order by 'Number of Orders' desc limit 1"
    try:
        cur.execute(query)
        con.commit()
        json_dump = cur.fetchall()
        if len(json_dump) == 0:
            print("Empty set")
            print(BLUE + "Press ENTER to continue" + DEFAULT)
            input("")
            return
        x = PrettyTable()
        x.field_names = list(json_dump[0].keys())
        for row in json_dump:
            x.add_row(row.values())
        print(x)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
    except Exception as e:
        print(RED + str(e) + DEFAULT)
        print(BLUE + "Press ENTER to continue" + DEFAULT)
        input("")
        return



while True:
    cls()
    username = input("Username: ")
    password = input("Password: ")
    port = int(input("Enter Port Number: "))
    try:
        con = pymysql.connect(host="localhost",
                            user=username,
                            password=password,
                            db="Restaurant",
                            port=port,
                            cursorclass=pymysql.cursors.DictCursor)
        cls()
        if (con.open):
            print("Connected!")
        else:
            print(RED + "Failed to connect" + DEFAULT)
            continue
    except:
        cls()
        input("Press ENTER to continue")
        continue
    while True:
        try:
            con = pymysql.connect(host="localhost",
                                user=username,
                                password=password,
                                db="Restaurant",
                                port=port,
                                cursorclass=pymysql.cursors.DictCursor)
            cls()
            if (con.open):
                print("Connected!")
            else:
                print(RED + "Failed to connect" + DEFAULT)
                exit()
        except:
            cls()
            input("Press ENTER to continue")
            exit()

        with con.cursor() as cur:
            cls()
            print("""
            0. EXIT THE PROGRAM
            1. Restaurant Details
            2. Billing Details
            3. Customer Details
            4. Restaurant Finances Details
            5. Restaurant-wise Menus
            6. Orders Details (excluding items ordered)
            7. Order Items
            8. Staff Details
            9. Get all the restaurants selling an item
            10. Profit details of a restaurant
            11. Get order details by customer-ID
            12: Get top dish of a restaurant by restaurant-ID
            """)

            try:
                inp = int(input(
                    "Type the number corresponding to the respective record that you wish to view/edit: "))
            except:
                continue
            cls()
            if inp == 0:
                break
            elif inp == 1:
                entity_type("Restaurant", ["RestaurantID"]).begin()
            elif inp == 2:
                entity_type("Billing", ["OrderID"]).begin()
            elif inp == 3:
                entity_type("Customer", ["CustomerID"]).begin()
            elif inp == 4:
                entity_type("Expenditure", ["RestaurantID", "Month"]).begin()
            elif inp == 5:
                entity_type("Menu", ["ItemID"]).begin()
            elif inp == 6:
                entity_type("Order_Details", ["OrderID"]).begin()
            elif inp == 7:
                entity_type("Order_Items", ["OrderID", "ItemID"]).begin()
            elif inp == 8:
                entity_type("Staff", ["StaffID"]).begin()
            elif inp == 9:
                restaurants_having_item()
            elif inp == 10:
                max_profit()
            elif inp == 11:
                order_details()
            elif inp == 12:
                top_dish()
