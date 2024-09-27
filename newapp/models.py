from django.db import models

# Lớp cơ sở trừu tượng cho thông tin chung
class CommonInfo(models.Model):
    name = models.CharField("Tên", max_length=100)

    class Meta:
        abstract = True
        ordering = ["name"]

# Lớp Place với thông tin cơ bản
class Place(models.Model):
    name = models.CharField(max_length=50, help_text="Nhập tên địa điểm")
    address = models.CharField(max_length=80, help_text="Nhập địa chỉ")

    def __str__(self):
        return self.name

# Lớp Restaurant kế thừa từ Place
class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False, help_text="Có phục vụ hot dog không?")
    serves_pizza = models.BooleanField(default=False, help_text="Có phục vụ pizza không?")

    place_ptr = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.name} (Restaurant)"

# Lớp Supplier kế thừa từ Place
class Supplier(Place):
    customers = models.ManyToManyField(Place, related_name='providers', help_text="Chọn các khách hàng của nhà cung cấp")

    def __str__(self):
        return f"{self.name} (Supplier)"

# Lớp Person
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Lớp MyPerson (Mô hình proxy)
class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # Thực hiện một hành động nào đó
        pass

# Lớp OrderedPerson (Mô hình proxy)
class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True

# Trình quản lý tùy chỉnh
class NewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)  # Ví dụ, lọc theo trường active

# Lớp MyPerson với trình quản lý tùy chỉnh
class MyPersonWithManager(Person):
    objects = NewManager()

    class Meta:
        proxy = True

# Lớp Album
class Album(models.Model):
    artist = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='albums', verbose_name="Nhạc sĩ")
    name = models.CharField("Tên album", max_length=100, help_text="Nhập tên album")
    release_date = models.DateField("Ngày phát hành", help_text="Nhập ngày phát hành album")
    num_stars = models.IntegerField("Số sao đánh giá", help_text="Nhập số sao đánh giá album")

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        print(f"Saving album: {self.name}")
        super().save(**kwargs)

# Lớp Musician kế thừa từ CommonInfo
class Musician(CommonInfo):
    first_name = models.CharField("Tên đầu tiên của nhạc sĩ", max_length=50, help_text="Nhập tên đầu tiên của nhạc sĩ")
    last_name = models.CharField("Họ của nhạc sĩ", max_length=50, help_text="Nhập họ của nhạc sĩ")
    instrument = models.CharField("Loại nhạc cụ", max_length=100, help_text="Nhập loại nhạc cụ")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, **kwargs):
        print(f"Saving musician: {self.first_name} {self.last_name}")
        super().save(**kwargs)

# Lớp Fruit kế thừa từ CommonInfo
class Fruit(CommonInfo):
    name = models.CharField("Tên loại trái cây", max_length=100, help_text="Nhập tên của loại trái cây", unique=True)

    def __str__(self):
        return self.name

# Lớp Manufacturer kế thừa từ CommonInfo
class Manufacturer(CommonInfo):
    pass

# Lớp Car
class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Nhà sản xuất")
    model = models.CharField("Mô hình xe", max_length=100)

    def __str__(self):
        return self.model

# Lớp Group
class Group(models.Model):
    name = models.CharField("Tên nhóm", max_length=128)
    members = models.ManyToManyField(Person, through="Membership", related_name="%(app_label)s_%(class)s_members", verbose_name="Danh sách thành viên")

    def __str__(self):
        return self.name

# Lớp Membership
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Người tham gia", related_name="%(app_label)s_%(class)s_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Nhóm", related_name="%(app_label)s_%(class)s_memberships")
    date_joined = models.DateField("Ngày tham gia")
    invite_reason = models.CharField("Lý do mời", max_length=64)

    def __str__(self):
        return f"{self.person.name} - {self.group.name}"

# Lớp Ox
class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"

    def __str__(self):
        return f"Ox with horn length {self.horn_length}"

# Lớp PersonWithStatus
class PersonWithStatus(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime

        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        "Returns the person's full name."
        return f"{self.first_name} {self.last_name}"
