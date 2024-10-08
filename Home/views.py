from xml.dom import NotFoundErr


try:
    from base64 import urlsafe_b64encode
    from lib2to3.pgen2.tokenize import generate_tokens
    from click import get_current_context
    from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
    from django.shortcuts import redirect, render
    from django.contrib.auth.models import User

    from .forms import CommentForm
    from .models import Comment, Contact, Video
    from django.contrib import messages
    from django.contrib.auth import authenticate, login, logout
    from django.core.mail import send_mail, EmailMessage
    from my_site import settings
    from django.contrib.sites.shortcuts import get_current_site
    from django.template.loader import render_to_string
    from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
    from django.utils.encoding import force_bytes, force_str
    from .tokens import generate_token


    def indexx(request):
        # user = request.user.get_full_name() #Full name of the user
        allvideos = Video.objects.all()
        allvid = allvideos[:3]
        return render(request, "Home/index.html", {"allvid": allvid})


    def is_ajax(request):
        return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


    def video(request, myid):

        video = Video.objects.filter(id=myid)
        allvideos = Video.objects.all()
        comments = Comment.objects.filter(post=video[0], reply=None).order_by("-id")

        if request.method == "POST":
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = request.POST["content"]
                reply_id = request.POST.get("comment_id")
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(
                    post=video[0], user=request.user, content=content, reply=comment_qs
                )
                comment.save()

                # return HttpResponseRedirect(request.path_info)

        else:
            comment_form = CommentForm

        if is_ajax(request=request):
            html = render_to_string(
                "Home/comments.html",
                {
                    "video": video[0],
                    "allvideos": allvideos,
                    "comments": comments,
                    "comment_form": comment_form,
                },
                request=request,
            )
            return JsonResponse({"form": html})

        return render(
            request,
            "Home/video.html",
            {
                "video": video[0],
                "allvideos": allvideos,
                "comments": comments,
                "comment_form": comment_form,
            },
        )


    def contact(request):
        thank = False
        if request.method == "POST":
            name = request.POST.get("name", "")
            email = request.POST.get("email", "")
            phone = request.POST.get("phone", "")
            msg = request.POST.get("msg", "")
            contact = Contact(name=name, email=email, phone=phone, msg=msg)
            contact.save()
            thank = True
        return render(request, "Home/contact.html", {"thank": thank})


    def signup(request):
        if request.method == "POST":
            username = request.POST["username"]
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            email = request.POST["email"]
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]

            if User.objects.filter(username=username):
                messages.error(
                    request, "username already exist! Please try another username"
                )
                return redirect("signup")
            if User.objects.filter(email=email):
                messages.error(request, "Email already registered!")
                return redirect("signup")
            if len(pass1) < 8:
                messages.error(request, "Please enter a password of atleast 8 digits!")
                return redirect("signup")
            if pass1 != pass2:
                messages.error(
                    request, "Check if both the feilds of password are entered correctly!"
                )
                return redirect("signup")

            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            messages.success(
                request,
                "Your Account Has Been Successfully Created. We have send you a confiration email, please confirm you email in order to activate your account...",
            )
            # Sending Email
            subject = "Welcome to Cyber Programmer - cyberprogrammmer.com"
            message = (
                "Hello "
                + myuser.first_name
                + "!! \n"
                + "Welcome to Cyber Programmer!! \n\nThank you for visiting our website \nWe have also sent you a confirmation email please confirm your email-address in order to activate your accout \n\nIf you are new to our website and don't know about our channel then please subscribe our channel by clicking on the link given below: \n"
                + "https://www.youtube.com/c/CyberProgrammer"
                + "\n\nThank You,\n"
                + myuser.first_name
            )
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Confirmation of Email

            current_site = get_current_site(request)
            email_subject = "Confirm Your Email Address @ cyberprogrammer.com"
            message2 = render_to_string(
                "email_confirmation.html",
                {
                    "name": myuser.first_name,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                    "token": generate_token.make_token(myuser),
                },
            )
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            return redirect("login")
        return render(request, "Home/signup.html", {})


    def login_user(request):
        if request.method == "POST":
            username = request.POST["username"]
            pass1 = request.POST["pass1"]

            user = authenticate(username=username, password=pass1)
            if user is not None:
                login(request, user)
                fname = user.first_name
                messages.success(request, "Logged-In Successfully!")
                return redirect("home")
            else:
                messages.error(request, "Wrong Credentials!")
                return redirect("login")

        return render(request, "Home/login.html", {})


    def logout_user(request):
        logout(request)
        messages.success(request, "Logged-Out Successfully!")
        return redirect("home")


    def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None

        if myuser is not None and generate_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            login(request, myuser)
            messages.success(request, "Account Activated Successfully!")
            return redirect("home")
        else:
            return render(request, "activation_failed.html")


    def sourcecode(request):
        allvideos = Video.objects.all()
        return render(request, "Home/sourcecode.html", {"allvideos": allvideos})


    def search(request):
        if request.method == "POST":
            searched = request.POST.get("searched")
            videos = Video.objects.filter(video_name__contains=searched)

            return render(
                request, "Home/search.html", {"searched": searched, "videos": videos}
            )
        else:
            return render(request, "Home/error_search.html", {})


    def search(request):
        if request.method == "POST":
            searched = request.POST.get("searched")

            videos = Video.objects.filter(video_name__contains=searched)
            heigtvideos = len(videos)

            return render(
                request, "Home/search.html", {"searched": searched, "videos": videos , "heightvideos" : heigtvideos}
            )
        else:
            return render(request, "Home/error_search.html", {})

    def practice(request):
        return render(request , "Home/practice.html")

    import sys
    # Create your views here.
    def python(request):
        res = render(request,'Home/python.html')
        return res

    def runcode(request):
        if request.method == 'POST':
            code_part = request.POST['code_area']
            input_part = request.POST['input_area']
            y = input_part
            input_part = input_part.replace("\n"," ").split(" ")
            def input():
                a = input_part[0]
                del input_part[0]
                return a
            try:
                orig_stdout = sys.stdout
                sys.stdout = open('file.txt', 'w')
                exec(code_part)
                sys.stdout.close()
                sys.stdout=orig_stdout
                output = open('file.txt', 'r').read()
            except Exception as e:
                sys.stdout.close()
                sys.stdout=orig_stdout
                output = e
            print(output)
        res = render(request,'Home/python.html',{"code":code_part,"input":y,"output":output})
        return res

    def html(request):
        return render(request , 'Home/htmlcssjs.html')
    def error_404(request , exception):
        return render(request,'Home/404error.html' )
except:
    HttpResponse('Something Gone wrong')