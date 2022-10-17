from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()

            user = authenticate(request, username = user.username, password =request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form' : form, 'page' : page}
    return render(request, 'photos/login_register.html', context)

@login_required(login_url='login')

def gallery(request):
    user = request.user
    # photo_title = request.GET.get('photo_title')
    if 'q' in request.GET:
        q = request.GET['q']
        photos = Photo.objects.filter(photo_title__icontains=q)

    # photos = Photo.objects.all()
        context = {
           'photos': photos
        }
        return render(request, 'photos/search.html', context)
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required(login_url='login')

def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
                

        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                photo_title=data['photo_title'],
                image=image
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

def deleteItem(request, id):

    pho = Photo.objects.get(id=id)
    pho.delete()
    return redirect('gallery')



#Every time you call the phone and laptop camera method gets frame
#More info found in camera.py
# def gen(camera):
# 	while True:
# 		frame = camera.get_frame()
# 		yield (b'--frame\r\n'
# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# #Method for laptop camera
# def video_feed(request):
# 	return StreamingHttpResponse(gen(VideoCamera()),
#                     #video type
# 					content_type='multipart/x-mixed-replace; boundary=frame')

# #Method for phone camera
# def webcam_feed(request):
# 	return StreamingHttpResponse(gen(IPWebCam()),
#                     #video type
# 					content_type='multipart/x-mixed-replace; boundary=frame')