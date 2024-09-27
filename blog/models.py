from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline


my_input = "example_username"

Entry.objects.all().filter(pub_date__year=2006)
Entry.objects.get(headline__contains="Lennon")
Blog.objects.filter(entry__authors__name="Lennon")
Blog.objects.filter(entry__authors__name__isnull=True)
Blog.objects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)
Blog.objects.filter(entry__headline__contains="Lennon").filter(entry__pub_date__year=2008)


async def get_entries():
    async for entry in Author.objects.filter(name__startswith="A"):
        user = await User.objects.filter(username=my_input).afirst()


class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.name


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateField()

    def __str__(self):
        return self.question


Q(question__startswith="What")
Q(question__startswith="Who") | Q(question__startswith="What")
Q(question__startswith="Who") | ~Q(pub_date__year=2005)
Poll.objects.get(
    Q(question__startswith="Who"),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
)


class ThemeBlog(Blog):
    theme = models.CharField(max_length=200)


django_blog = ThemeBlog(name="Django", tagline="Django is easy", theme="python")
django_blog.save()

django_blog.pk = None
django_blog.id = None
django_blog._state.adding = True
django_blog.save()

entry = Entry.objects.all()[0]
old_authors = entry.authors.all()
entry.pk = None
entry._state.adding = True
entry.save()
entry.authors.set(old_authors)


class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    details = models.TextField()


Entry.objects.filter(pub_date__year=2007).update(headline="Everything is the same")

class EntryManager(models.Manager):
    def is_published(self):
        return self.filter(pub_date__lte=date.today())


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    objects = models.Manager()
    entries = EntryManager()


b = Blog.objects.get(id=1)
b.entry_set(manager="entries").all()
b.entry_set(manager="entries").is_published()

e = Entry.objects.get(id=3)
e.authors.all()
e.authors.count()
e.authors.filter(name__contains="John")

a = Author.objects.get(id=5)
a.entry_set.all()

e1 = Author.objects.get(id=1)
e2 = Author.objects.get(id=2)

a.entry_set.set([e1, e2])
a.entry_set.set([e1.pk, e2.pk])


ed = EntryDetail.objects.get(id=2)
ed.entry
e = Entry.objects.get(id=2)
e.entrydetail
Entry.objects.filter(blog=b)
Entry.objects.filter(blog=b.id)
Entry.objects.filter(blog=5)
