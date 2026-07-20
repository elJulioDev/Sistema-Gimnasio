from django.db import migrations

MAQUINAS = [
    ('Press banca', 'fuerza'),
    ('Sentadilla libre', 'fuerza'),
    ('Peso muerto', 'fuerza'),
    ('Press militar', 'fuerza'),
    ('Remo polea baja', 'fuerza'),
    ('Jalón al pecho', 'fuerza'),
    ('Prensa de piernas', 'fuerza'),
    ('Curl de bíceps', 'fuerza'),
    ('Extensión de tríceps', 'fuerza'),
    ('Máquina abductor/aductor', 'fuerza'),
    ('Hack squat', 'fuerza'),
    ('Peck deck', 'fuerza'),
    ('Trotadora', 'cardio'),
    ('Bicicleta estática', 'cardio'),
    ('Elíptica', 'cardio'),
    ('Escaladora', 'cardio'),
    ('Remo cardio', 'cardio'),
]

def seed_machines(apps, schema_editor):
    Machine = apps.get_model('routines', 'Machine')
    for nombre, categoria in MAQUINAS:
        Machine.objects.get_or_create(nombre=nombre, defaults={'categoria': categoria})

def unseed_machines(apps, schema_editor):
    Machine = apps.get_model('routines', 'Machine')
    Machine.objects.filter(nombre__in=[n for n, _ in MAQUINAS]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_machines, unseed_machines),
    ]