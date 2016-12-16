from django import forms
from django.core.validators import URLValidator

from .validators import validate_email

class SubmitedURLForm(forms.Form):

	url = forms.CharField(label="Submit URL", validators=[validate_email])

	# def clean_url(self):
	# 	url = self.clean_data['url']
	# 	print(url)
	# 	url_validator = URLValidator()
	# 	try:
	# 		url_validator(url)
	# 	except:
	# 		raise forms.ValidationError("Invalid URL for this field")
	# 	return url