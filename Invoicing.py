import csv
import datetime

class Invoice:
    _invoiceIds = 90001
    
    def __init__(self):
        self._date = datetime.datetime.now().strftime("%a %b %d %Y")
        self._costDue = 0
        
        self._invoiceNumber = Invoice._getInvoiceNumber(self._date)

        self._allServices = {}
        self._paid = False
        

    @classmethod
    def _getInvoiceNumber(cls, date):
        date = date[-7:].replace(" ", "")
        return str(cls._nextInvoiceNumber()) + date

    @classmethod
    def _nextInvoiceNumber(cls):
        num = cls._invoiceIds
        cls._invoiceIds += 1
        return num   

    def invoiceNumber(self):
        return self._invoiceNumber

    def services(self):
        return self._allServices

    def paid(self):
        return self._paid

    def markPaid(self):
        self._paid = true

    def addService(self, service, price):
        self._allServices[service] = price

    def removeService(self, service):
        self._allServices.pop(service)
        
    def total(self):
        t = 0
        for value in self._allServices.values():
            t += value

        return t

    def __str__(self):
        s = self._invoiceNumber + "\n"
        s += self._date + "\n\n"
        s += "-"*42 + "\n"
        for key, inv in self._allServices.items():
            s += f'{key[:25]:<30} - ${inv:>8.2f} \n'
        
        s += "-"*42 + "\n"
        s += f'${self.total():>31.2f}\n'
        if self._paid:
            s += f'{"PAID":>31}'
        else:
            s += f'{"UNPAID":>31}'
        s += "\n\n\n"

        return s
        


    
        
        
class POS:

    _menu = ['create invoice', 'add service to invoice', 'remove service from invoice', 'accept payment', 'print invoice', 'exit']
    

    def __init__(self, filename):
        
        self._serviceLookup = self._getServiceList(filename)

        self._allInvoices = {}
        
        

    @classmethod
    def _getServiceList(cls, filename):

        services = {}
        with open(filename) as fileIn:
            fileIn.readline()
            reader = csv.reader(fileIn)
            for line in reader:
                services[line[0]] = int(line[1])

        return services


    def _addInvoice(self, inv):
        self._allInvoices[inv.invoiceNumber()] = inv

    
    def _listUnpaidInvoices(self):
        unpaid = {}
        for key, inv in self._allInvoices.items():
            if not inv.paid():
                unpaid[key] = inv
        return unpaid

    def printMenu(self):
        s = "MAIN MENU"
        print(f'{s:^32}')
        print("-"*32)
        
        for i in range(0, len(self._menu)):
            print(f'{i+1:>3}. {self._menu[i]}')

    def getMenuSelection(self):
        try:
            choice = input("\nEnter your selection")

            while int(choice) > len(self._menu):
                choice = input(f'\nYou\'ve entered an invalid choice {choice}. Enter a valid number')

            return int(choice)

        except ValueError:
            print(f'\nYou\'ve entered an invalid choice {choice}. Enter a number')



    @classmethod
    def close(cls):
        print("\n\n\nThank you. No data will be saved")
    


    def printServices(self, listServices):

        for key, price in listServices.items():
            print(f'{key:<65} ${price:>6.2f}')
            

    def getService(self, listServices):
        choice = input("\nWhich service would you like to add?")
        while choice not in listServices:
            choice = input("\nNot valid choice, try again")
        return choice, self._serviceLookup[choice]
    
    def confirmInvoice(self):

        print("\n\nChoose an invoice number to edit")
        for key in self._listUnpaidInvoices():
            print(f'{key:<20}')

        choice = input("Enter")
        while choice not in self._listUnpaidInvoices().keys():
            choice = input("wrong number, try again")

        return self._listUnpaidInvoices()[choice]
        
        
    @classmethod
    def printInvoice(cls, inv):
        print(inv)


    @classmethod
    def confirmInvoiceCreated(cls, inv):
        print(f'\n\nYou have created Invoice {inv.invoiceNumber()}\n\n')

        
    def main(self):

        
        self.printMenu()
        choice = self.getMenuSelection()

        while choice != len(self._menu):
            
            if choice == 1:
                currentInv = Invoice()
                self._addInvoice(currentInv)
                self.confirmInvoiceCreated(currentInv)
                
            elif choice == 2:
                currentInv = self.confirmInvoice()
                self.printServices(self._serviceLookup)
                service, price = self.getService(self._serviceLookup)
                currentInv.addService(service, price)

            elif choice == 3:
                currentInv = Invoice()
                self.printServices(currentInv.services())
                service, price = self.getService(currentInv.services())
                currentInv.removeService(service)

            elif choice == 4:
                currentInv = self.confirmInvoice()
                self.markPaid()
                
            elif choice == 5:
                currentInv = self.confirmInvoice()
                self.printInvoice(currentInv)

            self.printMenu()
            choice = self.getMenuSelection()

        self.close()



clinic = POS("serviceList.csv")
clinic.main()

