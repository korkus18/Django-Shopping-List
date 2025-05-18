from django.db import models
from django.contrib.auth.models import User

class ItemsList(models.Model):
	CATEGORY_CHOICES = [
		('dairy', 'Mléčné výrobky'),
		('vegetables', 'Ovoce a zelenina'),
		('frozen', 'Mražené potraviny'),
		('meal', 'Hotová jídla'),
		('bread', 'Pečivo'),
		('other', 'Ostatní')
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	itemname = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='items_images/', blank=True, null=True)
	completed = models.BooleanField(default=False)
	date_added = models.DateTimeField(auto_now_add=True)
	category = models.CharField(
		max_length=20,
		choices=CATEGORY_CHOICES,
		default='other'
	)

	def __str__(self):
		return self.itemname

	class Meta:
		ordering = ['-date_added']

