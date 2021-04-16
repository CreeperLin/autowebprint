import os


class NoneDisplay:

    def __enter__(self, disp=None):
        self.disp = disp

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self.disp is not None:
            os.environ['DISPLAY'] = self.disp
