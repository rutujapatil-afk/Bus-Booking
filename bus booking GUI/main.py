from tkinter import *
from PIL import ImageTk,Image
import sqlite3
from tkinter import messagebox

#create a database
conn=sqlite3.connect('bustables1.db')

#create cursor
cur=conn.cursor()

cur.execute('''create table if not exists passenger_ticket(
    Name text,
    Gender text,
    No_of_seats integer,
    Mobile_no integer,
    Age integer,
    Fare integer,
    Travel_on text,
    Boarding_point text,
    Destination_point text,
    operator_name text,
    Bus_id integer,
    foreign key(Bus_id) references bus(B_id) on delete cascade
    )
''')

#create operator table
cur.execute('''create table if not exists operator(
    Opr_id integer primary key,
    Opr_name text,
    Opr_address text,
    Opr_phone integer,
    Opr_email text
)''')

#create route table
cur.execute('''create table if not exists route(
    R_id integer,
    Stn_name text,
    Stn_id integer,
    primary key(R_id,Stn_id)
)
''')
#create bus table
cur.execute('''create table if not exists bus(
    B_id integer primary key,
    B_type text,
    B_capacity integer,
    B_fare integer,
    B_oprid integer,
    B_rid integer,
    foreign key(B_oprid) references operator(opr_id) on delete cascade,
    foreign key(B_rid) references route(R_id) on delete cascade
)''')

#create run table
cur.execute('''create table if not exists run(
    Run_bid integer,
    Run_date text,
    Run_seatavailable integer,
    primary key(Run_bid,Run_date),
    foreign key(Run_bid) references bus(B_id) on delete cascade
)''')

#-------------------------------------------------------------------------------------------------------------------------------------------

def Add_Run_Details():
    #create a database
    conn=sqlite3.connect('bustables1.db')
    #create cursor
    cur=conn.cursor()

    # Create a new window
    global Add_Run_Details_win
    Add_Run_Details_win = Toplevel()
    Add_Run_Details_win.title("Add New Run Details")
    Add_Run_Details_win.geometry('1920x1080')

    # Add widgets and functionality for the new window
    global img 
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(Add_Run_Details_win,image=img,relief='sunken').pack()
    Label(Add_Run_Details_win, text="Online Bus Booking System",bg='sky blue',fg='red',font=("Arial",25)).pack(pady=15)
    Label(Add_Run_Details_win, text="Add Bus Running Details",bg='green',fg='red',font=("Arial",20)).pack(padx=10,pady=5)

    fr_run=Frame(Add_Run_Details_win)
    fr_run.pack(padx=5,pady=15)
   
    lbl_runbid=Label(fr_run,text='Bus ID',font=("Arial",15))
    lbl_runbid.grid(row=0,column=0)
    lbl_rundate=Label(fr_run,text='Running Date',font=("Arial",15))
    lbl_rundate.grid(row=0,column=2)
    lbl_runseatavailable=Label(fr_run,text='Seat Available',font=("Arial",15))
    lbl_runseatavailable.grid(row=0,column=4)

    ent_runbid=Entry(fr_run,font=("Arial",10))
    ent_runbid.grid(row=0,column=1)
    ent_rundate=Entry(fr_run,font=("Arial",10))
    ent_rundate.grid(row=0,column=3)
    ent_runseatavailable=Entry(fr_run,font=("Arial",10))
    ent_runseatavailable.grid(row=0,column=5)

    def addrun():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
      
        cur.execute('insert into run values(:a,:b,:c)',
                {
                    'a':ent_runbid.get(),
                    'b':ent_rundate.get(),
                    'c':ent_runseatavailable.get(),
                })
        cur.execute('select * from run')
        records=cur.fetchall()
        lbl_display=Label(fr_run,text=records[-1])
        lbl_display.grid(row=1,column=0,columnspan=8)
    
        conn.commit()
        conn.close()

    
    def deleterun():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
        
        cur.execute('delete from run where Run_bid=? and Run_date=?',
                (ent_runbid.get(),ent_rundate.get())
        )
    
        cur.execute('select *,oid from run')
        records=cur.fetchall()
        lbl_display=Label(fr_run,text=records)
        lbl_display.grid(row=1,column=0,columnspan=8)
    
        conn.commit()
        conn.close()

   
    def addrunpopup():
        response=messagebox.showinfo('run entry','run record added')
        if(response=='ok'):
            addrun()
        else:
            return

    def deleterunpopup():
        response=messagebox.showinfo('run entry update','run record updated successfully')
        if(response=='ok'):
            deleterun()
        else:
            return

    def check():
        if(ent_runbid.get()=='' or ent_rundate.get()=='' or ent_runseatavailable.get()==''):
            response=messagebox.showerror('Invalid Details','Please Enter Valid Details')   
        else:
            addrunpopup()
    
    btn_addrun=Button(fr_run,text='Add Run',bg='light green',font=("Arial",15),command=check)
    btn_addrun.grid(row=0,column=6,padx=10)

    
    btn_deleterun=Button(fr_run,text='Delete Run',bg='light green',font=("Arial",15),command=deleterunpopup)
    btn_deleterun.grid(row=0,column=7)

    def home():
        create_window2(1)
        Add_Run_Details_win.destroy()
    Button(fr_run,text='HOME',borderwidth=5,bg='brown',font=("Arial",15),command=home).grid(padx=5,row=0,column=8)
    
   
    
    conn.commit()
    conn.close()
    Add_Database_Details_win.destroy()
#----------------------------------------------------------------------------------------------------------------------------------------
def Add_Route_Details():
   
    conn=sqlite3.connect('bustables1.db')
   
    cur=conn.cursor()

    
    global Add_Route_Details_win
    Add_Route_Details_win = Toplevel()
    Add_Route_Details_win.title("Add New Route Details")
    Add_Route_Details_win.geometry('1920x1080')

   
    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(Add_Route_Details_win,image=img,relief='groove').pack()
    Label(Add_Route_Details_win, text="Online Bus Booking System",bg='sky blue',fg='red',pady=5,font=('Arial',25)).pack(padx=10,pady=15)
    Label(Add_Route_Details_win, text="Add New Bus Route Details",bg='green',fg='red',font=('Arial',20)).pack(padx=10)

    
    
    fr_route=Frame(Add_Route_Details_win)
    fr_route.pack(pady=15)
    
    lbl_routeid=Label(fr_route,text='Route Id',font=('Arial',15))
    lbl_routeid.grid(row=0,column=0)
    lbl_stnname=Label(fr_route,text='Station Name',font=('Arial',15))
    lbl_stnname.grid(row=0,column=2)
    lbl_stnid=Label(fr_route,text='Station Id',font=('Arial',15))
    lbl_stnid.grid(row=0,column=4)
   
    ent_routeid=Entry(fr_route)
    ent_routeid.grid(row=0,column=1)
    ent_stnname=Entry(fr_route)
    ent_stnname.grid(row=0,column=3)
    ent_stnid=Entry(fr_route)
    ent_stnid.grid(row=0,column=5)
    
    
    def addroute():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
       
        cur.execute('insert into route values(:rid,:stnname,:stnid)',
                    {
                        'rid':ent_routeid.get(),
                        'stnname':ent_stnname.get(),
                        'stnid':ent_stnid.get()
                    })
        cur.execute('select * from route')
        records=cur.fetchall()
        Label(fr_route,text=records[-1]).grid(row=1,column=0,columnspan=8)
    
        conn.commit()
        conn.close()
    
    
    def deleteroute():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
       
        cur.execute('delete from route where R_id=? and Stn_id=?',
                (ent_routeid.get(),ent_stnid.get())
        )
        cur.execute('select * from route')
        records=cur.fetchall()
        Label(fr_route,text=records).grid(row=1,column=0)
    
        conn.commit()
        conn.close()

    def check():
        if(ent_routeid.get()=='' or ent_stnname.get()=='' or ent_stnid.get()==''):
            response=messagebox.showerror('Invalid Details','Please Enter Valid Details')   
        else:
            addroute()
    
    btn_addroute=Button(fr_route,text='Add Route',bg='light green',font=('Arial',15),command=check)
    btn_addroute.grid(row=0,column=6)
   
    btn_deleteroute=Button(fr_route,text='Delete Route',bg='light green',fg='red',font=('Arial',15),command=deleteroute)
    btn_deleteroute.grid(row=0,column=7,padx=5)

    def home():
        create_window2(1)
        Add_Route_Details_win.destroy()
    Button(fr_route,text='HOME',borderwidth=5,bg='brown',font=('Arial',15),command=home).grid(padx=5,row=0,column=8)
    
    
    
  
    conn.commit()
    conn.close()
    Add_Database_Details_win.destroy()
#---------------------------------------------------------------------------------------------------------------------------------------
def Add_Bus_Details():
    
    conn=sqlite3.connect('bustables1.db')

    cur=conn.cursor()

    
    global Add_Bus_Details_win
    Add_Bus_Details_win = Toplevel()
    Add_Bus_Details_win.title("Add New Bus Details")
    Add_Bus_Details_win.geometry('1920x1080')
    
    
    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(Add_Bus_Details_win,image=img,relief='sunken').pack()
    Label(Add_Bus_Details_win, text="Online Bus Booking System",bg='sky blue',fg='red',font=("Arial",25)).pack(pady=15,padx=10)
    Label(Add_Bus_Details_win, text="Add New Bus Details",bg='green',fg='red',font=("Arial",20)).pack(padx=10)

    
    
    
    fr_bus=Frame(Add_Bus_Details_win)
    fr_bus.pack(pady=15,padx=10)
    
    lbl_bid=Label(fr_bus,text="Bus ID",font=("Arial",15))
    lbl_bid.grid(row=0,column=0)
    lbl_btype=Label(fr_bus,text="Bus Type",font=("Arial",15))
    lbl_btype.grid(row=0,column=2)

    
    btype=['Ac 2x2','Ac 3x2','Non Ac 2x2','Non Ac 3x2','Ac Sleeper 2x1','Non Ac Sleeper 2x1']
    select=StringVar()
    select.set(btype[0])
    drop=OptionMenu(fr_bus,select,*btype)
    drop.grid(row=0,column=3)

    lbl_bcapacity=Label(fr_bus,text="Capacity",font=("Arial",15))
    lbl_bcapacity.grid(row=0,column=4)
    lbl_bfare=Label(fr_bus,text="Fare Rs",font=("Arial",15))
    lbl_bfare.grid(row=0,column=6)
    lbl_boprid=Label(fr_bus,text="Operator ID",font=("Arial",15))
    lbl_boprid.grid(row=0,column=8)
    lbl_brid=Label(fr_bus,text="Route ID",font=("Arial",15))
    lbl_brid.grid(row=0,column=10)

    
    ent_bid=Entry(fr_bus)
    ent_bid.grid(row=0,column=1)
    ent_bcapacity=Entry(fr_bus)
    ent_bcapacity.grid(row=0,column=5)
    ent_bfare=Entry(fr_bus)
    ent_bfare.grid(row=0,column=7)
    ent_boprid=Entry(fr_bus)
    ent_boprid.grid(row=0,column=9)
    ent_brid=Entry(fr_bus)
    ent_brid.grid(row=0,column=11)

   
    def addbus():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
        
        cur.execute('insert into bus values(:a,:b,:c,:d,:e,:f)',
                {
                    'a':ent_bid.get(),
                    'b':select.get(),
                    'c':ent_bcapacity.get(),
                    'd':ent_bfare.get(),
                    'e':ent_boprid.get(),
                    'f':ent_brid.get()
                })
        cur.execute('select * from bus')
        records=cur.fetchall()
        lbl_display=Label(fr_bus,text=records[-1])
        lbl_display.grid(row=2,column=0,columnspan=11)
    
        conn.commit()
        conn.close()
   
    def editbus():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
       
        cur.execute("""update bus set
            B_type=:type,
            B_capacity=:capacity,
            B_fare=:fare,
            B_oprid=:oprid,
            B_rid=:rid
        
            where B_id=:id""",
            {
                'type':select.get(),
                'capacity':ent_bcapacity.get(),
                'fare':ent_bfare.get(),
                'oprid':ent_boprid.get(),
                'rid':ent_brid.get(),
                'id':ent_bid.get()
            })
        cur.execute('select * from bus')
        records=cur.fetchall()
        lbl_display=Label(fr_bus,text=records)
        lbl_display.grid(row=2,column=0,columnspan=11)
    
        conn.commit()
        conn.close()
   
    def addbuspopup():
        response=messagebox.showinfo('bus entry','bus record added')
        if(response=='ok'):
            addbus()
        else:
            return
   
    def editbuspopup():
        response=messagebox.showinfo('bus entry update','bus record updated successfully')
        if(response=='ok'):
            editbus()
        else:
            return

    def check():
        if(ent_bid.get()=='' or ent_bcapacity.get()=='' or ent_bfare.get()=='' or ent_boprid.get()=='' or ent_brid==''):
            response=messagebox.showerror('Invalid Details','Please Enter Valid Details')   
        else:
            addbuspopup()
   
    btn_addbus=Button(fr_bus,text='Add bus',bg='light green',font=("Arial",15),command=check)
    btn_addbus.grid(pady=15,row=1,column=0,columnspan=11)

    
    btn_editbus=Button(fr_bus,text='Edit bus',bg='light green',font=("Arial",15),command=editbuspopup)
    btn_editbus.grid(pady=15,row=1,column=1,columnspan=11)

    def home():
        create_window2(1)
        Add_Bus_Details_win.destroy()
    Home=Button(fr_bus,text='HOME',bg='brown',font=("Arial",15),command=home)
    Home.grid(row=1,column=3,columnspan=12)
    
    
    
    conn.commit()
    conn.close()
    Add_Database_Details_win.destroy()
#-----------------------------------------------------------------------------------------------------------------------------------------
#func to call new window Add_Operator_Details_win and destroy Add_Bus_Details_win
def Add_Operator_Details():
    
    conn=sqlite3.connect('bustables1.db')
    
    cur=conn.cursor()

  
    global Add_Operator_Details_win
    Add_Operator_Details_win = Toplevel()
    Add_Operator_Details_win.title("Add Operator Details")
    Add_Operator_Details_win.geometry('1920x1080')

   
    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(Add_Operator_Details_win,image=img,relief='groove').pack()
    Label(Add_Operator_Details_win, text="Online Bus Booking System",bg='sky blue',fg='red',pady=5,font=('Helvetica',25)).pack(pady=15)
    Label(Add_Operator_Details_win, text="Add Bus Operator Details",bg='green',fg='brown',font=('Helvetica',20)).pack()
  
   
    fr_operator=Frame(Add_Operator_Details_win)
    fr_operator.pack(pady=15)
    
    lbl_operatorid=Label(fr_operator,text='Operator id',font=('Helvetica',15))
    lbl_operatorid.grid(row=0,column=0)
    lbl_name=Label(fr_operator,text='Name',font=('Helvetica',15))
    lbl_name.grid(row=0,column=2)
    lbl_address=Label(fr_operator,text='Address',font=('Helvetica',15))
    lbl_address.grid(row=0,column=4)
    lbl_phone=Label(fr_operator,text='Phone',font=('Helvetica',15))
    lbl_phone.grid(row=0,column=6)
    lbl_email=Label(fr_operator,text='Email',font=('Helvetica',15))
    lbl_email.grid(row=0,column=8)

  
    ent_operatorid=Entry(fr_operator)
    ent_operatorid.grid(row=0,column=1)
    ent_name=Entry(fr_operator)
    ent_name.grid(row=0,column=3)
    ent_address=Entry(fr_operator)
    ent_address.grid(row=0,column=5)
    ent_phone=Entry(fr_operator)
    ent_phone.grid(row=0,column=7)
    ent_email=Entry(fr_operator)
    ent_email.grid(row=0,column=9)

    
    def addoperator():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
        
        cur.execute('insert into operator values(:opr_id,:opr_name,:opr_address,:opr_phone,:opr_email)',
                {
                    'opr_id':ent_operatorid.get(),
                    'opr_name':ent_name.get(),
                    'opr_address':ent_address.get(),
                    'opr_phone':ent_phone.get(),
                    'opr_email':ent_email.get()
                })
        cur.execute('select * from operator')
        records=cur.fetchall()
        lbl_display=Label(fr_operator,text=records[-1])
        lbl_display.grid(row=1,column=0,columnspan=11)
    
        conn.commit()
        conn.close()

   
    def editoperator():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
        
        cur.execute("""update operator set
            opr_name=:name,
            opr_address=:address,
            opr_phone=:phone,
            opr_email=:email

            where opr_id=:id""",
            {
                'name':ent_name.get(),
                'address':ent_address.get(),
                'phone':ent_phone.get(),
                'email':ent_email.get(),

                'id':ent_operatorid.get()
            })
        cur.execute('select * from operator')
        records=cur.fetchall()
        lbl_display=Label(fr_operator,text=records)
        lbl_display.grid(row=1,column=0,columnspan=11)
    
        conn.commit()
        conn.close()
   
    def opraddpopup():
        response=messagebox.showinfo('operator entry','operator record added')
        if(response=='ok'):
            addoperator()
        else:
            return
    
    def opreditpopup():
        response=messagebox.showinfo('operator entry update','operator record updated successfully')
        if(response=='ok'):
            editoperator()
        else:
            return

    
    def check():
        if(len(ent_phone.get())!=10 or ent_operatorid.get()=='' or ent_name.get()=='' or ent_address.get()=='' or ent_email.get()==''):
            response=messagebox.showerror('Invalid Entries','Please Enter Valid Details')
            
        else:
            opraddpopup()
        
    
    btn_opradd=Button(fr_operator,text='ADD',bg='light green',command=check,font=('Arial',15))
    btn_opradd.grid(row=0,column=10,padx=5)

    
    btn_opredit=Button(fr_operator,text='EDIT',bg='light green',command=opreditpopup,font=('Arial',15))
    btn_opredit.grid(row=0,column=11)

    def home():
        create_window2(1)
        Add_Operator_Details_win.destroy()
    Button(fr_operator,text='HOME',borderwidth=5,bg='brown',command=home,font=('Helvetica',15)).grid(padx=5,row=0,column=12)
    

  
    conn.commit()
    conn.close()
    Add_Database_Details_win.destroy()
#--------------------------------------------------------------------------------------------------------------------------------------
def Add_Database_Details():
    #create a database
    conn=sqlite3.connect('bustables1.db')
    #create cursor
    cur=conn.cursor()

    # Create a new window
    global Add_Database_Details_win
    Add_Database_Details_win = Toplevel()
    Add_Database_Details_win.title("Add Bus Details")
    Add_Database_Details_win.geometry('1920x1080')

   
    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(Add_Database_Details_win,image=img,relief='groove').pack()
    Label(Add_Database_Details_win, text="Online Bus Booking System",bg='sky blue',fg='red',pady=5,font=("Helvetica",25)).pack(ipadx=100,pady=15)
    Label(Add_Database_Details_win, text="Add New Details to DataBase",fg='brown',bg='light green',font=("Helvetica",20)).pack()
    
    fr1=Frame(Add_Database_Details_win)
    fr1.pack(pady=15)
    
  
    btn_newoperator=Button(fr1,text='New Operator',bg='sky blue',font=("Helvetica",15),command=Add_Operator_Details)
    btn_newoperator.grid(row=0,column=0,padx=10)
    btn_newbus=Button(fr1,text='New Bus',bg='sky blue',font=("Helvetica",15),command=Add_Bus_Details)
    btn_newbus.grid(row=0,column=1)
    btn_newroute=Button(fr1,text='New Route',bg='sky blue',font=("Helvetica",15),command=Add_Route_Details)
    btn_newroute.grid(row=0,column=2,padx=10)
    btn_newrun=Button(fr1,text='New Run',bg='sky blue',font=("Helvetica",15),command=Add_Run_Details)
    btn_newrun.grid(row=0,column=3)

    def home():
        create_window2(1)
        Add_Database_Details_win.destroy()
    Button(fr1,text='HOME',borderwidth=5,bg='brown',command=home).grid(padx=10,row=0,column=4)
    
   
    conn.commit()
    conn.close()
    
    
    window2.withdraw()
#-------------------------------------------------------------------------------------------------------------------------------------
def Check_Booked_Seat():
    
    conn=sqlite3.connect('bustables1.db')
  
    cur=conn.cursor()
    
    
    global check_Booked_win
    check_Booked_win = Toplevel()
    check_Booked_win.title("check Booked Seat")
    check_Booked_win.geometry('1920x1080')

   
    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(check_Booked_win,image=img,relief='groove').pack()
    Label(check_Booked_win, text="Online Bus Booking System",bg='sky blue',fg='red',font=('Helvetica',25),pady=5).pack(pady=15)
    Label(check_Booked_win, text="Check Your Booking",bg='light green',font=('Helvetica',15)).pack()

    
    fr_detail=Frame(check_Booked_win)
    fr_detail.pack(pady=15)
    Label(fr_detail,text='Enter Your Mobile No:',font=('Helvetica',15)).grid(row=0,column=0,padx=5)
    Mobile=Entry(fr_detail)
    Mobile.grid(row=0,column=1)

    
    def check_Booking():
        
        conn=sqlite3.connect('bustables1.db')
        
        cur=conn.cursor()
        
        fr1=Frame(check_Booked_win,borderwidth=2,relief=SUNKEN)
        fr1.pack()

        
        cur.execute('select *,oid from passenger_ticket where Mobile_no=?',(Mobile.get(),))
        data=cur.fetchall()
        if(data==[]):
            response=messagebox.showerror('ERROR','Record not found!')
        else:
            Label(fr1,text='Passengers : '+data[0][0]).grid(row=0,column=0)
            Label(fr1,text='Gender : '+data[0][1]).grid(row=0,column=1)
            Label(fr1,text='No of Seats : '+str(data[0][2])).grid(row=1,column=0)
            Label(fr1,text='Phone : '+str(data[0][3])).grid(row=1,column=1)
            Label(fr1,text='Age : '+str(data[0][4])).grid(row=2,column=0)
            Label(fr1,text='Fare Rs : '+str(data[0][5])).grid(row=2,column=1)
            Label(fr1,text='Travel ON : '+data[0][6]).grid(row=3,column=0)
            Label(fr1,text='Boarding Point : '+data[0][7]).grid(row=3,column=1)
            Label(fr1,text='Destination Point : '+data[0][8]).grid(row=4,column=0)
            Label(fr1,text='Bus Detail : '+data[0][9]).grid(row=4,column=1)
            Label(fr1,text='Booking Ref : '+str(data[0][11])).grid(row=5,column=0)
            cur.execute('select Fare from passenger_ticket where Mobile_no=?',(Mobile.get(),))
            fare=cur.fetchall()
            Label(fr1,text='Total amount Rs '+str(fare[0][0])+'/- to be paid at the time of boarding the bus',font=("Arial",12,"italic")).grid(row=6,column=0,columnspan=2)
        
        
        conn.commit()
        conn.close()
    def check_entry():
        if(Mobile.get()):
            check_Booking()
        else:
            response=messagebox.showwarning('ERROR','Please Enter a valid Value')
    
    btn1=Button(fr_detail,text='Check Booking',borderwidth=5,bg='light green',command=check_entry)
    btn1.grid(row=0,column=2,padx=5)
    def home():
        create_window2(1)
        check_Booked_win.destroy()
    Button(fr_detail,text='HOME',borderwidth=5,bg='brown',command=home).grid(row=0,column=3)

    
    conn.commit()
    conn.close()
    
   
    window2.withdraw()
#----------------------------------------------------------------------------------------------------------------------------------------
def ticket_window(ent_mobile):
    mob=ent_mobile.get()

    conn=sqlite3.connect('bustables1.db')
    #create cursor
    cur=conn.cursor()


    global ticket_win
    ticket_win = Toplevel()
    ticket_win.title("Ticket window")
    ticket_win.geometry('1920x1080')


    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(ticket_win,image=img,relief='groove').pack()
    Label(ticket_win, text="Online Bus Booking System",bg='sky blue',fg='red',font=("Helvetica",25)).pack(pady=15)
    Label(ticket_win, text="Bus ticket",fg='red',bg='light green',font=("Helvetica",15)).pack()

 
    fr1=Frame(ticket_win,relief='sunken',borderwidth=2)
    fr1.pack(padx=10,pady=10)
    
    cur.execute('select *,oid from passenger_ticket where Mobile_no=?',(mob,))
    data=cur.fetchall()
    Label(fr1,text='Passengers : '+data[0][0]).grid(row=0,column=0)
    Label(fr1,text='Gender : '+data[0][1]).grid(row=0,column=1)
    Label(fr1,text='No of Seats : '+str(data[0][2])).grid(row=1,column=0)
    Label(fr1,text='Phone : '+str(data[0][3])).grid(row=1,column=1)
    Label(fr1,text='Age : '+str(data[0][4])).grid(row=2,column=0)
    Label(fr1,text='Fare Rs : '+str(data[0][5])).grid(row=2,column=1)
    Label(fr1,text='Travel ON : '+data[0][6]).grid(row=3,column=0)
    Label(fr1,text='Boarding Point : '+data[0][7]).grid(row=3,column=1)
    Label(fr1,text='Destination Point : '+data[0][8]).grid(row=4,column=0)
    Label(fr1,text='Bus Detail : '+data[0][9]).grid(row=4,column=1)
    Label(fr1,text='Booking Ref : '+str(data[0][11])).grid(row=5,column=0)
    cur.execute('select Fare from passenger_ticket where Mobile_no=?',(mob,))
    fare=cur.fetchall()
    Label(fr1,text='Total amount Rs '+str(fare[0][0])+'/- to be paid at the time of boarding the bus',font=("Arial",12,"italic")).grid(row=6,column=0,columnspan=2)
    response=messagebox.showinfo('success','seat booked...')

    def home():
        create_window2(1)
        ticket_win.destroy()
    Button(fr1,text='HOME',borderwidth=5,bg='brown',command=home).grid(row=7,column=0,columnspan=2)
    

    conn.commit()
    conn.close()
    Seat_Booking_win.destroy()
#---------------------------------------------------------------------------------------------------------------------------------------
def Seat_Booking():
    #create a database
    conn=sqlite3.connect('bustables1.db')
    #create cursor
    cur=conn.cursor()
    

    global Seat_Booking_win
    Seat_Booking_win = Toplevel()
    Seat_Booking_win.title("Seat Booking")
    Seat_Booking_win.geometry('1920x1080')


    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(Seat_Booking_win,image=img).pack()
    Label(Seat_Booking_win, text="Online Bus Booking System",bg='sky blue',fg='red',font=('Helvetica',25)).pack(ipadx=120,pady=20)
    Label(Seat_Booking_win, text="Enter Journey Details",bg='light green',font=('Arial',20)).pack()

  
    fr_show=Frame(Seat_Booking_win)
    fr_show.pack(pady=15)

    lbl_to=Label(fr_show,text='To',font=('Arial',15))
    lbl_to.grid(row=0,column=0)
    lbl_from=Label(fr_show,text='From',font=('Arial',15))
    lbl_from.grid(row=0,column=2)
    lbl_jdate=Label(fr_show,text='Journey Date(dd/mm/yyyy)',font=('Arial',15))
    lbl_jdate.grid(row=0,column=4)


    global ent_to
    global ent_from
    global ent_jdate

    ent_to=Entry(fr_show)
    ent_to.grid(row=0,column=1)
    ent_from=Entry(fr_show)
    ent_from.grid(row=0,column=3)
    ent_jdate=Entry(fr_show)
    ent_jdate.grid(row=0,column=5)



    def proceedtobook(selected_bid):
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
        
   
        fr_passenger=Frame(Seat_Booking_win)
        fr_passenger.pack()
 
        lbl_name=Label(fr_passenger,text='Name')
        lbl_name.grid(row=0,column=0)
        lbl_gender=Label(fr_passenger,text='Gender')
        lbl_gender.grid(row=0,column=2)
        lbl_seats=Label(fr_passenger,text='No of Seats')
        lbl_seats.grid(row=0,column=4)
        lbl_mobile=Label(fr_passenger,text='Mobile NO')
        lbl_mobile.grid(row=0,column=6)
        lbl_age=Label(fr_passenger,text='Age')
        lbl_age.grid(row=0,column=8)
    
     
        global ent_seats
        ent_name=Entry(fr_passenger)
        ent_name.grid(row=0,column=1)
        ent_seats=Entry(fr_passenger)
        ent_seats.grid(row=0,column=5)
        global ent_mobile
        ent_mobile=Entry(fr_passenger)
        ent_mobile.grid(row=0,column=7)
        ent_age=Entry(fr_passenger)
        ent_age.grid(row=0,column=9)

       
        gender=['male','female','third gender']
        gen=StringVar()
        gen.set(gender[0])
        drop=OptionMenu(fr_passenger,gen,*gender)
        drop.grid(row=0,column=3)

        
        def bookseat():
            
            conn=sqlite3.connect('bustables1.db')
            
            cur=conn.cursor()

            cur.execute('''select bus.B_fare, operator.Opr_name
                from bus
                inner join operator on bus.B_oprid=operator.Opr_id
                where B_id=?''',(selected_bid,))
            test=cur.fetchall()
            total_fare=int(ent_seats.get())*test[0][0]
            op_name=test[0][1]

      
            cur.execute('update run set Run_seatavailable=? where Run_bid=?',(seat_diff,selected_bid))
        
            
            cur.execute('insert into passenger_ticket values(:a,:b,:c,:d,:e,:f,:g,:h,:i,:j,:k)',
                {
                    'a':ent_name.get(),
                    'b':gen.get(),
                    'c':ent_seats.get(),
                    'd':ent_mobile.get(),
                    'e':ent_age.get(),
                    'f':total_fare,
                    'g':ent_jdate.get(),
                    'h':ent_from.get(),
                    'i':ent_to.get(),
                    'j':op_name,
                    'k':selected_bid
                })
            '''
            cur.execute('select * from passenger_ticket')
            records=cur.fetchall()
            lbl_display=Label(fr_passenger,text=records[-1])
            lbl_display.grid(row=1,column=0,columnspan=11)
            '''
        
          
            conn.commit()
       
            conn.close()
            ticket_window(ent_mobile)
            
   
        def popup():
            conn=sqlite3.connect('bustables1.db')
            cur=conn.cursor()
        
            cur.execute('select B_fare from bus where B_id=?',(selected_bid,))
            fare=cur.fetchall()
            response=messagebox.askyesno('Fare confirm','Total amount to be paid Rs'+str(int(ent_seats.get())*fare[0][0]))
            if(response==1):
                bookseat()
            else:
                return
        
            conn.commit()
            conn.close()
        def check():
            conn=sqlite3.connect('bustables1.db')
            cur=conn.cursor()
            cur.execute('select Run_seatavailable from run where Run_bid=?',(selected_bid,))
            seat_avl=cur.fetchall()
            
            mobile_value=ent_mobile.get()
            age=ent_age.get()
            if(age!=''):
                int_age=int(age)
            global seat_diff
            seat_diff=seat_avl[0][0]-int(ent_seats.get())
            if(len(mobile_value)!=10 or seat_diff<=0 or ent_name.get()=='' or ent_seats.get()=='' or ent_age.get()=='' or int_age>=120 or int_age<1):
                response=messagebox.showerror('Invalid Details','Please Enter Valid Details')
                
            else:
                popup()
            conn.commit()
            conn.close()
            
       
        btn_bookseat=Button(fr_passenger,text='Book Seat',bg='light green',command=check)
        btn_bookseat.grid(row=0,column=10)

        conn.commit()
        conn.close()



    def showbus():
        conn=sqlite3.connect('bustables1.db')
        cur=conn.cursor()
    
        Label(fr_show,text='Select Bus',fg='green').grid(row=1,column=0)
        Label(fr_show,text='Bus Type',fg='green').grid(row=1,column=1)
        Label(fr_show,text='Operator',fg='green').grid(row=1,column=2)
        Label(fr_show,text='Available',fg='green').grid(row=1,column=3)
        Label(fr_show,text='Capacity',fg='green').grid(row=1,column=4)
        Label(fr_show,text='Fare',fg='green').grid(row=1,column=5)

        
        global selected_bus_id
        selected_bus_id = IntVar()

        cur.execute('''select distinct bus.B_id,bus.B_type,operator.Opr_name,run.Run_seatavailable,bus.B_capacity,bus.B_fare
                    from route
                    inner join bus on route.R_id=bus.B_rid
                    inner join operator on bus.B_oprid=operator.Opr_id
                    inner join run on bus.B_id=run.Run_bid
                    where (route.Stn_name=? or route.Stn_name=?) and run.Run_date=? and
                    route.R_id IN (
                        SELECT R_id
                        FROM route
                        WHERE Stn_name = ? OR Stn_name = ?
                        GROUP BY R_id
                        HAVING COUNT(DISTINCT Stn_name) = 2
                    )
                    ''',(ent_to.get(),ent_from.get(),ent_jdate.get(),ent_to.get(),ent_from.get()))
        final=cur.fetchall()

       
        row_num = 2  
        for row in final:
          
            Radiobutton(fr_show, variable=selected_bus_id, value=row[0]).grid(row=row_num, column=0)
            for col_num, value in enumerate(row[1:]):
                Label(fr_show, text=value).grid(row=row_num, column=col_num + 1)
            row_num += 1
    
       
        btn_sendbid=Button(fr_show,text='Proceed to Book',bg='light green',command=lambda: proceedtobook(selected_bus_id.get()))
        btn_sendbid.grid(row=2,column=6)
    
        conn.commit()
        conn.close()

   
    btn_showbus=Button(fr_show,text='SHOW BUS',bg='green',borderwidth=5,command=showbus)
    btn_showbus.grid(row=0,column=6,padx=10)

    def home():
        create_window2(1)
        Seat_Booking_win.destroy()
    Button(fr_show,text='HOME',bg='brown',borderwidth=5,command=home).grid(row=0,column=7)


    conn.commit()
    conn.close()
   
    window2.withdraw()

def create_window2(event):
    
    global window2
    window2 = Toplevel(root)
    window2.title("Window 2")
    window2.geometry('1920x1080')

    
    global img
    img=ImageTk.PhotoImage(Image.open('python_bus.png'))
    Label(window2,image=img,relief='sunken').pack()
    Label(window2, text="Online Bus Booking System",font=('Helvetica',25),fg='red',bg='light blue').pack(ipadx=80,pady=25)

 
    fr1=Frame(window2)
    fr1.pack()

    btn1=Button(fr1,text='Seat Booking',bg='light green',font=('Helvetica',15),command=Seat_Booking)
    btn1.grid(row=0,column=0,padx=10)
    
    btn2=Button(fr1,text='Check Booked Seat',bg='light green',font=('Helvetica',15),command=Check_Booked_Seat)
    btn2.grid(row=0,column=1,padx=10)
    
    btn3=Button(fr1,text='Add Database Details',bg='light green',font=('Helvetica',15),command=Add_Database_Details)
    btn3.grid(row=0,column=2,padx=10)

    Label(fr1,text='For Admin Only',fg='red').grid(row=1,column=2,pady=5)

  
    root.withdraw()



root = Tk()
root.title("Window 1")
root.geometry('1920x1080')


img=ImageTk.PhotoImage(Image.open('python_bus.png'))
Label(root,image=img,relief='sunken').pack()
label1 = Label(root, text="Online Bus Booking System",fg='red',bg='light blue',pady=5,font=("Helvetica", 24))
label1.pack(pady=10)
Label(root,text="Name: Rutuja Patil",fg='blue',font=('Helvetica',15)).pack(pady=10)
Label(root,text="Er : 221B496",fg='blue',font=('Helvetica',15)).pack(pady=10)
Label(root,text="Mobile: 9022051650",fg='blue',font=('Helvetica',15)).pack(pady=10)
Label(root,text="Submitted to: Dr. Mahesh Kumar",fg='red',bg='light blue',font=('Helvetica',15)).pack(pady=10)
Label(root,text="Project Based Learning",fg='red',font=('Helvetica',15)).pack(pady=10)


root.bind('<KeyPress>', create_window2)

conn.commit()
conn.close()
root.mainloop()
