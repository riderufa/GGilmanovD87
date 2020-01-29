from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    print(action)
    if action == "post_add":

        for cat in instance.category.all():
            slug = cat.slug

            new_count = 0
            for task in TodoItem.objects.all():
                new_count += task.category.filter(slug=slug).count()

            Category.objects.filter(slug=slug).update(todos_count=new_count)

    if action == "post_remove":
        cat_counter = Counter()
        for cat in Category.objects.all():
            cat_counter[cat.slug] = 0
        for t in TodoItem.objects.all():
            for cat in t.category.all():
                cat_counter[cat.slug] += 1
        for slug, new_count in cat_counter.items():
            Category.objects.filter(slug=slug).update(todos_count=new_count)

 
@receiver(post_delete)
def task_cats_removed(sender, instance, **kwargs):

    cat_counter = Counter()
    for cat in Category.objects.all():
        cat_counter[cat.slug] = 0
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1
    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)

@receiver(post_save)
def task_saved(sender, instance, **kwargs):

    priority_counter = Counter()
    for todo in TodoItem.objects.all():
        priority_counter[todo.priority] = 0
    for todo in TodoItem.objects.all():
        priority_counter[todo.priority] += 1
    for name_priority, new_count in priority_counter.items():
        Priority.objects.filter(name=name_priority).update(todos_count=new_count)

@receiver(post_delete)
def task_deleted(sender, instance, **kwargs):
    
    priority_counter = Counter()
    for priority in Priority.objects.all():
        priority_counter[priority.name] = 0
    for todo in TodoItem.objects.all():
        priority_counter[todo.priority] += 1
    print(priority_counter)
    for name_priority, new_count in priority_counter.items():
        Priority.objects.filter(name=name_priority).update(todos_count=new_count)