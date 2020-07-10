from tkinter import *
import datetime
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk

root = Tk()
root.title('KP & Associates Attendance Register')
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='office icon.png'))
#root.geometry('200x100')
F_m = LabelFrame(root)
F_m.pack()

f_l = LabelFrame(F_m)
f_l.grid(row=0, column=0, sticky=W+E)

f_r = LabelFrame(F_m)
f_r.grid(row=0, column=1, sticky=N)


con = sqlite3.connect('Attendance.db')
c = con.cursor()

c.execute("CREATE TABLE IF NOT EXISTS staff (name TEXT, post TEXT, salary INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS date_t (date TEXT, day TEXT, month TEXT, year text)")
#c.execute("DROP TABLE date_t")
#c.execute("INSERT INTO staff VALUES (:name, :post, :salary)", {'name': 'a', 'post': 'CKJ', 'salary': 100})



staff_name = []
staff_id = []
staff_post = []
staff_salary = []

staff_t_data = []
staff_salary_data = []

row_no = [1]

temp = {}
n_c = 0

day = datetime.date.today().day
month = datetime.date.today().month
year = datetime.date.today().year
date = str(day)+'-'+str(month)+'-'+str(year)

c.execute("SELECT * from date_t")
yesterday = c.fetchall()
yesterday_date = yesterday[-1][0]
yesterday_day = yesterday[-1][1]
yesterday_month = yesterday[-1][2]
yesterday_year = yesterday[-1][3]



def cre_list():
    global staff_id, staff_name, staff_post, staff_salary, row_no, staff_t_data, staff_salary_data
    con = sqlite3.connect('Attendance.db')
    c = con.cursor()

    c.execute("SELECT oid, name, post, salary FROM staff")
    db_staff_data = c.fetchall()
    for id, name, post, salary in db_staff_data:
        staff_id.append(id)
        staff_name.append(name)
        staff_post.append(post)
        staff_salary.append(salary)

        row_no.append(row_no[-1]+1)
    row_no.remove(row_no[-1])
    staff_t_data = list(zip(row_no, staff_id, staff_name))
    staff_salary_data = list(zip(staff_name, staff_salary))


    con.commit()
    con.close()

def cl_list():
    global staff_id, staff_name, staff_post, staff_salary, row_no, staff_t_data, staff_salary_data
    staff_id.clear()
    staff_name.clear()
    staff_post.clear()
    staff_salary.clear()
    row_no = [1]
    staff_t_data.clear()
    staff_salary_data.clear()

def cre_table():
    global staff_name
    con = sqlite3.connect('Attendance.db')
    c = con.cursor()

    for name in staff_name:
        #c.execute("DROP TABLE %s" % (name))
        c.execute("CREATE TABLE IF NOT EXISTS %s (date TEXT, day TEXT, month TEXT, year text, ap TEXT);" % (name))
        #c.execute("SELECT * FROM %s;" % (name))
        #print(c.fetchall())

    con.commit()
    con.close()

def today_temp():
    global temp, n_c
    r = dict(zip(staff_name, row_no))
    db_row_no = []
    db_id = []
    db_name = []
    db_ap = []
    for name in staff_name:
        db_row_no.append(r.get(name))

        c.execute("SELECT oid, name FROM staff WHERE name=:name", {'name': name})
        db_app = c.fetchall()
        db_id.append(db_app[0][0])
        db_name.append(db_app[0][1])

        c.execute("SELECT ap FROM %s WHERE date=:date LIMIT 1;" % (name), {'date': date})
        try:
            ap = c.fetchall()[0][0]
        except:
            ap = 'none'
        db_ap.append(ap)

    l_for_temp = list(zip(db_row_no, db_id, db_name, db_ap))

    for r_l, id_l, name_l, ap_l in l_for_temp:
        temp[id_l] = (r_l, id_l, name_l, ap_l)
    if db_ap.count('Present') > 0 or db_ap.count('Absent') > 0 :
        temp[444] = (row_no[-1], 444, 'All Present', 'Present')
    else:
        temp[444] = (row_no[-1], 444, 'All Present', 'none')

    n_c = db_ap.count('none')


def p(v_r, id, name):
    b_p = Button(f_l, text='Present', state=DISABLED, bg='yellow')
    b_p.grid(row=int(v_r)-1, column=2, pady=(5, 0), padx=(5, 0))

    b_a = Button(f_l, text='Absent', state=DISABLED)
    b_a.grid(row=int(v_r)-1, column=3, pady=(5, 0), padx=(5, 5))

    con = sqlite3.connect('Attendance.db')
    c = con.cursor()

    c.execute('''INSERT INTO %s VALUES (:date, :d, :m, :y, :present) ''' % (name), {'date': date, 'd': day, 'm': month, 'y': year, 'present': 'Present'})

    c.execute('SELECT * FROM %s;' % (name))

    temp[v_r] = (v_r, id, name, 'Present')

    con.commit()
    con.close()

    b_all_p = Button(f_l, text='All Present', state=DISABLED)
    b_all_p.grid(row=int(int(row_no[-1])), column=0, columnspan=4, pady=(5, 0))
    temp[444] = (row_no[-1], 444, 'All Present', 'Present')

def a(v_r, id, name):
    b_p = Button(f_l, text='Present', state=DISABLED)
    b_p.grid(row=int(v_r)-1, column=2, pady=(5, 0), padx=(5, 0))

    b_a = Button(f_l, text='Absent', state=DISABLED, bg='red')
    b_a.grid(row=int(v_r)-1, column=3, pady=(5, 0), padx=(5, 5))

    con = sqlite3.connect('Attendance.db')
    c = con.cursor()

    c.execute('''INSERT INTO %s VALUES (:date, :d, :m, :y, :absent) ''' % (name), {'date': date, 'd': day, 'm': month, 'y': year, 'absent': 'Absent'})

    c.execute('SELECT * FROM %s;' % (name))

    temp[v_r] = (v_r, id, name, 'Absent')

    con.commit()
    con.close()

    b_all_p = Button(f_l, text='All Present', state=DISABLED)
    b_all_p.grid(row=int(int(row_no[-1])), column=0, columnspan=4, pady=(6, 0))
    temp[444] = (row_no[-1], 444, 'All Present', 'Present')

def all_p():
    global temp, staff_t_data, f_l, b_p, b_a, b_all_p
    for var_row, id, name in staff_t_data:
        b_p = Button(f_l, text='Present', state=DISABLED, bg='yellow')
        b_p.grid(row=int(var_row) - 1, column=2, pady=(5, 0), padx=(5, 0))

        b_a = Button(f_l, text='Absent', state=DISABLED)
        b_a.grid(row=int(var_row) - 1, column=3, pady=(5, 0), padx=(5, 5))

        con = sqlite3.connect('Attendance.db')
        c = con.cursor()

        c.execute('''INSERT INTO %s VALUES (:date, :d, :m, :y, :present) ''' % (name),
                  {'date': date, 'd': day, 'm': month, 'y': year, 'present': 'Present'})

        c.execute('SELECT * FROM %s;' % (name))

        #c.execute("INSERT INTO t_true VALUES (:true)", {'true': 'true'})

        temp[var_row] = (var_row, id, name, 'Present')

        con.commit()
        con.close()

    b_all_p = Button(f_l, text='All Present', state=DISABLED)
    b_all_p.grid(row=int(int(row_no[-1])), column=0, columnspan=4, pady=(5, 0))

    temp[444] = (row_no[-1], 444, 'All Present', 'Present')

def refresh():
    global f_l, temp
    f_l.destroy()
    f_l = LabelFrame(F_m)
    f_l.grid(row=0, column=0, sticky=W + E)
    cl_list()
    cre_list()
    cre_table()
    row_no.append(444)
    for num in row_no:
        t_l = [temp.get(num)]
        for var_row, id, name, pa in t_l:
            if pa == 'Present':
                if id != 444:
                    sr = Label(f_l, text=id, width=5, anchor=W)
                    sr.grid(row=int(var_row) - 1, column=0, pady=(7, 0), sticky=W)

                    l_name = Label(f_l, text=name, width=15, anchor=W)
                    l_name.grid(row=int(var_row) - 1, column=1, pady=(5, 0), sticky=W)

                    b_p = Button(f_l, text='Present', state=DISABLED, bg='yellow')
                    b_p.grid(row=int(var_row) - 1, column=2, pady=(5, 0), padx=(5, 0))

                    b_a = Button(f_l, text='Absent', state=DISABLED)
                    b_a.grid(row=int(var_row) - 1, column=3, pady=(5, 0), padx=(5, 5))
                else:
                    b_all_p = Button(f_l, text='All Present', state=DISABLED)
                    b_all_p.grid(row=row_no[-2], column=0, columnspan=4, pady=(5, 0))


            elif pa == 'Absent':
                sr = Label(f_l, text=id, width=5, anchor=W)
                sr.grid(row=int(var_row) - 1, column=0, pady=(7, 0), sticky=W)

                l_name = Label(f_l, text=name, width=15, anchor=W)
                l_name.grid(row=int(var_row) - 1, column=1, pady=(5, 0), sticky=W)

                b_p = Button(f_l, text='Present', state=DISABLED)
                b_p.grid(row=int(var_row) - 1, column=2, pady=(5, 0), padx=(5, 0))

                b_a = Button(f_l, text='Absent', state=DISABLED, bg='red')
                b_a.grid(row=int(var_row) - 1, column=3, pady=(5, 0), padx=(5, 5))

            elif pa == 'none':
                if id != 444:
                    sr = Label(f_l, text=id, width=5, anchor=W)
                    sr.grid(row=int(var_row) - 1, column=0, pady=(7, 0), sticky=W)

                    l_name = Label(f_l, text=name, width=15, anchor=W)
                    l_name.grid(row=int(var_row) - 1, column=1, pady=(5, 0), sticky=W)

                    b_p = Button(f_l, text='Present', command=lambda r=int(var_row), i=id, n=str(name): p(r, i, n))
                    b_p.grid(row=int(int(var_row) - 1), column=2, pady=(5, 0), padx=(5, 0), sticky=W)

                    b_a = Button(f_l, text='Absent', command=lambda r=int(var_row), i=id, n=str(name): a(r, i, n))
                    b_a.grid(row=int(int(var_row) - 1), column=3, pady=(5, 0), padx=(5, 5), sticky=W)
                else:
                    b_all_p = Button(f_l, text='All Present', command=all_p)
                    b_all_p.grid(row=row_no[-2], column=0, columnspan=4, pady=(5, 0))
    row_no.remove(444)

def sal():
    global month
    sal_win = Tk()
    sal_win.title('Salary Window')
    sal_win.iconbitmap('office icon.ico')

    con = sqlite3.connect('Attendance.db')
    c = con.cursor()
    var_row = 0
    for name, sal in staff_salary_data:
        Label(sal_win, text=name, width=15).grid(row=var_row, column=0, sticky=W, ipadx=30)
        c.execute("SELECT * FROM %s WHERE month=%s;" % (name, month))
        t_L = c.fetchall()
        x = len(t_L)
        y = []
        if x > 27:
            for n in range(x):
                y.append(t_L[n][-1])
            if x == 28:
                Label(sal_win, text='Rs. '+str((int(y.count('Present'))+3)*sal), width=15).grid(row=var_row, column=1, sticky=W, ipadx=30)
                var_row += 1
            if x == 29:
                Label(sal_win, text='Rs. '+str((int(y.count('Present'))+2)*sal), width=15).grid(row=var_row, column=1, sticky=W, ipadx=30)
                var_row += 1
            if x == 30:
                Label(sal_win, text='Rs. '+str((int(y.count('Present'))+1)*sal), width=15).grid(row=var_row, column=1, sticky=W, ipadx=30)
                var_row += 1
            if x == 31:
                Label(sal_win, text='Rs. '+str((int(y.count('Present')))*sal), width=15).grid(row=var_row, column=1, sticky=W, ipadx=30)
                var_row += 1

        else:
            for n in range(x):
                y.append(t_L[n][-1])
            Label(sal_win, text='Rs. '+str(int(y.count('Present'))*sal), width=15).grid(row=var_row, column=1, sticky=W)
            var_row += 1

    con.commit()
    con.close()
    sal_win.mainloop()

def cancel(ea):
    global editor, add_win
    if ea == 'editing':
        yn = messagebox.askyesno('Cancel Editing', 'Do you want to cancel editing?')
        if yn == 1:
            editor.destroy()
    elif ea == 'adding':
        yn2 = messagebox.askyesno('Cancel Adding', 'Do you want to cancel adding a staff member?')
        if yn2 == 1:
            add_win.destroy()

def save(ea):
    global edit_box, ed_name_box, ed_post_box, ed_salary_box, editor, add_win, a_name_box, a_post_box, a_salary_box, var_name, temp
    if ea == 'editing':
        con = sqlite3.connect('Attendance.db')
        c = con.cursor()

        g_id = edit_box.get()
        g_name = ed_name_box.get()
        g_post = ed_post_box.get()
        g_salary = ed_salary_box.get()

        c.execute('UPDATE staff SET name = :name,post=:post, salary = :salary WHERE oid = :id', {'name': g_name, 'post': g_post, 'salary': g_salary, 'id': g_id})
        try:
            c.execute("ALTER TABLE %s RENAME TO %s;" % (var_name, g_name))
        except:
            pass

        r = [temp.get(int(g_id))]
        v_r = r[0][0]
        ap = r[0][-1]
        temp[int(g_id)] = (v_r, int(g_id), g_name, ap)
        con.commit()
        con.close()
        editor.destroy()
        refresh()

    elif ea == 'adding':
        g_name = a_name_box.get()
        g_post = a_post_box.get()
        g_salary = a_salary_box.get()
        if g_name != '' and g_salary != '':
            con = sqlite3.connect('Attendance.db')
            c = con.cursor()

            print(g_name, g_post, g_salary)

            r = row_no[-1] + 1
            i = staff_id[-1]+1
            temp[i] = (r, i, g_name, 'none')

            c.execute("INSERT INTO staff VALUES (:name, :post, :salary)", {'name': g_name, 'post': g_post, 'salary': g_salary})

            con.commit()
            con.close()
            add_win.destroy()
            refresh()


        elif g_name == '' and g_salary == '':
            Label(add_win, text='Re-enter').grid(row=3, column=0, columnspan=4)

def edit_data(id):
    global editor, ed_name_box, ed_salary_box, ed_post_box, var_name
    if id != '':
        try:
            con = sqlite3.connect('Attendance.db')
            c = con.cursor()

            g_every_data = c.execute('SELECT * FROM staff WHERE oid = %s;' % (id)).fetchall()

            var_name = g_every_data[0][0]

            f_edit_data = LabelFrame(editor, text='Edit Data')
            f_edit_data.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=W+E)

            b_edit_data = Button(editor, text='Edit Data', width=10, state=DISABLED)
            b_edit_data.grid(row=1, column=0, columnspan=2, pady=5)

            Label(f_edit_data, text='You are editing id. no. '+str(id)).grid(row=0, column=0, columnspan=4)



            f_name_l = Label(f_edit_data, text='Name :')
            f_name_l.grid(row=1, column=0, pady=(0, 5))

            ed_name_box = Entry(f_edit_data, width=12)
            ed_name_box.insert(0, g_every_data[0][0])
            ed_name_box.grid(row=1, column=1, padx=(2, 5), pady=(0, 5), ipadx=60, columnspan=3)

            f_post_l = Label(f_edit_data, text='Post   :')
            f_post_l.grid(row=2, column=0, pady=(0, 5))

            ed_post_box = Entry(f_edit_data)
            ed_post_box.insert(0, g_every_data[0][1])
            ed_post_box.grid(row=2, column=1, padx=(2, 5), pady=(0, 5), sticky=W+E, columnspan=3)

            f_salary_l = Label(f_edit_data, text='Salary :')
            f_salary_l.grid(row=3, column=0, pady=(0, 5))

            ed_salary_box = Entry(f_edit_data)
            ed_salary_box.insert(0, g_every_data[0][2])
            ed_salary_box.grid(row=3, column=1, padx=(2, 5), pady=(0, 5), sticky=W+E, columnspan=3)

            b_save = Button(f_edit_data, text='Save', command=lambda: save('editing'))
            b_save.grid(row=4, column=0, padx=(2, 5), pady=(0, 5), sticky=W+E, columnspan=2)

            b_cancel = Button(f_edit_data, text='Cancel', command=lambda: cancel('editing'))
            b_cancel.grid(row=4, column=2, padx=(2, 5), pady=(0, 5), sticky=W+E, columnspan=2)


            con.commit()
            con.close()
        except:
            f_edit_data = LabelFrame(editor, text='Edit Data')
            f_edit_data.grid(row=2, column=0, padx=5, columnspan=2, sticky=W+E)

            Label(f_edit_data, text='ID is invalid').pack()
    else:
        Label(editor, text='Re-enter').grid(row=2, column=0, columnspan=2)

def edit():
    global editor, edit_box
    editor = Tk()
    editor.title('Editor Window')
    editor.iconbitmap('office icon.ico')


    l_name_editor = Label(editor, text='ID no. :')
    l_name_editor.grid(row=0, column=0)

    edit_box = Entry(editor, width=12)
    edit_box.grid(row=0, column=1, ipadx=60, padx=5)

    b_edit_data = Button(editor, text='Edit Data', width=10, command=lambda: edit_data(edit_box.get()))
    b_edit_data.grid(row=1, column=0, columnspan=2, pady=5)

    Label(editor, text="PLEASE use '_' instead of 'SPACE'").grid(row=3, column=0, columnspan=4)

    editor.mainloop()

def add():
    global add_win, a_name_box, a_salary_box, a_post_box
    add_win = Tk()
    add_win.title('Add Window')
    add_win.iconbitmap('office icon.ico')


    a_name_l = Label(add_win, text='Name :')
    a_name_l.grid(row=0, column=0, pady=(5, 5))

    a_name_box = Entry(add_win, width=12)
    a_name_box.grid(row=0, column=1, padx=(2, 5), pady=(5, 5), columnspan=3, ipadx=60)

    a_post_l = Label(add_win, text='Post    :')
    a_post_l.grid(row=1, column=0, pady=(0, 5), sticky=W)

    a_post_box = Entry(add_win)
    a_post_box.grid(row=1, column=1, padx=(2, 5), pady=(0, 5), sticky=W + E, columnspan=3)

    a_salary_l = Label(add_win, text='Salary :')
    a_salary_l.grid(row=2, column=0, pady=(0, 5))

    a_salary_box = Entry(add_win)
    a_salary_box.grid(row=2, column=1, padx=(2, 5), pady=(0, 5), sticky=W + E, columnspan=3)

    b_save = Button(add_win, text='Save', command=lambda: save('adding'))
    b_save.grid(row=3, column=0, padx=(2, 5), pady=(0, 5), sticky=W + E, columnspan=2)

    b_cancel = Button(add_win, text='Cancel', command=lambda: cancel('adding'))
    b_cancel.grid(row=3, column=2, padx=(2, 5), pady=(0, 5), sticky=W + E, columnspan=2)

    add_win.mainloop()

def delete(id):
    global remove_win, id_box, temp
    if id != '':
        name = temp.get(int(id))[2]
        yn = messagebox.askquestion('Delete', 'Do you want to delete ID no. '+str(id)+' : '+name+'?')
        if yn == 'yes':
            con = sqlite3.connect('Attendance.db')
            c = con.cursor()
            g_every_data = c.execute('SELECT * FROM staff WHERE oid = %s;' % (id)).fetchall()
            var_name = g_every_data[0][0]

            c.execute("DELETE FROM staff WHERE oid=:id", {'id': id})
            c.execute("DROP TABLE %s" % (var_name))
            con.commit()
            con.close()

            temp.pop(int(id))
            remove_win.destroy()
            refresh()
    else:
        Label(remove_win, text='Re-enter').grid(row=2, column=0, columnspan=2)

def remove():
    global remove_win, id_box
    remove_win = Tk()
    remove_win.title('Remove Window')
    remove_win.iconbitmap('office icon.ico')


    l_name_remove = Label(remove_win, text='ID no.', width=8)
    l_name_remove.grid(row=0, column=0, sticky=W+E)

    id_box = Entry(remove_win, width=12)
    id_box.grid(row=0, column=1, columnspan=3, sticky=W+E, ipadx=60, padx=(0, 5))

    b_delete = Button(remove_win, text='Delete', command=lambda: delete(id_box.get()))
    b_delete.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky=W+E, columnspan=2)

    b_cancel = Button(remove_win, text='Cancel', command=lambda: cancel('removing'))
    b_cancel.grid(row=1, column=2, padx=(3, 5), pady=(5, 5), sticky=W+E, columnspan=2)

    remove_win.mainloop()

def verify():
    verify_ap_l = []
    name_ap_l = []
    verify_list = []

    for name in staff_name:
        c.execute("SELECT ap FROM %s WHERE date=:date LIMIT 1;" % (name), {'date': yesterday_date})
        try:
            verify_ap = c.fetchall()[0][0]
        except:
            verify_ap = 'none'

        verify_ap_l.append(verify_ap)

        name_ap_l.append(name)

    verify_list = list(zip(name_ap_l, verify_ap_l))
    print(verify_list)


    for name, ap in verify_list:
        if ap == 'none':
            p_yn = messagebox.askyesno('Attendance Missing', 'Was '+name+' PRESENT on '+yesterday_date+' ?')
            print(p_yn)
            if p_yn == True:
                c.execute('''INSERT INTO %s VALUES (:date, :d, :m, :y, :present) ''' % (name),
                          {'date': yesterday_date, 'd': yesterday_day, 'm': yesterday_month, 'y': yesterday_year, 'present': 'Present'})
            if p_yn == False:
                c.execute('''INSERT INTO %s VALUES (:date, :d, :m, :y, :absent) ''' % (name),
                          {'date': yesterday_date, 'd': yesterday_day, 'm': yesterday_month, 'y': yesterday_year, 'absent': 'Absent'})

def start():
    global b_p, b_add, b_all_p
    con = sqlite3.connect('Attendance.db')
    c = con.cursor()

    for var_row, id, name in staff_t_data:
        temp[id] = (var_row, id, name, 'none')
        sr = Label(f_l, text=id, width=5, anchor=W)
        sr.grid(row=int(var_row)-1, column=0, pady=(7, 0), sticky=W)

        l_name = Label(f_l, text=name, width=15, anchor=W)
        l_name.grid(row=int(var_row)-1, column=1, pady=(5, 0), sticky=W)

        b_p = Button(f_l, text='Present', command=lambda r=int(var_row), i=id, n=str(name): p(r, i, n))
        b_p.grid(row=int(int(var_row) - 1), column=2, pady=(5, 0), padx=(5, 0), sticky=W)

        b_a = Button(f_l, text='Absent', command=lambda r=int(var_row), i=id, n=str(name): a(r, i, n))
        b_a.grid(row=int(int(var_row) - 1), column=3, pady=(5, 5), padx=(5, 0), sticky=W)

    temp[444] = (row_no[-1], 444, 'All Present', 'none')

    b_all_p = Button(f_l, text='All Present', command=all_p)
    b_all_p.grid(row=int(int(row_no[-1])), column=0, columnspan=4, pady=(5, 0))

    con.commit()
    con.close()


b_cal_salary = Button(f_r, text='Cal Salary', command=sal, width=10)
b_cal_salary.grid(row=0, column=5, padx=10, pady=(5, 0))

b_edit = Button(f_r, text='Edit', width=10, command=edit)
b_edit.grid(row=1, column=5, padx=10, pady=(5, 0))

b_add = Button(f_r, text='Add', width=10, command=add)
b_add.grid(row=2, column=5, padx=10, pady=(5, 0))

b_sub = Button(f_r, text='Remove', width=10, command=remove)
b_sub.grid(row=3, column=5, padx=10, pady=(5, 0))

b_refresh = Button(f_r, text='Refresh', width=10, command=refresh)
b_refresh.grid(row=4, column=5, padx=10, pady=(5, 5))


if yesterday_date == str(date):
            cre_list()
            cre_table()
            today_temp()
            if n_c > 1:
                messagebox.showinfo('About Attendance', "In today"+"'s attendance "+str(n_c)+" are remaining.")
            elif n_c == 1:
                messagebox.showinfo('About Attendance', "In today"+"'s attendance "+str(n_c)+" is remaining.")
            else:
                messagebox.showinfo('About Attendance', "Today"+"'s attendance is already taken.")

            refresh()

if yesterday_date != str(date):

            c.execute("INSERT INTO date_t VALUES (:date, :d, :m, :y)", {'date': date, 'd': day, 'm': month, 'y': year})

            cre_list()
            cre_table()
            start()
            verify()

con.commit()
con.close()

root.mainloop()