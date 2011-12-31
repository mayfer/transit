from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from transit.schedule.dbimport import import_all

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print "importing db"
        import_all()
        print "done"
    
