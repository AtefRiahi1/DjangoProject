from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import admin_role_required, both_role_required
from home.models import *
from home.forms import *
from about.models import *
from about.forms import *
from contact.models import *
from contact.forms import *
from settings.models import *
from settings.forms import *
from menus.models import *
from menus.forms import *
from legal.models import *
from legal.forms import *

# # # # # # # # # # # # # # # # # #
        # Admin Home Page #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@both_role_required
def adminHome(request):
    services = serviceSection.objects.all()
    projects = projectSection.objects.all()
    testimonials = testimonialsSection.objects.all()
    teams = teamSection.objects.all()
    clients = clientSection.objects.all()
    subscribers = Subscriber.objects.all().order_by('-created_at')
    contacts = Contact.objects.all().order_by('-created_at')

    context = {
        'title' : 'Dashboard',
        'services': services,
        'projects': projects,
        'testimonials': testimonials,
        'teams': teams,
        'clients': clients,
        'subscribers' : subscribers,
        'contacts' : contacts,
    }
    return render(request, 'dashboard/main/index.html', context)

# # # # # # # # # # # # # # # # # #
        # Admin Blog #
# # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # #
    # Admin Blog Categories #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
        # Admin Project #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
    # Admin Project Categories #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
        # Admin Service #
# # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # #
    # Admin Slider Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminSliderElementList(request):
    sliders = sliderSection.objects.all()
    context = {
        'title' : 'Sliders',
        'sliders' : sliders,
    }
    return render(request, 'dashboard/main/elements/slider/sliders.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminSliderElementCreate(request):
    if request.method == 'POST':
        form = sliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider created successfully!')
            return redirect('adminSliderElementList')
    else:
        form = sliderForm()
    context = {
        'title' : 'Create Slider',
        'form' : form,
    }
    return render(request, 'dashboard/main/elements/slider/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminSliderElementEdit(request, id):
    slider = get_object_or_404(sliderSection, id=id)
    if request.method == 'POST':
        form = sliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider updated successfully!')
            return redirect('adminSliderElementList')
    else:
        form = sliderForm(instance=slider)

    context = {
        'title' : 'Edit Slider',
        'form' : form,
        'slider' : slider,
    }
    return render(request, 'dashboard/main/elements/slider/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminSliderElementDelete(request, id):
    slider = get_object_or_404(sliderSection, id=id)
    slider.delete()
    messages.warning(request, 'Slider deleted!')
    return redirect('adminSliderElementList')

# # # # # # # # # # # # # # # # # #
    # Admin Fun Fact Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminFunFactElementList(request):
    facts = funFactSection.objects.all()
    context = {
        'title' : 'Fun Facts',
        'facts' : facts,
    }
    return render(request, 'dashboard/main/elements/funfact/funfacts.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminFunFactElementCreate(request):
    if request.method == 'POST':
        form = funFactSectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fun Fact created successfully!')
            return redirect('adminFunFactElementList')
    else:
        form = funFactSectionForm()
    context = {
        'title' : 'Create Fun Fact',
        'form' : form,
    }
    return render(request, 'dashboard/main/elements/funfact/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminFunFactElementEdit(request, id):
    fact = get_object_or_404(funFactSection, id=id)
    if request.method == 'POST':
        form = funFactSectionForm(request.POST, request.FILES, instance=fact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fun Fact updated successfully!')
            return redirect('adminFunFactElementList')
    else:
        form = funFactSectionForm(instance=fact)
    context = {
        'title' : 'Edit Fun Fact',
        'form' : form,
        'fact' : fact,
    }
    return render(request, 'dashboard/main/elements/funfact/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminFunFactElementDelete(request, id):
    fact = get_object_or_404(funFactSection, id=id)
    fact.delete()
    messages.warning(request, 'Fun Fact deleted!')
    return redirect('adminFunFactElementList')

# # # # # # # # # # # # # # # # # #
   # Admin Testimonials Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminTestimonialsElementList(request):
    testimonials = testimonialsSection.objects.all()
    context = {
        'title' : 'Testimonials',
        'testimonials' : testimonials,
    }
    return render(request, 'dashboard/main/elements/testimonial/testimonials.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminTestimonialsElementCreate(request):
    if request.method == 'POST':
        form = testimonialSectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial created successfully!')
            return redirect('adminTestimonialsElementList')
    else:
        form = testimonialSectionForm()
    context = {
        'title' : 'Create Testimonial',
        'form' : form,
    }
    return render(request, 'dashboard/main/elements/testimonial/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminTestimonialsElementEdit(request, id):
    testimonial = get_object_or_404(testimonialsSection, id=id)
    if request.method == 'POST':
        form = testimonialSectionForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect('adminTestimonialsElementList')
    else:
        form = testimonialSectionForm(instance=testimonial)
    context = {
        'title' : 'Edit Testimonial',
        'form' : form,
        'testimonial' : testimonial,
    }
    return render(request, 'dashboard/main/elements/testimonial/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminTestimonialsElementDelete(request, id):
    testimonial = get_object_or_404(testimonialsSection, id=id)
    testimonial.delete()
    messages.warning(request, 'Testimonial deleted!')
    return redirect('adminTestimonialsElementList')

# # # # # # # # # # # # # # # # # #
      # Admin Team Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminTeamElementList(request):
    teams = teamSection.objects.all()
    context = {
        'title' : 'Teams',
        'teams' : teams,
    }
    return render(request, 'dashboard/main/elements/team/teams.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminTeamElementCreate(request):
    if request.method == 'POST':
        form = teamSectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team memeber created successfully!')
            return redirect('adminTeamElementList')
    else:
        form = teamSectionForm()
    context = {
        'title' : 'Create Team',
        'form' : form,
    }
    return render(request, 'dashboard/main/elements/team/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminTeamElementEdit(request, id):
    team = get_object_or_404(teamSection, id=id)
    if request.method == 'POST':
        form = teamSectionForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team memeber updated successfully!')
            return redirect('adminTeamElementList')
    else:
        form = teamSectionForm(instance=team)
    context = {
        'title' : 'Edit Team',
        'form' : form,
        'team' : team,
    }
    return render(request, 'dashboard/main/elements/team/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminTeamElementDelete(request, id):
    team = get_object_or_404(teamSection, id=id)
    team.delete()
    messages.warning(request, 'Team memeber deleted!')
    return redirect('adminTeamElementList')

# # # # # # # # # # # # # # # # # #
    # Admin Client Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminClientElementList(request):
    clients = clientSection.objects.all()
    context = {
        'title' : 'Clients',
        'clients' : clients,
    }
    return render(request, 'dashboard/main/elements/client/clients.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminClientElementCreate(request):
    if request.method == 'POST':
        form = clientSectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully!')
            return redirect('adminClientElementList')
    else:
        form = clientSectionForm()
    context = {
        'title' : 'Create Client',
        'form' : form,
    }
    return render(request, 'dashboard/main/elements/client/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminClientElementEdit(request, id):
    client = get_object_or_404(clientSection, id=id)
    if request.method == 'POST':
        form = clientSectionForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully!')
            return redirect('adminClientElementList')
    else:
        form = clientSectionForm(instance=client)

    context = {
        'title' : 'Edit Client',
        'form' : form,
        'client' : client,
    }
    return render(request, 'dashboard/main/elements/client/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminClientElementDelete(request, id):
    client = get_object_or_404(clientSection, id=id)
    client.delete()
    messages.warning(request, 'Client deleted!')
    return redirect('adminClientElementList')

# # # # # # # # # # # # # # # # # #
    # Admin Pricing Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminPricingElementList(request):
    pricings = pricingSection.objects.all()
    context = {
        'title' : 'Pricing',
        'pricings' : pricings,
    }
    return render(request, 'dashboard/main/elements/pricing/pricing.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminPricingElementCreate(request):
    if request.method == 'POST':
        form = pricingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pricing created successfully!')
            return redirect('adminPricingElementList')
    else:
        form = pricingForm()
    context = {
        'title' : 'Create Pricing',
        'form' : form,
    }
    return render(request, 'dashboard/main/elements/pricing/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminPricingElementEdit(request, id):
    pricing = get_object_or_404(pricingSection, id=id)
    if request.method == 'POST':
        form = pricingForm(request.POST, request.FILES, instance=pricing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pricing updated successfully!')
            return redirect('adminPricingElementList')
    else:
        form = pricingForm(instance=pricing)
    context = {
        'title' : 'Edit Pricing',
        'form' : form,
        'pricing' : pricing,
    }
    return render(request, 'dashboard/main/elements/pricing/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def adminPricingElementDelete(request, id):
    pricing = get_object_or_404(pricingSection, id=id)
    pricing.delete()
    messages.success(request, 'Pricing deleted!')
    return redirect('adminPricingElementList')

# # # # # # # # # # # # # # # # # #
    # Admin Contacts #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def AdminContactList(request):
    contacts = Contact.objects.all()
    context = {
        'title' : 'Contacts',
        'contacts' : contacts,
    }
    return render(request, 'dashboard/main/form_data/contacts.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminContactDelete(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    messages.warning(request, 'Contact deleted!')
    return redirect('AdminContactList')

# # # # # # # # # # # # # # # # # #
    # Admin Subscriber #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def AdminSubscriberList(request):
    subscribers = Subscriber.objects.all()
    
    context = {
        'title' : 'Subscribers',
        'subscribers' : subscribers
    }
    return render(request, 'dashboard/main/form_data/subscribers.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminSubscriberDelete(request, id):
    subscriber = get_object_or_404(Subscriber, id=id)
    subscriber.delete()
    return redirect('AdminSubscriberList')

# # # # # # # # # # # # # # # # # #
    # Admin Website Settings #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def AdminWebsiteSettings(request):
    setting = websiteSetting.objects.first()
    if request.method == 'POST':
        form = websiteSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('AdminWebsiteSettings')
    else:
        form = websiteSettingForm(instance=setting)
    context = {
        'title' : 'Website Settings',
        'setting' : setting,
        'form' : form,
    }
    return render(request, 'dashboard/main/setting/website.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminHeaderFooterSettings(request):
    hf = headerFooterSetting.objects.first()
    if request.method == 'POST':
        form = headerFooterSettingForm(request.POST, request.FILES, instance=hf)
        if form.is_valid():
            form.save()
            messages.success(request, 'Header footer updated successfully!')
            return redirect('AdminHeaderFooterSettings')
    else:
        form = headerFooterSettingForm(instance=hf)
    context = {
        'title' : 'Header Footer Settings',
        'hf' : hf,
        'form' : form,
    }
    return render(request, 'dashboard/main/setting/hf.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminSEOSettings(request):
    seo = SeoSetting.objects.first()
    if request.method == 'POST':
        form = SeoSettingForm(request.POST, request.FILES, instance=seo)
        if form.is_valid():
            form.save()
            messages.success(request, 'SEO settings updated successfully!')
            return redirect('AdminSEOSettings')
    else:
        form = SeoSettingForm(instance=seo)
    context = {
        'title' : 'SEO Settings',
        'seo' : seo,
        'form' : form,
    }
    return render(request, 'dashboard/main/setting/seo.html', context)

# # # # # # # # # # # # # # # # # #
    # Admin Primary Menus #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def AdminPrimaryMenuList(request):
    menus = primaryMenu.objects.all()
    context = {
      'title' : 'Menus',
      'menus' : menus,
    }
    return render(request, 'dashboard/main/menu/primary/menus.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminPrimaryMenuCreate(request):
    if request.method == 'POST':
        form = primaryMenuForm(request.POST)
        if form.is_valid():
            order = form.cleaned_data['order']
            if primaryMenu.objects.filter(order=order).exists():
                form.add_error('order', 'A menu with this order already exists. Use a different order.')
            else:
                form.save()
                messages.success(request, 'Menu created successfully!')
                return redirect('AdminPrimaryMenuList')
    else:
        form = primaryMenuForm()

    context = {
        'title': 'Create Menu',
        'form': form,
    }
    return render(request, 'dashboard/main/menu/primary/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminPrimaryMenuEdit(request, id):
    menu = get_object_or_404(primaryMenu, id=id)
    if request.method == 'POST':
        form = primaryMenuForm(request.POST, instance=menu)
        if form.is_valid():
            order = form.cleaned_data['order']
            if primaryMenu.objects.filter(order=order).exclude(id=id).exists():
                form.add_error('order', 'A menu with this order already exists. Use a different order.')
            else:
                form.save()
                messages.success(request, 'Menu updated successfully!')
                return redirect('AdminPrimaryMenuList')
    else:
        form = primaryMenuForm(instance=menu)

    context = {
        'title': 'Edit Menu',
        'form': form,
      'menu': menu,
    }
    return render(request, 'dashboard/main/menu/primary/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminPrimaryMenuDelete(request, id):
    menu = get_object_or_404(primaryMenu, id=id)
    menu.delete()
    messages.warning(request, 'Menu deleted!')
    return redirect('AdminPrimaryMenuList')

# # # # # # # # # # # # # # # # # #
    # Admin Sub Menus #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def AdminSubMenuList(request):
    submenus = subMenu.objects.all()
    context = {
        'title' : 'Sub Menus',
        'submenus' : submenus,
    }
    return render(request, 'dashboard/main/menu/sub/menus.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminSubMenuCreate(request):
    if request.method == 'POST':
        form = subMenuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Submenu created successfully!')
            return redirect('AdminSubMenuList')
    else:
        form = subMenuForm()
    
    context = {
        'title': 'Create Submenu',
        'form': form,
    }
    return render(request, 'dashboard/main/menu/sub/create.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminSubMenuEdit(request, id):
    submenu = get_object_or_404(subMenu, id=id)
    if request.method == 'POST':
        form = subMenuForm(request.POST, instance=submenu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Submenu updated successfully!')
            return redirect('AdminSubMenuList')
    else:
        form = subMenuForm(instance=submenu)
    
    context = {
        'title': 'Edit Submenu',
        'form': form,
        'submenu': submenu,
    }
    return render(request, 'dashboard/main/menu/sub/edit.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminSubMenuDelete(request, id):
    submenu = get_object_or_404(subMenu, id=id)
    submenu.delete()
    messages.warning(request, 'Submenu deleted!')
    return redirect('AdminSubMenuList')

# # # # # # # # # # # # # # # # # #
    # Admin Page Edit #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def AdminHomePage(request):
    homeabout = aboutSection.objects.first()
    homeSEO = homePageSEO.objects.first()

    if request.method == 'POST':
        if 'subtitle' in request.POST:
            form = aboutSectionForm(request.POST, request.FILES, instance = homeabout)
            if form.is_valid():
                form.save()
                messages.success(request, 'Home page updated successfully!')
                return redirect('AdminHomePage')
        elif 'meta_title' in request.POST:
            SeoForm = homePageSEOForm(request.POST, request.FILES, instance = homeSEO)
            if SeoForm.is_valid():
                SeoForm.save()
                messages.success(request, 'Home page seo updated successfully!')
                return redirect('AdminHomePage')
        else:
            return redirect('AdminHomePage')
    else:
        form = aboutSectionForm(instance = homeabout)
        SeoForm = homePageSEOForm(instance = homeSEO)

    context ={
        'title' : 'Home Page',
        'form' : form,
        'SeoForm' : SeoForm,
        'homeabout' : homeabout,
    }
    return render(request, 'dashboard/main/pages/home.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminAboutPage(request):
    aboutSection = aboutPage.objects.first()
    aboutSEO = aboutPageSEO.objects.first()
    if request.method == 'POST':
        if 'subtitle' in request.POST:
            form = aboutPageForm(request.POST, request.FILES, instance=aboutSection)
            if form.is_valid():
                form.save()
                messages.success(request, 'About page updated successfully!')
                return redirect('AdminAboutPage')
        elif 'meta_title' in request.POST:
            SeoForm = aboutPageSEOForm(request.POST, request.FILES, instance = aboutSEO)
            if SeoForm.is_valid():
                SeoForm.save()
                messages.success(request, 'About page seo updated successfully!')
                return redirect('AdminAboutPage')
        else:
            return redirect('AdminAboutPage')
    else:
        form = aboutPageForm(instance=aboutSection)
        SeoForm = aboutPageSEOForm(instance=aboutSEO)

    context = {
        'title' : 'About Page',
        'form' : form,
        'SeoForm' : SeoForm,
    }
    return render(request, 'dashboard/main/pages/about.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminContactPage(request):
    contactSEO = contactPageSEO.objects.first()
    if request.method == 'POST':
        SeoForm = contactPageSEOForm(request.POST, instance = contactSEO)
        if SeoForm.is_valid():
            SeoForm.save()
            messages.success(request, 'Contact page seo updated successfully!')
            return redirect('AdminContactPage')
    
    else:
        SeoForm = contactPageSEOForm(instance =  contactSEO)

    context = {
        'title' : 'Contact Page',
        'SeoForm' : SeoForm,
    }
    return render(request, 'dashboard/main/pages/contact.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminTermsPage(request):
    term = Terms.objects.first()
    if request.method == 'POST':
        form = termsForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terms & condition updated successfully')
            return redirect('AdminTermsPage')
    else:
        form = termsForm(instance=term)

    context = {
        'title' : 'Terms Page',
        'form' : form,
    }
    return render(request, 'dashboard/main/pages/terms.html', context)

@login_required(login_url='logIn')
@admin_role_required
def AdminPolicyPage(request):
    policy = Policy.objects.first()
    if request.method == 'POST':
        form = policyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Privacy policy updated successfully')
            return redirect('AdminPolicyPage')
    else:
        form = policyForm(instance=policy)

    context = {
        'title' : 'Policy Page',
        'form' : form,
    }
    return render(request, 'dashboard/main/pages/policy.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/404.html', status=404)

def error_500(request):
    return render(request, 'error/500.html', status=500)

    
        


