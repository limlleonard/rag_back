from django.db import models

# Create your models here.


class File(models.Model):
    username = models.ForeignKey
    filepath = models.FileField

    # property decorator
    def filename(self):
        return self.filename.filepath.split("/")[-1]


files = File.objects.filter(username="user1")
filenames = [file.filename for file in files]

first_file = files.first()
username = first_file.username
filepath = first_file.filepath
filename = first_file.filename()


# object(filter username = user1)
# get filename from filepath
# serialize the request body

filepath1 = file1.filepath
filename = filepath1.split("/")[-1]
