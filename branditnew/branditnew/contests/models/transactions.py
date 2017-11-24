from django.db import models
from django.contrib.auth.models import User



class Transaction_Type(models.Model):
    """
    CURRENT TRANSACTION TYPES
    : contest creation
    : contest entry submission
    : project
    : print order
    : brandlancer points purchase

    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Transaction_Status(models.Model):
    name = models.CharField(max_length=50)
    """
    CURRENT TRANSACTION STATUSES [ BORROWED FROM HUBTEL'S INVOICE STATUSES]
    : pending [ neither completed nor cancelled ]
    : completed [ payment has been made ]
    : cancelled [ process was ended without payment being made ]

    """

    def __str__(self):
        return self.name



class Transaction(models.Model):
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Transaction_Type, on_delete=models.DO_NOTHING)
    amount = models.PositiveSmallIntegerField()
    token = models.CharField(max_length=100, blank=True, null=True)
    status = models.ForeignKey(Transaction_Status, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return 'transaction on '+ str(self.created_at)


    @classmethod
    def create(cls, user, type, amount, invoice_token):
        transaction = cls(client=user, amount=amount)
        transaction.status = Transaction_Status.objects.get(name="pending")
        transaction.type = Transaction_Type.objects.get(name=type)
        transaction.token = invoice_token

        return transaction
    


    def update_status(self, new_status):
        #this should only work if the new status exists.
        self.status = Transaction_Status.objects.filter(name=new_status)

        
