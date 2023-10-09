from import_export import resources
from django.contrib.auth.models import User

class PersonResource(resources.ModelResource):
	class meta:
		model = User