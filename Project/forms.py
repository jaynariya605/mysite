from django import forms
from Project.models import approvals

class DataForm(forms.ModelForm):
	

	class Meta:
		model = approvals
		fields = '__all__'
		exclude =["user","date_modified", "date_published","Result"]