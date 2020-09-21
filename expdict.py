from . import _utils as utils
import inspect
import dis

@utils.edit(dict, 'tp_iter')
@utils.nullwrap
def dict_iter(self):
    last_frame = inspect.currentframe().f_back
    for inst in dis.Bytecode(last_frame.f_code):
        if inst.opname in ['STORE_FAST', 'STORE_GLOBAL', 'STORE_NAME', 'STORE_DEREF']:
            yield self.get(inst.argval)
