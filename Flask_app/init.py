import pandas as pd
from flask import Flask , render_template,request


app = Flask(__name__)



@app.route("/") 
def index():
    return render_template("start.html")


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



        return render_template('/index.html', data=data , st_name=stu_name , classes=classes,M_staff=M_staff ,M_staff_all=M_staff,Names=Names,who="Student",to="Staff")
    

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

        return render_template('/input.html',Names=Names,who="Student",result_dict=data)
    



@app.route('/Staff', methods=['GET', 'POST'])
def Staff_pie_chart():
    chart_data=pd.read_csv("./Overall_staff_Attendance.csv")
    all_staff_name=list(chart_data.columns.values)

    if request.method == 'POST':
        staff_name = request.form['name']
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
        

    


        return render_template('/index.html', data=data , st_name=staff_name , classes=classes,M_staff=M_staff ,Names=all_staff_name,M_staff_all=M_staff_all,who="Staff",to="Student")
    
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

            df = pd.DataFrame(list(zip(all_staff_name, classes,Auto,Manual,percentage)),columns =['Name', 'classes',"Auto","Manual","Auto_percentage"])
            df['Auto_percentage'] = pd.to_numeric(df['Auto_percentage'].str.rstrip('%'))
            data = df.sort_values(by='Auto_percentage')
            data['Auto_percentage'] = data['Auto_percentage'].astype(str) + '%'
            data = data.to_dict('list')

        return render_template('/input.html',Names=all_staff_name,who="Staff",result_dict=data)



 



if __name__ == "__main__":
    app.run(debug=True)
