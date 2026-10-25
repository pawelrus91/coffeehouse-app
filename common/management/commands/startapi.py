from django.core.management.templates import TemplateCommand

APP_TEMPLATE_DIR = './template/app_template/.'


class Command(TemplateCommand):
    help = (
        'Creates a API Django app directory structure for the given app name in '
        'the current directory or optionally in the given directory.'
    )
    missing_args_message = 'You must provide an API application name.'

    def handle(self, **options):
        app_name = options.pop('name')
        target = options.pop('directory')
        if 'template' not in options:
            options['template'] = APP_TEMPLATE_DIR
        super().handle('app', app_name, target, **options)
