# Generated by Django 5.1.2 on 2024-11-07 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('I', 'In Progress')], max_length=1)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('priority', models.CharField(choices=[('L', 'Low'), ('H', 'High'), ('M', 'Medium')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='TaskTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('task', models.ManyToManyField(related_name='tags', to='taskmans.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='createdBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to='taskmans.user'),
        ),
        migrations.CreateModel(
            name='AssignedTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmans.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmans.user')),
            ],
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['createdBy', 'title', 'createdAt', 'due_date'], name='taskmans_ta_created_0d750c_idx'),
        ),
        migrations.AddIndex(
            model_name='assignedto',
            index=models.Index(fields=['task', 'user'], name='taskmans_as_task_id_d7d8d9_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='assignedto',
            unique_together={('task', 'user')},
        ),
    ]
