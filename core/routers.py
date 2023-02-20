from django.db.utils import DEFAULT_DB_ALIAS


class SecondaryDatabaseRouter:
    app_name = ['admin_tools_stats', 'django_nvd3', 'bootstrap_admin', 'django.contrib.admin',
                                     'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                                     'django.contrib.messages', 'django.contrib.staticfiles', 'django_ledger',
                                     'easyaudit', 'django_archive', 'blog', 'dashboard', 'analytics', 'users',
                                     'assessments', 'data_browser', 'slick_reporting', 'crispy_forms',
                                     'django_quill', 'django.contrib.humanize']

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_name:
            return 'secondary'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Returns the name of the master database for write queries.
        """
        return 'default'

    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allows relations only if both objects are in the same database.
        """
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allows migrations only on the master database.
        """
        if db == 'default':
            return app_label not in self.app_name
        elif app_label in self.app_name:
            return False
        return None