import cx_Oracle
import Logout
con=cx_Oracle.connect("ce50/ce50@INFY")
cur=con.cursor()
def log():
    print('Enter below details:')
    admin_id=input('Admin id:')
    spassword=input('Password:')
    password=int(spassword)
    cur.execute('Select password from admin where admin_id=:1',(admin_id,))
    xc=cur.fetchone()
    print(xc)
    xcc=xc[0]
    x=int(xcc)
    if x==password:
        print('Enter\n1)Print closed account history\n2)FD Report of a Customer\n'
              '3)FD Report of Customers vis-à-vis another Customer\n4)FD Report of Customers w.r.t a particular FD Amount\n'
              '5)Loan Report of a Customer\n6)Loan Report of Customers vis-à-vis another Customer\n'
              '7)Loan Report of Customers w.r.t a particular Loan Amount \n8)Loan – FD Report of Customers\n'
              '9)Report of Customers who are yet to avail a loan (customer id, first name, last name)\n'
              '10)Report of Customers who are yet to open a FD account (customer id, first name, lastname)\n'
              '11)Report of Customers who neither have a loan nor a FD account with the bank (customerid, first name, last name,)\n'
              '12)Logout')

        svalue=input('Enter your choice:')
        value=int(svalue)
        if value==1:
            cur.execute('Select accountno,firstname,lastname,opendate from customer where closedate is not null')
            x=cur.fetchall()
            print(x)
            print('%20s %20s %20s %20s'%('Account no','Firstname','Lastname','OpenDate'))
            for item in x:
                print('%20s %20s %20s %20s' % (item[0], item[1], item[2], str(item[3])))
        elif value==2:
            c_id=input('Enter customer-id of customer:')
            cur.execute('Select closedate from customer where accountno=:1',(c_id,))
            y=cur.fetchone()
            if y==None:
                cur.execute('Select * from customer where accountno=:1',(c_id,))
                x=cur.fetchall()
                if(x != []):
                    cur.execute('Select * from fd where amount>(Select sum(amount) num from fd where accountno=:1)', (c_id,))
                    x = cur.fetchall()
                    print('%20s %20s %20s %20s' % ('FD Account no', 'Account no', 'Amount', 'Term'))
                    for item in x:
                        print('%20s %20s %20s %20s' % (item[0], item[1], str(item[2]), str(item[3])))

                else:
                    print('N.A.')
            else:
                print('Account is closed')

        elif value==3:
            c_id=input('Enter customer-id of customer:')
            cur.execute('Select closedate from customer where accountno=:1', (c_id,))
            y = cur.fetchone()
            if y == None:
                cur.execute('Select * from customer where accountno=:1',(c_id,))
                x=cur.fetchall()

                if(x != []):
                    cur.execute('Select * from fd where amount>(Select sum(amount) num from fd where accountno=:1)',(c_id,))
                    x=cur.fetchall()
                    print('%20s %20s %20s %20s' % ('FD Account no', 'Account no', 'Amount', 'Term'))
                    for item in x:
                        print('%20s %20s %20s %20s' % (item[0], item[1], str(item[2]), str(item[3])))

                else:
                    print('Customer does not have account')
            else:
                print('Account is closed')

        elif value==4:
            samount=input('Enter amount:')
            amount=int(samount)
            if (amount>0) and (amount%1000==0):
                cur.execute('Select c.accountno,c.firstname,c.lastname,f.amount from customer c join fd f on \
                          c.accountno=f.accountno where f.amount>:1',(amount,))
                x=cur.fetchall()
                print('%20s %20s %20s %20s' % ('Account no', 'Firstname', 'Lastname', 'Amount'))
                for item in x:
                    print('%20s %20s %20s %20s' % (item[0], item[1], item[2], str(item[3])))

        elif value==5:
            customerid = input('customer id:')
            cur.execute('Select closedate from customer where accountno=:1', (customerid,))
            y = cur.fetchone()
            if y == None:
                cur.execute("""Select loanaccountno,amount,repayterm from LOAN WHERE (accountno = :1)""", \
                            (customerid,))
                result = cur.fetchall()
                print('%20s  %20s  %20s ' % ('loanaccountno', 'amount', 'repayterm',))
                for item in result:
                    print('%20s  %20s  %20s ' % (str(item[0]), item[1], item[2],))
            else:
                print('Account is closed')

        elif value==6:
            c_id=input('Enter customer id:')
            cur.execute('Select closedate from customer where accountno=:1', (c_id,))
            y = cur.fetchone()
            if y == None:
                cur.execute('Select * from customer c join loan l on c.accountno=l.accountno')
                x=cur.fetchall()

                if(x != []):
                    cur.execute('Select * from loan where amount>(Select sum(amount) num from loan where accountno=:1)', (c_id,))
                    x = cur.fetchall()
                    print('%20s %20s %20s %20s' % ('Loan Account no', 'Account no', 'Amount', 'Re Payment Term'))
                    for item in x:
                        print('%20s %20s %20s %20s' % (item[0], item[1], str(item[2]), str(item[3])))

                else:
                    print('Customer\'s entry does not exist in customer or laon table')
            else:
                print('Account is closed')

        elif value==7:
            samount = input('Enter amount:')
            amount = int(samount)
            if (amount > 0) and (amount % 1000 == 0):
                cur.execute('Select c.accountno,c.firstname,c.lastname,l.amount from customer c join loan l on \
                                  c.accountno=l.accountno where l.amount>:1', (amount,))
                x = cur.fetchall()
                print('%20s %20s %20s %20s' % ('Account no', 'Firstname', 'Lastname', 'Amount'))
                for item in x:
                    print('%20s %20s %20s %20s' % (item[0], item[1], item[2], str(item[3])))

        elif value==8:
            cur.execute('Select c.accountno,c.firstname,c.lastname,z.l,z.f \
                          from customer c \
                          join\
                          (Select x.a account,x.loan l,y.fd f from\
                          (Select accountno a,sum(amount) loan from loan \
                          group by accountno) x \
                          join(Select accountno a,sum(amount) fd from fd group by accountno) y on \
                          x.a=y.a where x.loan>y.fd) z on c.accountno=z.account')
            x = cur.fetchall()
            print('%20s %20s %20s %20s %20s' % ('Account no', 'Firstname', 'Lastname', 'Loan','FD'))
            for item in x:
                print('%20s %20s %20s %20s %20s' % (item[0], item[1], item[2], str(item[3]),str(item[4])))

        elif value == 9:
            cur.execute(
                """Select c.accountno,c.firstname,c.lastname from customer c left outer join loan l on c.accountno=l.accountno where l.accountno is null """)
            result = cur.fetchall()
            print('%20s  %20s  %20s ' % ('accountno', 'firstname', 'lastname',))
            for item in result:
                print('%20s  %20s  %20s ' % (str(item[0]), item[1], item[2],))

        elif value == 10:
            cur.execute(
                """Select c.accountno,c.firstname,c.lastname from customer c left outer join fd f on c.accountno=f.accountno where f.accountno is null """)
            result = cur.fetchall()
            print('%20s  %20s  %20s ' % ('accountno', 'firstname', 'lastname',))
            for item in result:
                print('%20s  %20s  %20s ' % (str(item[0]), item[1], item[2],))

        elif value == 11:
            cur.execute("""select c.accountno,c.firstname,c.lastname from customer c left outer join loan l on c.accountno=l.accountno
                                                          left outer join fd f on c.accountno=f.accountno
                                                          where (l.accountno is null and f.accountno is null) """)
            result = cur.fetchall()
            print('%20s  %20s  %20s ' % ('accountno', 'firstname', 'lastname',))
            for item in result:
                print('%20s  %20s  %20s ' % (str(item[0]), item[1], item[2],))

        elif value == 12:
            Logout.close()
    else:
        print('Password incorrect')