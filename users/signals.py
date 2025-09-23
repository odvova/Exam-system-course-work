from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver


REQUIRED_GROUPS = ("hod", "teacher", "student")

@receiver(post_save, sender=get_user_model())
def assign_groups_on_user_save(sender, instance, created, **kwargs):
    
    if instance.is_superuser and not getattr(instance, "is_hod", False):
        instance.is_hod = True
        if not instance.is_staff:
            instance.is_staff = True
        instance.save(update_fields=["is_hod", "is_staff"])

    sync_user_groups(instance)


def ensure_groups_exist():
    for name in REQUIRED_GROUPS:
        Group.objects.get_or_create(name=name)

def sync_user_groups(user):
    """Map boolean flags on the user to group membership."""
    ensure_groups_exist()

    want = set()
    if getattr(user, "is_hod", False):
        want.add("hod")
    if getattr(user, "is_teacher", False):
        want.add("teacher")
    if getattr(user, "is_student", False):
        want.add("student")

    current = set(user.groups.values_list("name", flat=True))

    for g in want - current:
        user.groups.add(Group.objects.get(name=g))

    for g in current - want:
        if g in REQUIRED_GROUPS:
            user.groups.remove(Group.objects.get(name=g))

    should_be_staff = user.is_hod or user.is_teacher
    if should_be_staff != user.is_staff and not user.is_superuser:
        user.is_staff = should_be_staff
        user.save(update_fields=["is_staff"])

@receiver(post_migrate)
def create_groups_after_migrate(sender, **kwargs):
    """Ensure groups exist; optionally attach permissions by codename."""
    ensure_groups_exist()

    PERMS = {
        "hod": {
            "view_user","add_user","change_user","delete_user",
            "view_group","add_group","change_group","delete_group",
            "view_exam","add_exam","change_exam","delete_exam",
            "view_question","add_question","change_question","delete_question",
            "view_answer","add_answer","change_answer","delete_answer",
            "view_teacherrequest","add_teacherrequest","change_teacherrequest","delete_teacherrequest",
            "view_studentrequest","add_studentrequest","change_studentrequest","delete_studentrequest",
            "view_session","add_session","change_session","delete_session",
        },
        "teacher": {
            "view_exam","add_exam","change_exam","delete_exam",
            "view_question","add_question","change_question","delete_question",
            "view_answer","add_answer","change_answer","delete_answer",
            "view_teacherrequest","view_studentrequest",
        },
        "student": {
            "view_exam","view_question","add_answer","view_answer",
        },
    }

    all_perms = {p.codename: p for p in Permission.objects.all()}
    for gname, codenames in PERMS.items():
        g = Group.objects.get(name=gname)
        perms = [all_perms[c] for c in codenames if c in all_perms]
        g.permissions.set(perms)

@receiver(post_save, sender=get_user_model())
def update_groups_on_user_save(sender, instance, **kwargs):
    """Keep groups in sync whenever a user is created/updated."""
    sync_user_groups(instance)