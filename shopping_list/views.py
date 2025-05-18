from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import *
import json
import logging

logger = logging.getLogger(__name__)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Registration successful!')
			return redirect('index')
	else:
		form = UserCreationForm()
	return render(request, 'registration/register.html', {'form': form})

@login_required
def index(request):
	# Get all items and group them by category
	all_items = ItemsList.objects.filter(user=request.user)
	items_by_category = {
		'dairy': all_items.filter(category='dairy'),
		'vegetables': all_items.filter(category='vegetables'),
		'frozen': all_items.filter(category='frozen'),
		'meal': all_items.filter(category='meal'),
		'bread': all_items.filter(category='bread'),
		'other': all_items.filter(category='other')
	}
	
	# Remove empty categories
	items_by_category = {k: v for k, v in items_by_category.items() if v.exists()}
	
	category_names = {
		'dairy': 'Mléčné výrobky',
		'vegetables': 'Ovoce a zelenina',
		'frozen': 'Mražené potraviny',
		'meal': 'Hotová jídla',
		'bread': 'Pečivo',
		'other': 'Ostatní'
	}
	
	return render(request, "shopping_list/index.html", {
		"items_by_category": items_by_category,
		"category_names": category_names,
		"items_saved": all_items.exists()
	})

@login_required
def addItem(request):
	if request.method == 'POST':
		item_name = request.POST.get('item', '').strip()
		category = request.POST.get('category', 'other')
		
		if not item_name:
			if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
				return JsonResponse({
					'success': False,
					'error': 'Item name is required'
				}, status=400)
			messages.error(request, 'Item name is required')
			return redirect('index')

		try:
			# Create new item
			new_item = ItemsList(
				itemname=item_name,
				user=request.user,
				category=category
			)
			
			# Handle image if provided
			if 'image' in request.FILES:
				new_item.image = request.FILES['image']
			
			# Save the item
			new_item.save()
			
			if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
				return JsonResponse({
					'success': True,
					'item': {
						'id': new_item.id,
						'itemname': new_item.itemname,
						'category': new_item.category,
						'image_url': new_item.image.url if new_item.image else None,
						'date_added': new_item.date_added.strftime('%B %d, %Y, %I:%M %p'),
						'completed': new_item.completed
					}
				})
			
			messages.success(request, 'Item added successfully!')
			return redirect('index')
			
		except Exception as e:
			logger.error(f"Error adding item: {str(e)}")
			if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
				return JsonResponse({
					'success': False,
					'error': 'Failed to add item'
				}, status=500)
			messages.error(request, 'Failed to add item')
			return redirect('index')
			
	return redirect('index')

@login_required
def item_detail(request, item_id):
	item = get_object_or_404(ItemsList, id=item_id, user=request.user)
	return render(request, 'shopping_list/item_detail.html', {'item': item})

@login_required
def edit_item(request, item_id):
	"""
	View for handling item editing
	"""
	try:
		item = get_object_or_404(ItemsList, id=item_id, user=request.user)
	except:
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			return JsonResponse({
				'success': False,
				'error': 'Item not found'
			}, status=404)
		messages.error(request, 'Item not found')
		return redirect('index')

	if request.method == 'POST':
		try:
			# Get and validate form data
			itemname = request.POST.get('itemname', '').strip()
			category = request.POST.get('category', 'other')
			completed = request.POST.get('completed') == 'true'

			if not itemname:
				return JsonResponse({
					'success': False,
					'error': 'Item name is required'
				}, status=400)

			# Update fields
			item.itemname = itemname
			item.category = category
			item.completed = completed

			# Handle image
			if 'image' in request.FILES:
				try:
					# Delete old image if exists
					if item.image:
						item.image.delete(save=False)
					item.image = request.FILES['image']
				except Exception as e:
					logger.error(f"Image upload error: {str(e)}")
					return JsonResponse({
						'success': False,
						'error': 'Failed to upload image'
					}, status=400)

			# Save the item
			item.save()

			# Prepare response data
			response_data = {
				'success': True,
				'item': {
					'id': item.id,
					'itemname': item.itemname,
					'category': item.category,
					'image_url': item.image.url if item.image else None,
					'date_added': item.date_added.strftime('%B %d, %Y, %I:%M %p'),
					'completed': item.completed
				}
			}

			return JsonResponse(response_data)

		except Exception as e:
			logger.error(f"Error updating item: {str(e)}")
			return JsonResponse({
				'success': False,
				'error': 'An error occurred while updating the item'
			}, status=500)

	# GET request
	if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
		return JsonResponse({
			'success': True,
			'item': {
				'id': item.id,
				'itemname': item.itemname,
				'category': item.category,
				'image_url': item.image.url if item.image else None,
				'date_added': item.date_added.strftime('%B %d, %Y, %I:%M %p'),
				'completed': item.completed
			}
		})

	return render(request, 'shopping_list/edit_item.html', {'item': item})

@login_required
def completeItem(request, item_id):
	try:
		item = ItemsList.objects.get(id=item_id)
		if item.user == request.user:
			item.completed = True
			item.save()
			messages.success(request, 'Item marked as completed!')
	except ItemsList.DoesNotExist:
		messages.error(request, 'Item not found!')
	return redirect('index')

@login_required
def deleteItem(request, item_id):
	try:
		item = ItemsList.objects.get(id=item_id)
		if item.user == request.user:
			if item.image:
				item.image.delete()
			item.delete()
			messages.success(request, 'Item deleted successfully!')
	except ItemsList.DoesNotExist:
		messages.error(request, 'Item not found!')
	return redirect('index')

@login_required
def deleteAll(request):
	items = ItemsList.objects.filter(user=request.user)
	for item in items:
		if item.image:
			item.image.delete()
	items.delete()
	messages.success(request, 'All items deleted successfully!')
	return redirect('index')