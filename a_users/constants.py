EXPERTISE_CHOICES = [
    ('web_dev', 'Web Development'),
    ('mobile_dev', 'Mobile Development'),
    ('data_science', 'Data Science'),
    ('machine_learning', 'Machine Learning'),
    ('cloud_computing', 'Cloud Computing'),
    ('cybersecurity', 'Cybersecurity'),
    ('ui_ux', 'UI/UX Design'),
    ('other', 'Other')
]
# User type choices
USER_TYPES = [
    ('MENTOR', 'Mentor'),
    ('MENTEE', 'Mentee'),
]

WORKING_STATUS_CHOICES = [
    ('EMPLOYED', 'Employed'),
    ('SELF_EMPLOYED', 'Self Employed'),
    ('UNEMPLOYED', 'Unemployed'),
]

# File upload limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'gif']
ALLOWED_DOCUMENT_TYPES = ['pdf', 'doc', 'docx']
ALLOWED_VIDEO_TYPES = ['mp4', 'avi', 'mkv']
# Default profile picture URL
