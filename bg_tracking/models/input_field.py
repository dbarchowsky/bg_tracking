class InputField:

    required = False

    def collect_request_var(self, form, key):
        try:
            if len(str(form[key])) > 0:
                setattr(self, key, form[key])
        except KeyError:
            raise KeyError('Expected input is missing: {} \n'.format(key))
        except AttributeError:
            raise ValueError('Invalid input for {}.'.format(key))

    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required')
        super().__init__(self, *args, **kwargs)
