import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils import timezone

# applications.globals.models file has been added over here because this requires global models as well
# if that part has been done earlier then we could imported it directly instead of copy pasting.
# .....................................................................................................................
class Constants:
    # Class for various choices on the enumerations
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    USER_CHOICES = (
        ('student', 'student'),
        ('staff', 'staff'),
        ('compounder', 'compounder'),
        ('faculty', 'faculty')
    )

    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    MODULES = (
        ("academic_information", "Academic"),
        ("central_mess", "Central Mess"),
        ("complaint_system", "Complaint System"),
        ("eis", "Employee Imformation System"),
        ("file_tracking", "File Tracking System"),
        ("health_center", "Health Center"),
        ("leave", "Leave"),
        ("online_cms", "Online Course Management System"),
        ("placement_cell", "Placement Cell"),
        ("scholarships", "Scholarships"),
        ("visitor_hostel", "Visitor Hostel"),
        ("other", "Other"),
    )

    ISSUE_TYPES = (
        ("feature_request", "Feature Request"),
        ("bug_report", "Bug Report"),
        ("security_issue", "Security Issue"),
        ("ui_issue", "User Interface Issue"),
        ("other", "Other than the ones listed"),
    )

    TITLE_CHOICES = (
        ("Mr.", "Mr."),
        ("Mrs.", "Mrs."),
        ("Ms.", "Ms."),
        ("Dr.", "Dr."),
        ("Professor", "Prof."),
        ("Shreemati", "Shreemati"),
        ("Shree", "Shree")
    )

    DESIGNATIONS = (
        ('academic', 'Academic Designation'),
        ('administrative', 'Administrative Designation'),
    )
    USER_STATUS = {
        ("NEW", "NEW"),
        ("PRESENT", "PRESENT"),
    }


class Designation(models.Model):
    '''
        Current Purpose : To store and segregate information regarding a designation in a the department  
        Eg : rewacaretaker -- Administrative designation

        ATTRIBUTES :

        name(char) - to store the designation name as information eg: dean_rspc
        full_name(char) - to store the full name of the designation eg: Dean(Research, Sponsered Projects and Consultancy)
        type(char) - to store the designation type eg: Academic designation
    '''
    name = models.CharField(max_length=50, unique=True,
                            blank=False, default='student')
    full_name = models.CharField(
        max_length=100, default='Computer Science and Engineering')

    type = models.CharField(
        max_length=30, default='academic', choices=Constants.DESIGNATIONS)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'globals_designation'


class DepartmentInfo(models.Model):
    '''
        Current Purpose : To store the list of departments in the institute 
        Eg : CSE, ME, Finance etct
        ! - Disciplines(CSE,ECE,etc) and Departments(Finance,etc) are under the same table.
        ! - Can incorporate more attributes

        ATTRIBUTES :

        name(char) - to store the department name as information
    '''

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return 'department: {}'.format(self.name)
    
    class Meta:
        db_table = 'globals_departmentinfo'


class ExtraInfo(models.Model):
    '''
        Current Purpose : to store one to one mapping of information for each user under django.contrib.auth.User

        

        ATTRIBUTES :

        id(char) - primary key defined for augmenting extra information (is redundant)
        user(User) - one to one field for linking the extra information to the User
        title(char) - to store title of the personeg : Mr, Ms, Dr)
        sex(char) - to store the gender from SEX_CHOICES
        date_of_birth(DateTime) - Date of birth of user
        user_status(char) - Defines whether the user is new or is already part of the Institute
        address(char) - address of the user
        phone_no(BigInt) - the phone number of the user
        user_type(char) - type of user (eg : student, staff)
        department(DepartmentInfo) - to link a user to a department from DepartmentInfo table
        profile_picture(ImageField) - profile photo of the user
        about_me(text) - to store extra information of the user

    '''
    id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20, choices=Constants.TITLE_CHOICES, default='Dr.')
    sex = models.CharField(
        max_length=2, choices=Constants.SEX_CHOICES, default='M')
    date_of_birth = models.DateField(default=datetime.date(1970, 1, 1))
    user_status = models.CharField(
        max_length=50, choices=Constants.USER_STATUS, default='PRESENT')
    address = models.TextField(max_length=1000, default="")
    phone_no = models.BigIntegerField(null=True, default=9999999999)
    user_type = models.CharField(max_length=20, choices=Constants.USER_CHOICES)
    department = models.ForeignKey(
        DepartmentInfo, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to='globals/profile_pictures')
    about_me = models.TextField(default='NA', max_length=1000, blank=True)
    date_modified = models.DateTimeField('date_updated', blank=True, null=True)

    @property
    def age(self):
        timedelta = timezone.now().date() - self.date_of_birth
        return int(timedelta.days / 365)

    def __str__(self):
        return '{} - {}'.format(self.id, self.user.username)
    
    class Meta:
        db_table = 'globals_extrainfo'


class HoldsDesignation(models.Model):
    """
    Purpose : Records designations held by users.

    ATTRIBUTES :
    'user' refers to the permanent/tenured holder of the designation.
    'working' always refers to the user who's holding the title, either permanently or temporarily
    Use 'working' to handle permissions in code

    'designation(Designation)' - maps the designation to the user 
    held_at(DateTime) - stores the time at which the position was held
    """
    user = models.ForeignKey(
        User, related_name='holds_designations', on_delete=models.CASCADE)
    working = models.ForeignKey(
        User, related_name='current_designation', on_delete=models.CASCADE)
    designation = models.ForeignKey(
        Designation, related_name='designees', on_delete=models.CASCADE)
    held_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'designation'], ['working', 'designation']]

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.designation)
    
    class Meta:
        db_table = 'globals_holdsdesignation'


# TODO : ADD additional staff related fields when needed
class Staff(models.Model):
    '''
        Current Purpose : To store attributes relevant to a staff member 
        
        ! - Not complete yet

        ATTRIBUTES :

        id(ExtraInfo) - to establish attributes to a user
    '''
    id = models.OneToOneField(
        ExtraInfo, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'globals_staff'


# TODO : ADD additional employee related fields when needed
class Faculty(models.Model):
    '''
        Current Purpose : To store attributes relevant to a faculty 
        
        ! - Not complete yet

        ATTRIBUTES :

        id(ExtraInfo) - to establish attributes to a user
    '''
    id = models.OneToOneField(
        ExtraInfo, on_delete=models.CASCADE, primary_key=True)

        

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'globals_faculty'


""" Feedback and bug report models start"""


class Feedback(models.Model):
    '''
        Current Purpose : To store the feedback of a user 
        
        

        ATTRIBUTES :

        user(User) - the 1-1 attribute for the user who has given a feedback
        rating - the rating given by the user
        feedback(Text) - the descriptive feedback given by the user
        timestamp(DateTime) - to store when the feedback was registered
    '''


    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="fusion_feedback")
    rating = models.IntegerField(choices=Constants.RATING_CHOICES)
    feedback = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ": " + str(self.rating)
    
    class Meta:
        db_table = 'globals_feedback'


def Issue_image_directory(instance, filename):
    return 'issues/{0}/images/{1}'.format(instance.user.username, filename)


class IssueImage(models.Model):
    '''
        Current Purpose : To store images of an issue by a user 
        
        

        ATTRIBUTES :

        user(User) - to link the user who will upload the image
        image(Image) - the image of the issue
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Issue_image_directory)

    class Meta:
        db_table = 'globals_issueimage'


class Issue(models.Model):

    '''
        Current Purpose : To link an issue with issue images by a user and relevant details of the issue
        
        

        ATTRIBUTES :

        user(User) - to link the user who is reporting the issue
       report_type(char) - to store the issue type (eg: feature request, bug report etc ) 
       module(char) -  to store in which module the issue was found(eg : Academic, Mess etc)
       closed(boolean) -  to denote whether the issue has been resolved or not
       text(Text) -  textual description of the issue
       title(char) -  to store the title of the issue
       images(IssueImage) - reference to the images for the issue
       support(User) - manyTomany field to store the users who also support the issue
       timestamp(DateTime) - to keep track when the issue was first created
       added_on(DateTime) - to keep track of when the issue was last modified

    '''
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reported_issues")
    report_type = models.CharField(
        max_length=63, choices=Constants.ISSUE_TYPES)
    module = models.CharField(max_length=63, choices=Constants.MODULES)
    closed = models.BooleanField(default=False)
    text = models.TextField()
    title = models.CharField(max_length=255)
    images = models.ManyToManyField(IssueImage, blank=True)
    support = models.ManyToManyField(User, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'globals_issue'


""" End of feedback and bug report models"""



class ModuleAccess(models.Model):
    designation = models.CharField(max_length=155)
    program_and_curriculum = models.BooleanField(default=False)
    course_registration = models.BooleanField(default=False)
    course_management = models.BooleanField(default=False)
    other_academics = models.BooleanField(default=False)
    spacs = models.BooleanField(default=False)
    department = models.BooleanField(default=False)
    examinations = models.BooleanField(default=False)
    hr = models.BooleanField(default=False)
    iwd = models.BooleanField(default=False)
    complaint_management = models.BooleanField(default=False)
    fts = models.BooleanField(default=False)
    purchase_and_store = models.BooleanField(default=False)
    rspc = models.BooleanField(default=False)
    hostel_management = models.BooleanField(default=False)
    mess_management = models.BooleanField(default=False)
    gymkhana = models.BooleanField(default=False)
    placement_cell = models.BooleanField(default=False)
    visitor_hostel = models.BooleanField(default=False)
    phc = models.BooleanField(default=False)

    def __str__(self):
        return self.designation
    
    class Meta:
        db_table = 'globals_moduleaccess'
    
# end of application.globals.models ...................................................................................


# Dean RSPC - applications.office_module.models --> same as applications.globals.models

# Dean RSPC Begins ....................................................................................................

class Constants2:
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    ACTION = (
        ('forward', 'forwarded'),
        ('revert', 'revert'),
        ('accept', 'accept'),
        ('reject', 'reject')

    )
    STATUS = (
        ('0', 'unseen'),
        ('1', 'seen')
    )
    APPROVAL = (
        ('0', 'reject'),
        ('1', 'accept')
    )
    APPROVAL_TYPE = (
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending'),
    )

    HALL_NO = (
        ('HALL-1','hall-1'),
        ('HALL-3','hall-3'),
        ('HALL-4','hall-4'),
    )
    DEPARTMENT=(
		('civil','civil'),
		('electrical','electrical')
	)

    BUILDING=(
		('corelab','corelab'),
		('computer center','computer center'),
		('hostel','hostel'),
		('mess','mess'),
		('library','library'),
		('cc','cc')
	)

    STATUS_CHOICES = (
        ('Forward', 'FORWARD'),
        ('Accept', 'ACCEPT')
    )



    PROJECT_TYPE = (
        ('SRes', 'Sponsored Research'),
        ('Consultancy', 'Consultancy'),
        ('fig', 'Faculty Initiation Grant'),
        ('Testing', 'Testing')
    )

    RESPONSE_TYPE = (
        ('Approve', 'Approve'),
        ('Disapprove', 'Disapprove'),
        ('Pending' , 'Pending')
    )

    RESPONSE_TYPE1 = (
        ('Forwarded', 'Forwarded'),
        ('Pending' , 'Pending')
    )

    TICK_TYPE = (
        ('NO', 'YES'),
        ('NO', 'NO')
    )

    PROJECT_OPERATED = (
        ('PI', 'Only by PI'),
        ('any', 'Either PI or CO-PI')
    )


    TRAVEL_CHOICES = (
        ('road', 'ROAD'),
        ('rail', 'RAIL')
      )

    TICK_TYPE = (
        ('Computer Graphics', 'Computer Graphics'),
        ('Machine Learning', 'Machine Learning'),
        ('Image Processing','Image Processing'),
        ('Data Structure','Data Structure')
    )

    APPROVAL_TYPE = (
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending'),
    )



PURCHASE_STATUS = (

    ('0', "Pending"),
    ('1', "Approve"),
    ('2', "Items Ordered"),
    ('3', "Items Puchased"),
    ('4', "Items Delivered"),

)

APPROVE_TAG = (

    ('0', "Pending"),
    ('1', "Approve"),
    ('-1',"Rejected"),
)


PURCHASE_TYPE = (

    ('0', "Amount < 25000"),
    ('1', "25000<Amount<250000"),

    ('2', "250000<Amount < 2500000"),
    ('3', "Amount>2500000"),

)

NATURE_OF_ITEM1 = (
    ('0', "Non-consumable"),
    ('1', "Consumable"),

)
NATURE_OF_ITEM2 = (
    ('0', "Equipment"),
    ('1', "Machinery"),
    ('2', "Furniture"),
    ('3', "Fixture"),

)

ITEM_TYPE = (
    ('0', "Non-consumable"),
    ('1', "Consumable"),

)

class Project_Registration(models.Model):
    PI_id = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    sponsored_agency = models.CharField(max_length=100)
    CO_PI = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True, blank=True)

    duration = models.IntegerField(default=0)
    agreement = models.CharField(choices=Constants2.TICK_TYPE,
                                 max_length=20, default='NO')
    amount_sanctioned = models.IntegerField(default=0)
    project_type = models.CharField(choices=Constants2.PROJECT_TYPE,
                                    max_length=25)
    project_operated = models.CharField(choices=Constants2.PROJECT_OPERATED,
                                        max_length=50, default='me')
    remarks = models.CharField(max_length=200)
    fund_recieved_date = models.DateField(null=True, blank=True)
    HOD_response = models.CharField(choices=Constants2.RESPONSE_TYPE1,
                                    max_length=10, default='Pending')
    DRSPC_response = models.CharField(choices=Constants2.RESPONSE_TYPE,
                                      max_length=10, default='Pending')
    applied_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.project_title
    
    class Meta:
        db_table = 'office_module_project_registration'


"""
DEAN RSPC
Table for Project Extension
"""


class Project_Extension(models.Model):
    project_id = models.ForeignKey(Project_Registration, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    extended_duration = models.IntegerField(default=0)
    extension_details = models.CharField(max_length=300)
    HOD_response = models.CharField(choices=Constants2.RESPONSE_TYPE1,
                                    max_length=10, default='Pending')
    DRSPC_response = models.CharField(choices=Constants2.RESPONSE_TYPE,
                                      max_length=10, default='Pending')
    file = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return str(self.project_id)
    
    class Meta:
        db_table = 'office_module_project_extension'


"""
DEAN RSPC
Table for Project Closure
"""


class Project_Closure(models.Model):
    project_id = models.ForeignKey(Project_Registration, on_delete=models.CASCADE)
    completion_date = models.DateField(null=True, blank=True)
    # extended_duration = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(null=True, blank=True)

    expenses_dues = models.CharField(choices=Constants2.TICK_TYPE,
                                     max_length=20, default='Pending')
    expenses_dues_description = models.CharField(max_length=200, blank=True, null=True)
    payment_dues = models.CharField(choices=Constants2.TICK_TYPE,
                                    max_length=20, default='Pending')
    payment_dues_description = models.CharField(max_length=200, blank=True, null=True)
    salary_dues = models.CharField(choices=Constants2.TICK_TYPE,
                                   max_length=20, default='Pending')
    salary_dues_description = models.CharField(max_length=200, blank=True, null=True)
    advances_dues = models.CharField(choices=Constants2.TICK_TYPE,
                                     max_length=20, default='Pending')
    advances_description = models.CharField(max_length=200, blank=True, null=True)
    others_dues = models.CharField(choices=Constants2.TICK_TYPE,
                                   max_length=20, default='Pending')
    other_dues_description = models.CharField(max_length=200, blank=True, null=True)
    overhead_deducted = models.CharField(choices=Constants2.TICK_TYPE,
                                         max_length=20, default='Pending')
    overhead_description = models.CharField(max_length=200, blank=True, null=True)
    HOD_response = models.CharField(choices=Constants2.RESPONSE_TYPE1,
                                    max_length=10, default='Pending')
    DRSPC_response = models.CharField(choices=Constants2.RESPONSE_TYPE,
                                      max_length=10, default='Pending')
    remarks = models.CharField(max_length=300, null=True)
    extended_duration = models.CharField(default='0', max_length=100, null=True)

    def __str__(self):
        return str(self.project_id)
    
    class Meta:
        db_table = 'office_module_project_closure'


"""
DEAN RSPC
Table for Project Reallocation
"""


class Project_Reallocation(models.Model):
    project_id = models.ForeignKey(Project_Registration, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    previous_budget_head = models.CharField(max_length=300)
    previous_amount = models.IntegerField(default=0)
    pf_no = models.CharField(max_length=100, null=True)
    new_budget_head = models.CharField(max_length=300)
    new_amount = models.IntegerField(default=0)
    transfer_reason = models.CharField(max_length=300)
    HOD_response = models.CharField(choices=Constants2.RESPONSE_TYPE1,
                                    max_length=10, default='Pending')
    DRSPC_response = models.CharField(choices=Constants2.RESPONSE_TYPE,
                                      max_length=10, default='Pending')

    def __str__(self):
        return str(self.project_id)
    
    class Meta:
        db_table = 'office_module_project_reallocation'


# Dean RSPC ends ....................................................................................................


class emp_visits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    v_type = models.IntegerField(default = 1)
    country = models.CharField(max_length=500, default=" ")
    place = models.CharField(max_length=500, default=" ")
    purpose = models.CharField(max_length=500, default=" ")
    v_date = models.DateField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    entry_date = models.DateField(null=True,blank=True, default=datetime.datetime.now)

    def __str__(self):
        return 'PF No.: {}   Name: {}   Purpose: {}'.format(self.pf_no,self.country,self.purpose)

    def get_absolute_url(self):
        return reverse('eis:profile')
    
    class Meta:
        db_table = 'eis_emp_visits'


class emp_techtransfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    details = models.CharField(max_length=500, default=" ")
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)

    class Meta:
        db_table = 'eis_emp_techtransfer'


class emp_session_chair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    name = models.CharField(max_length=500, default=" ")
    event = models.TextField(max_length=2500, default=" ")
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    s_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True, default=1)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    remarks = models.CharField(default = " ", max_length=1000)

    def __str__(self):
        return 'PF No.: {}   Name: {}'.format(self.pf_no,self.name)
    
    class Meta:
        db_table = 'eis_emp_session_chair'


class emp_research_projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    ptype = models.CharField(max_length=100, default="Research")
    pi = models.CharField(max_length=1000, default=" ")
    co_pi = models.CharField(max_length=1500, default=" ")
    title = models.TextField(max_length=5000, default=" ")
    funding_agency = models.CharField(max_length=250, default=" ", null=True)
    financial_outlay = models.CharField(max_length=150, default=" ", null=True)
    STATUS_TYPE_CHOICES = (
        ('Awarded', 'Awarded'),
        ('Submitted', 'Submitted'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length = 10, choices = STATUS_TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    date_submission = models.DateField(null=True, blank=True)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)

    def __str__(self):
        return 'PF No.: {}   pi: {}  title: {}'.format(self.pf_no,self.pi, self.title)
    
    class Meta:
        db_table = 'eis_emp_research_projects'


class emp_research_papers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    R_TYPE_CHOICES = (
        ('Journal', 'Journal'),
        ('Conference', 'Conference'),
    )
    rtype = models.CharField(max_length=500, choices = R_TYPE_CHOICES, default='Conference')
    authors = models.CharField(max_length=500, null=True, blank=True)
    co_authors = models.CharField(max_length=500, null=True, blank=True)
    title_paper = models.CharField(max_length=2500, null=True, blank=True)
    name = models.CharField(max_length=2500, null=True, blank=True)
    paper = models.CharField(max_length=2500, blank=True,null=True)
    venue = models.CharField(max_length=2500, null=True, blank=True)
    volume_no = models.CharField(max_length=500, null=True , blank=True)
    page_no = models.CharField(max_length=500,null=True, blank=True)
    IS_SCI_TYPE_CHOICES = (
        ('SCI', 'SCI'),
        ('SCIE', 'SCIE'),
    )
    is_sci = models.CharField(max_length=6, choices=IS_SCI_TYPE_CHOICES, null=True, blank=True)
    isbn_no = models.CharField(max_length=250, null=True, blank=True)
    doi = models.CharField(max_length=1000,null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_acceptance = models.DateField(null=True, blank=True)
    date_publication = models.DateField(null=True, blank=True)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.CharField(max_length=500, choices=MONTH_CHOICES, null=True, blank=True, default=1)
    doc_id = models.CharField(max_length=50, null=True, blank=True)
    doc_description = models.CharField(max_length=1000, null=True, blank=True)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    STATUS_TYPE_CHOICES = (
        ('Published', 'Published'),
        ('Accepted', 'Accepted'),
        ('Communicated', 'Communicated'),
    )
    status = models.CharField(max_length=15, choices=STATUS_TYPE_CHOICES, null=True, blank=True)
    date_submission = models.DateTimeField(null=True, blank=True)
    reference_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'PF No.: {}   Author: {}  Title: {}'.format(self.pf_no,self.authors, self.title_paper)
    
    class Meta:
        db_table = 'eis_emp_research_papers'


class emp_published_books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    PTYPE_TYPE_CHOICES = (
        ('Book', 'Book'),
        ('Monograph', 'Monograph'),
        ('Book Chapter', 'Book Chapter'),
        ('Handbook', 'Handbook'),
        ('Technical Report', 'Technical Report'),
    )
    p_type = models.CharField(max_length=16, choices=PTYPE_TYPE_CHOICES)
    title = models.CharField(max_length=2500, default=" ")
    publisher = models.CharField(max_length=2500, default=" ")
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    pyear = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    authors = models.CharField(max_length=250, default=" ")
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    publication_date = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return 'PF No.: {}   Type: {}  Title: {}'.format(self.pf_no,self.p_type, self.title)
    
    class Meta:
        db_table = 'eis_emp_published_books'


class emp_patents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    p_no = models.CharField(max_length=150)
    title = models.CharField(max_length=1500)
    earnings = models.IntegerField(default=0)
    STATUS_TYPE_CHOICES = (
        ('Filed', 'Filed'),
        ('Granted', 'Granted'),
        ('Published', 'Published'),
        ('Owned', 'Owned'),
    )
    status = models.CharField(max_length=15, choices=STATUS_TYPE_CHOICES)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    p_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True, default=1)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return 'PF No.: {}   Status: {}  Title: {}'.format(self.pf_no,self.status, self.title)
    
    class Meta:
        db_table = 'eis_emp_patents'


class emp_mtechphd_thesis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    degree_type = models.IntegerField(default=1)
    title = models.CharField(max_length=250)
    supervisors = models.CharField(max_length=250)
    co_supervisors = models.CharField(max_length=250, null=True, blank=True)
    rollno = models.CharField(max_length=200)
    s_name = models.CharField(max_length=5000)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    s_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True, default=1)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    semester=models.IntegerField(default = 1, blank=True, null=True)
    STATUS_TYPE_CHOICES = (
        ('Awarded', 'Awarded'),
        ('Submitted', 'Submitted'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length = 10, choices = STATUS_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return 'PF No.: {}   Supervisor: {}  Title: {}'.format(self.pf_no,self.supervisors, self.title)
    
    class Meta:
        db_table = 'eis_emp_mtechphd_thesis'


class emp_keynote_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    KEYNOTE_TYPE_CHOICES = (
        ('Keynote', 'Keynote'),
        ('Plenary Address', 'Plenary Address'),
    )
    type = models.CharField(max_length=140, choices=KEYNOTE_TYPE_CHOICES, default='Keynote')
    title = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    venue = models.CharField(max_length=1000)
    page_no = models.CharField(max_length=100)
    isbn_no = models.CharField(max_length=200)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    k_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True, default=1)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)

    def __str__(self):
        return 'PF No.: {}   Name: {}  Title: {}'.format(self.pf_no,self.name, self.title)
    
    class Meta:
        db_table = 'eis_emp_keynote_address'


class emp_expert_lectures(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    LECTURE_TYPE_CHOICES = (
        ('Expert Lecture', 'Expert Lecture'),
        ('Invited Talk', 'Invited Talk'),
    )
    l_type = models.CharField(max_length=14, choices=LECTURE_TYPE_CHOICES, default='Expert Lecture', null=False)
    title = models.CharField(max_length=1000)
    place = models.CharField(max_length=1000)
    l_date = models.DateField(null=True, blank=True)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    l_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True, default=1)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)

    def __str__(self):
        return 'PF No.: {}  Title: {}'.format(self.pf_no, self.title)
    
    class Meta:
        db_table = 'eis_emp_expert_lectures'


class emp_event_organized(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    TYPE_CHOICES = (
        ('Training Program', 'Training Program'),
        ('Seminar', 'Seminar'),
        ('Short Term Program', 'Short Term Program'),
        ('Workshop', 'Workshop'),
        ('Any Other', 'Any Other'),
    )
    type = models.CharField(max_length=180, choices=TYPE_CHOICES)
    name = models.CharField(max_length=1000)
    sponsoring_agency = models.CharField(max_length=150)
    venue = models.CharField(max_length=100)
    ROLE_TYPE_CHOICES = (
        ('Convener', 'Convener'),
        ('Coordinator', 'Coordinator'),
        ('Co-Convener', 'Co-Convener'),
    )
    role = models.CharField(max_length=11, choices=ROLE_TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)

    def __str__(self):
        return 'PF No.: {}  Name: {}'.format(self.pf_no, self.name)
    
    class Meta:
        db_table = 'eis_emp_event_organized'


class emp_consultancy_projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    consultants = models.CharField(max_length=150)
    title = models.CharField(max_length=1000)
    client = models.CharField(max_length=1000)
    financial_outlay = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=500, null=True, blank=True)
    date_entry = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    STATUS_TYPE_CHOICES = (
        ('Completed', 'Completed'),
        ('Submitted', 'Submitted'),
        ('Ongoing', 'Ongoing')
    )
    status = models.CharField(default = 'Ongoing', max_length = 10, choices = STATUS_TYPE_CHOICES, null=True, blank=True)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return 'PF No.: {}  Consultants: {}'.format(self.pf_no, self.consultants)
    
    class Meta:
        db_table = 'eis_emp_consultancy_projects'


class emp_confrence_organised(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    name = models.CharField(max_length=500)
    venue = models.CharField(max_length=500)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    k_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True, default=1)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_entry = models.DateField(default=datetime.datetime.now, null=True, blank=True)
    ROLE1_TYPE_CHOICES = (
        ('Advisary Committee', 'Advisary Committee'),
        ('Program Committee', 'Program Committee'),
        ('Organised', 'Organised'),
        ('Conference Chair', 'Conference Chair'),
        ('Any Other', 'Any Other'),
    )
    role1 = models.CharField(max_length=200, choices=ROLE1_TYPE_CHOICES, null=True, blank=True, default="Any Other")
    role2 = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return 'PF No.: {}  Name: {}'.format(self.pf_no, self.name)
    
    class Meta:
        db_table = 'eis_emp_confrence_organised'


class emp_achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    pf_no = models.CharField(max_length=20)
    A_TYPE_CHOICES = (
        ('Award', 'Award'),
        ('Honour', 'Honour'),
        ('Prize', 'Prize'),
        ('Other', 'Other'),
    )
    a_type = models.CharField(max_length=180, choices=A_TYPE_CHOICES, default="Other")
    details = models.TextField(max_length=1550, default=" ")
    DAY_CHOICES = []
    for r in range(1, 32):
        DAY_CHOICES.append((r, r))
    a_day = models.IntegerField(('Day'), choices=DAY_CHOICES, null=True, blank=True)
    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    a_month = models.IntegerField(('Month'), choices=MONTH_CHOICES, null=True, blank=True)
    YEAR_CHOICES = []
    for r in range(1995, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    a_year = models.IntegerField(('year'), choices=YEAR_CHOICES, null=True, blank=True)
    date_entry = models.DateField(default=datetime.datetime.now)
    achievment_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return 'PF No.: {} {} : {}'.format(self.pf_no, self.a_type,self.details)

    def get_absolute_url(self):
        return reverse('eis:profile')
    
    class Meta:
        db_table = 'eis_emp_achievement'


class faculty_about(models.Model):
    # id= models.OneToOneField(ExtraInfo, on_delete=models.CASCADE)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    about = models.TextField(max_length=2500)
    doj = models.DateField(default=datetime.datetime.now)
    education = models.TextField(max_length=500)
    interest = models.TextField(max_length=500)
    contact = models.CharField(max_length=10,null=True, blank=True)
    github = models.CharField(max_length=100,null=True, blank=True)
    linkedin = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        db_table = 'eis_faculty_about'