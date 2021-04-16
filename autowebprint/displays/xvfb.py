import os
from subprocess import Popen


def start_xvfb(disp, scr_w=1920, scr_h=1080, scr_d=24, *extra_args):
    args = ['Xvfb', disp]
    args.extend(['-screen', '0', '{}x{}x{}'.format(scr_w, scr_h, scr_d)])
    args.extend(['-ac', '+extension', 'GLX', '+render', '-noreset'])
    args.extend(extra_args)
    proc = Popen(args)
    return proc


def kill_xvfb(proc):
    proc.terminate()
    proc.kill()


class XvfbDisplay:

    def __init__(self, disp=10, start=True, kill=True, *args, **kwargs) -> None:
        self.proc = None
        self.disp = ':{}'.format(disp) if isinstance(disp, int) else disp
        self.start = start
        self.kill = kill
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        if self.start:
            self.proc = start_xvfb(disp=self.disp, *self.args, **self.kwargs)
        os.environ['DISPLAY'] = self.disp

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self.kill:
            kill_xvfb(self.proc)
