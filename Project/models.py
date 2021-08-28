from django.db import models
from django.conf import settings
# Create your models here.


class approvals(models.Model):

	CODE_GENDER = (
		('M', 'Male'),
		('F', 'Female')
	)

	MOBILE_CHOICES = (
		('1', 'Yes'),
		('0' , 'No')
	)

	WORKPHONE_CHOICES = (
		('1', 'Yes'),
		('0' , 'No')
	)

	PHONE_CHOICES = (
		('1', 'Yes'),
		('0' , 'No')
	)


	EMAIL_CHOICES = (
		('1', 'Yes'),
		('0' , 'No')
	)


	CAR_CHOICES = (
		('Y', 'Yes'),
		('N' , 'No')
	)


	PROPERTIES_CHOICES = (
		('Y', 'Yes'),
		('N' , 'No')
	)

	INCOME_CHOICES = (
		('Commercial associate' , 'Commercial associate'),
		('Pensioner' , 'Pensioner'),
		('State servant', 'State servant'),
		('Student', 'Student'),
		('Working' , 'Working')
		)

	EDUCATION_CHOICES = (
		('Academic degree', 'Academic degree'),
		('Higher education', 'Higher education'),
		('Incomplete higher', 'Incomplete higher'),
		('Lower secondary','Lower secondary'),
		('Secondary / secondary special','Secondary / secondary special')
	)


	STATUS_CHOICES = (
		('Civil marriage', 'Civil marriage'),
		('Married', 'Married'),
		('Separated', 'Separated'),
		('Single / not married' , 'Single / not married'),
		('Widow','Widow')
	)

	HOUSE_CHOICES = (
		('Co-op apartment','Co-op apartment'),
		('House / apartment', 'House / apartment'),
		('Municipal apartment', 'Municipal apartment'),
		('Office apartment', 'Office apartment'),
		('Rented apartment', 'Rented apartment'),
		('With parents','With parents')
	)


	OCCUPATION_CHIOCES = (
		('Accountants','Accountants'),
		('Cleaning staff','Cleaning staff'),
		('Cooking staff ','Cooking staff '),
		('Core staff','Core staff'),
		('Drivers','Drivers'),
		('HR staff','HR staff'),
		('High skill tech staff','High skill tech staff'),
		('IT staff','IT staff'),
		('Laborers', 'Laborers'),
		('Low-skill Laborers','Low-skill Laborers'),
		('Managers','Managers'),
		('Medicine staff','Medicine staff'),
		('Private service staff','Private service staff'),
		('Realty agents','Realty agents'),
		('Sales staff','Sales staff'),
		('Secretaries','Secretaries'),
		('Security staff','Security staff'),
		('Waiters/barmen staff','Waiters/barmen staff'),
		('Unknown','Unknown')
		)

	RESULT_CHOICES = (
		('0', 'Approved'),
		('1' , 'Rejected')
	)



	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	date_modified = models.DateField(verbose_name='last modified',auto_now=True)
	date_published = models.DateField(verbose_name='date joined',auto_now_add=True)
	CNT_CHILDREN = models.IntegerField()
	AMT_INCOME_TOTAL = models.IntegerField()
	DAYS_BIRTH = models.DateField()
	DAYS_EMPLOYED = models.DateField()
	FLAG_MOBIL = models.CharField(max_length=115, choices=MOBILE_CHOICES)
	FLAG_WORK_PHONE = models.CharField(max_length=115, choices=WORKPHONE_CHOICES)
	FLAG_PHONE = models.CharField(max_length=115,choices=PHONE_CHOICES)
	FLAG_EMAIL = models.CharField(max_length=115, choices=EMAIL_CHOICES)
	CNT_FAM_MEMBERS = models.IntegerField()
	CODE_GENDER = models.CharField(max_length=115, choices=CODE_GENDER)
	FLAG_OWN_CAR = models.CharField(max_length=115, choices=CAR_CHOICES)
	FLAG_OWN_REALTY = models.CharField(max_length=115 ,choices=PROPERTIES_CHOICES)
	NAME_INCOME_TYPE = models.CharField(max_length=115 , choices=INCOME_CHOICES)
	NAME_EDUCATION_TYPE = models.CharField(max_length=115 , choices=EDUCATION_CHOICES)
	NAME_FAMILY_STATUS = models.CharField(max_length=115, choices=STATUS_CHOICES)
	NAME_HOUSING_TYPE = models.CharField(max_length=115, choices=HOUSE_CHOICES)
	OCCUPATION_TYPE = models.CharField(max_length=115, choices=OCCUPATION_CHIOCES)
	Result = models.CharField(max_length=115, choices=RESULT_CHOICES)
	Feedback = models.CharField(max_length=115,blank= True, choices=RESULT_CHOICES)


