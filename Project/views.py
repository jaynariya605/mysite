from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from Project.forms import DataForm
import pandas as pd
import sklearn.externals 
import joblib
from Project.models import approvals
from django.forms import model_to_dict

# Create your views here.


def username_present(username):
	if username.is_admin:
		if approvals.objects.filter().exists():
			return True
	else:
		if approvals.objects.filter(user=username).exists():
			return True

    
	return False



def Data(username):
	if username.is_admin:
		obj = approvals.objects.all()
	else:
		obj = approvals.objects.filter(user=username)
	return obj





def ohevalue(df):
	ohe_col =['CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
       'FLAG_MOBIL', 'FLAG_WORK_PHONE', 'FLAG_PHONE', 'FLAG_EMAIL',
       'CNT_FAM_MEMBERS', 'CODE_GENDER_F', 'CODE_GENDER_M',
       'FLAG_OWN_CAR_N', 'FLAG_OWN_CAR_Y', 'FLAG_OWN_REALTY_N',
       'FLAG_OWN_REALTY_Y', 'NAME_INCOME_TYPE_Commercial associate',
       'NAME_INCOME_TYPE_Pensioner', 'NAME_INCOME_TYPE_State servant',
       'NAME_INCOME_TYPE_Student', 'NAME_INCOME_TYPE_Working',
       'NAME_EDUCATION_TYPE_Academic degree',
       'NAME_EDUCATION_TYPE_Higher education',
       'NAME_EDUCATION_TYPE_Incomplete higher',
       'NAME_EDUCATION_TYPE_Lower secondary',
       'NAME_EDUCATION_TYPE_Secondary / secondary special',
       'NAME_FAMILY_STATUS_Civil marriage', 'NAME_FAMILY_STATUS_Married',
       'NAME_FAMILY_STATUS_Separated',
       'NAME_FAMILY_STATUS_Single / not married', 'NAME_FAMILY_STATUS_Widow',
       'NAME_HOUSING_TYPE_Co-op apartment',
       'NAME_HOUSING_TYPE_House / apartment',
       'NAME_HOUSING_TYPE_Municipal apartment',
       'NAME_HOUSING_TYPE_Office apartment',
       'NAME_HOUSING_TYPE_Rented apartment', 'NAME_HOUSING_TYPE_With parents',
       'OCCUPATION_TYPE_Accountants', 'OCCUPATION_TYPE_Cleaning staff',
       'OCCUPATION_TYPE_Cooking staff', 'OCCUPATION_TYPE_Core staff',
       'OCCUPATION_TYPE_Drivers', 'OCCUPATION_TYPE_HR staff',
       'OCCUPATION_TYPE_High skill tech staff', 'OCCUPATION_TYPE_IT staff',
       'OCCUPATION_TYPE_Laborers', 'OCCUPATION_TYPE_Low-skill Laborers',
       'OCCUPATION_TYPE_Managers', 'OCCUPATION_TYPE_Medicine staff',
       'OCCUPATION_TYPE_Private service staff',
       'OCCUPATION_TYPE_Realty agents', 'OCCUPATION_TYPE_Sales staff',
       'OCCUPATION_TYPE_Secretaries', 'OCCUPATION_TYPE_Security staff',
       'OCCUPATION_TYPE_Unknown', 'OCCUPATION_TYPE_Waiters/barmen staff']
	df_processed = pd.get_dummies(df, columns=['CODE_GENDER','FLAG_OWN_CAR','FLAG_OWN_REALTY','NAME_INCOME_TYPE','NAME_EDUCATION_TYPE','NAME_FAMILY_STATUS','NAME_HOUSING_TYPE','OCCUPATION_TYPE'], drop_first = False)
	new_dict={}

	for i in ohe_col:
		if i in df_processed.columns:
			new_dict[i]=df_processed[i].values
		else:
			new_dict[i]=6

	newdf=pd.DataFrame(new_dict)
	return newdf




def Application(request, df, ID):
	
	model = joblib.load("Model.pkl")
	x=df
	y_pred = model.predict(x)
	

	obj = approvals.objects.get(id= ID)
	if(y_pred==0):
		obj.Result ="0"
		obj.save()
		
	elif(y_pred==1):
		obj.Result ="1"
		obj.save()
		
		return('1')
	else:
		print('Error')



def train(x,y):
	model = joblib.load("Model.pkl")
	model.partial_fit(x,y, classes=None)
	joblib.dump(model,'Model.pkl')
	return True




def edit_view(request):
	
	if request.POST and 'Edit_ID' in request.POST:
		Edit_ID = request.POST.get('Edit_ID')
		obj = approvals.objects.get(id=Edit_ID)

		if request.user.is_admin or request.user == obj.user:
			edit_form = DataForm(
				initial=  {
						"CNT_CHILDREN": obj.CNT_CHILDREN,
						"AMT_INCOME_TOTAL": obj.AMT_INCOME_TOTAL,
						"DAYS_BIRTH": obj.DAYS_BIRTH,
						"DAYS_EMPLOYED": obj.DAYS_EMPLOYED,
						"FLAG_MOBIL": obj.FLAG_MOBIL,
						"FLAG_WORK_PHONE": obj.FLAG_WORK_PHONE,
						"FLAG_PHONE": obj.FLAG_PHONE,
						"FLAG_EMAIL": obj.FLAG_EMAIL,
						"CNT_FAM_MEMBERS": obj.CNT_FAM_MEMBERS,
						"CODE_GENDER": obj.CODE_GENDER,
						"FLAG_OWN_CAR": obj.FLAG_OWN_CAR,
						"FLAG_OWN_REALTY": obj.FLAG_OWN_REALTY,
						"NAME_INCOME_TYPE": obj.NAME_INCOME_TYPE,
						"NAME_EDUCATION_TYPE": obj.NAME_EDUCATION_TYPE,
						"NAME_FAMILY_STATUS": obj.NAME_FAMILY_STATUS,
						"NAME_HOUSING_TYPE": obj.NAME_HOUSING_TYPE,
						"OCCUPATION_TYPE": obj.OCCUPATION_TYPE,

					}
				)

			return edit_form



	if request.POST and 'SAVE_ID' in request.POST:
		SAVE_ID = request.POST.get('SAVE_ID')
		obj = approvals.objects.get(id=SAVE_ID)
		if request.user.is_admin or request.user == obj.user:
			save_form = DataForm(request.POST, instance= obj)
			if save_form.is_valid():
				return save_form


		


def feedback(Feedback_ID, Feedback):
	obj = approvals.objects.get(id = Feedback_ID)
	obj.Feedback = Feedback
	obj.save()
	return obj









def ML_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
	context  = {}





	if username_present(request.user)==True:
		if request.POST and 'ID' in request.POST :
			ID = request.POST.get('ID')
			obj = Data(request.user)
			D = obj.get(id=ID)
			D.delete()
			return redirect('dashboard')



		if request.POST and 'Edit_ID' in request.POST :
			
			context['edit_form'] = edit_view(request)
			context['edit_ID'] = request.POST.get('Edit_ID')
			return render(request, 'Project/edit.html', context)


		if request.POST and 'SAVE_ID' in request.POST :

			save_form = edit_view(request)
			save_form.save()
			myDict =(request.POST).dict()
			df = pd.DataFrame(myDict, index=[0])

			df = df.iloc[: , 1:]
			df = df.drop(labels='SAVE_ID', axis=1)
			
			df ['DAYS_BIRTH'] = (pd.to_datetime(df.DAYS_BIRTH)-pd.to_datetime("now")).dt.days
			df ['DAYS_EMPLOYED'] = (pd.to_datetime(df.DAYS_EMPLOYED)-pd.to_datetime("now")).dt.days
			df2 = ohevalue(df)
			
			Application(request, df2, request.POST.get('SAVE_ID'))
			return redirect('dashboard')


		if (request.POST and 'Feedback' in request.POST) and (request.POST and 'feedback_id' in request.POST):


			Feedback = request.POST.get('Feedback')
			Feedback_ID = request.POST.get('feedback_id')
			obj = feedback(Feedback_ID, Feedback)
			df = model_to_dict(obj)
			df = pd.DataFrame(df, index=[0])
			df = df.iloc[: , 2:]
			df = df.drop(labels='Result', axis=1)
			df = df.reset_index(drop=True)
			df ['DAYS_BIRTH'] = (pd.to_datetime(df.DAYS_BIRTH)-pd.to_datetime("now")).dt.days
			df ['DAYS_EMPLOYED'] = (pd.to_datetime(df.DAYS_EMPLOYED)-pd.to_datetime("now")).dt.days
			df2 = ohevalue(df.iloc[: , :17])
			Y = df['Feedback']
			print(Y)
			train(df2,Y)
			


			


			



		
		obj = Data(request.user)
		context['user_data'] = obj
		

		return render(request, 'Project/history.html', context)




	elif username_present(request.user)==False:



		if request.POST:
			form = DataForm(request.POST)
			if form.is_valid():
				approvals = form.save(commit=False)
				approvals.user = request.user
				approvals.save()
				EID = approvals.id
				CNT_CHILDREN = form.cleaned_data['CNT_CHILDREN']
				AMT_INCOME_TOTAL = form.cleaned_data['AMT_INCOME_TOTAL']
				DAYS_BIRTH = form.cleaned_data['DAYS_BIRTH']
				DAYS_EMPLOYED = form.cleaned_data['DAYS_EMPLOYED']
				FLAG_MOBIL = form.cleaned_data['FLAG_MOBIL']
				FLAG_WORK_PHONE = form.cleaned_data['FLAG_WORK_PHONE']
				FLAG_PHONE = form.cleaned_data['FLAG_PHONE']
				FLAG_EMAIL = form.cleaned_data['FLAG_EMAIL']
				CNT_FAM_MEMBERS = form.cleaned_data['CNT_FAM_MEMBERS']
				CODE_GENDER = form.cleaned_data['CODE_GENDER']
				FLAG_OWN_CAR = form.cleaned_data['FLAG_OWN_CAR']
				FLAG_OWN_REALTY = form.cleaned_data['FLAG_OWN_REALTY']
				NAME_INCOME_TYPE = form.cleaned_data['NAME_INCOME_TYPE']
				NAME_EDUCATION_TYPE = form.cleaned_data['NAME_EDUCATION_TYPE']
				NAME_FAMILY_STATUS = form.cleaned_data['NAME_FAMILY_STATUS']
				NAME_HOUSING_TYPE = form.cleaned_data['NAME_HOUSING_TYPE']
				OCCUPATION_TYPE = form.cleaned_data['OCCUPATION_TYPE']

				myDict =(request.POST).dict()
				df = pd.DataFrame(myDict, index=[0])
				df = df.iloc[: , 1:]
				df ['DAYS_BIRTH'] = (pd.to_datetime(df.DAYS_BIRTH)-pd.to_datetime("now")).dt.days
				df ['DAYS_EMPLOYED'] = (pd.to_datetime(df.DAYS_EMPLOYED)-pd.to_datetime("now")).dt.days
				df2 = ohevalue(df)
				
				Application(request, df2, EID)

				
				
				return redirect('dashboard')

			else:
				
				context['Data_form'] = form

			

		else:
			form = DataForm()
			context['Data_form'] = form

		return render(request, 'Project/ml.html', context)