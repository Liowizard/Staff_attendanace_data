import pandas as pd
from flask import Flask , render_template,request


app = Flask(__name__)


All_Session_Data = pd.read_csv('./All_Session_Data.csv')
All_Session_Data= All_Session_Data.drop(All_Session_Data.columns[0], axis=1)
Session_Data_columns = All_Session_Data.columns


@app.route("/", methods=['GET', 'POST']) 
def index():

    infra_names = All_Session_Data["infra_name"].values.tolist()
    infra_names=set(infra_names)
    infra_names=list(infra_names)
    if request.method == 'POST':
        date_input = request.form['date']
        infra = request.form['name']
        date_input=str(date_input)
        if infra =="":
             ses_data=All_Session_Data[All_Session_Data['Session_Date'] == date_input]
        else:
            ses_data=All_Session_Data[(All_Session_Data['Session_Date'] == date_input) & (All_Session_Data['infra_name'] ==infra)]
        auto_p_sum = ses_data['auto present'].sum()
        manual_p_sum = ses_data['manual present '].sum()
        number_of_sessions=(ses_data.shape)[0]
        print(date_input,infra)
        return  render_template("session_table.html",table=ses_data , date=date_input,
                                infra=infra,manual_p_sum=manual_p_sum,auto_p_sum=auto_p_sum,
                                number_of_sessions=number_of_sessions)
    
    return render_template("start.html",infra_names=infra_names)







@app.route('/student', methods=['GET', 'POST'])
def Student_pie_chart():
    chart_data=pd.read_csv("./Overall_student_Attendance.csv")
    Names = chart_data['Name'].values.flatten().tolist()
    
    if request.method == 'POST':
        # name="MOHAMMED A HAWAIT"
        stu_name = request.form['name']
        Stu_data=chart_data.loc[chart_data['Name'] ==stu_name ]
        pie_value=(Stu_data.iloc[0]['pie_data'])
        pie_value=pie_value[1:-1]
        pie_value=pie_value.split(",")
        data = {'Task' : 'Attendance Mode', 'Auto' : int(pie_value[0]), 'Manual' : int(pie_value[1])}


        classes=(Stu_data.iloc[0]['classes'])



        M_S=(Stu_data.iloc[0]['M_staff'])
        # A_S=chart_data["A_staff"]
        M_S=M_S[1:-1]
        M_S=M_S.split(",")
        M_staff={}
        M_names = set(M_S)
        for name in M_names:
            count = M_S.count(name)
            M_staff.update({name.capitalize() : str(count)})
        M_staff=dict(sorted(M_staff.items(), key=lambda x: x[1], reverse=True))



        return render_template('/index.html', data=data , st_name=stu_name , 
                               classes=classes,M_staff=M_staff ,M_staff_all=M_staff,
                               Names=Names,who="student",to="Staff")
    

    else:
        pie_data = chart_data['pie_data'].tolist()
        per=chart_data['per'].tolist()
        Auto=[]
        Manual=[]
        percentage=[]

        for i in pie_data:
            i=i[1:-1]
            i=i.split(",")
            Auto.append(int(i[0]))
            Manual.append(int(i[1]))

        for pers in per:
            pers=str(round(pers, 1))+"%"
            percentage.append(pers)

        data=chart_data[["Name","classes"]].assign(Auto=Auto,Manual=Manual,Auto_percentage=percentage)
        data = data.to_dict('list')

        return render_template('/input.html',Names=Names,who="student",result_dict=data)
    



@app.route('/Staff', methods=['GET', 'POST'])
def Staff_pie_chart():
    chart_data=pd.read_csv("./Overall_staff_Attendance.csv")
    all_staff_name=list(chart_data.columns.values)

    if request.method == 'POST':
        staff_name = request.form['name']
        Session_Data=All_Session_Data.loc[All_Session_Data['Primary_staff'] ==staff_name]
        staff_data = chart_data[['all_student', staff_name]]
        pie=staff_data[staff_name][1]
        pie_value=pie[1:-1]
        pie_value=pie_value.split(",")
        data = {'Task' : 'Attendance Mode', 'Auto' : int(pie_value[0]), 'Manual' : int(pie_value[1])}

        classes=int(staff_data[staff_name][0])  

        M_staff_all={}
        nor=["classes","Staff_pie"]
        for no ,session in staff_data.iterrows():
            if session["all_student"] not in nor:
                m=session[staff_name]
                pie_value=m[1:-1]
                pie_value=pie_value.split(",")
                pie_value=pie_value[1]
                names=session["all_student"]
                M_staff_all.update({names.capitalize() : int(pie_value)})
                
        M_staff_all = {k: v for k, v in M_staff_all.items() if v != 0} 
        M_staff_all=dict(sorted(M_staff_all.items(), key=lambda x: x[1], reverse=True))
        M_staff = dict(sorted(M_staff_all.items(), key=lambda x: x[1], reverse=True)[:20])
        


        return render_template('/index.html', data=data , st_name=staff_name , classes=classes,
                               M_staff=M_staff ,Names=all_staff_name,All_Session_Data=Session_Data,
                               M_staff_all=M_staff_all,Session_Data_columns=Session_Data_columns,
                               who="Staff",to="Student")
    
    else:


        all_staff_name=list(chart_data.columns.values)
        classes = chart_data.iloc[0].tolist()
        pie=chart_data.iloc[1].tolist()

        del all_staff_name[0:2]
        del classes[0:2]
        del pie[0:2]

        Auto=[]
        Manual=[]
        percentage=[]

        for i in pie:
            i=i[1:-1]
            i=i.split(",")
            Auto.append(int(i[0]))
            Manual.append(int(i[1]))
            per=int(i[0])+int(i[1])
            per=int(i[0])/per
            per=per*100
            per=str(round(per, 1))+"%"
            percentage.append(per)

            df = pd.DataFrame(list(zip(all_staff_name, classes,Auto,Manual,percentage)),
                              columns =['Name', 'classes',"Auto","Manual","Auto_percentage"])
            df['Auto_percentage'] = pd.to_numeric(df['Auto_percentage'].str.rstrip('%'))
            data = df.sort_values(by='Auto_percentage')
            data['Auto_percentage'] = data['Auto_percentage'].astype(str) + '%'
            data = data.to_dict('list')

        return render_template('/input.html',Names=all_staff_name,who="Staff",result_dict=data)



 



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
