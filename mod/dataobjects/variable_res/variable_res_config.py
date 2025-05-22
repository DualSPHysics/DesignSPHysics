from mod.dataobjects.variable_res.bufferbox import BufferBox
from mod.tools.freecad_tools import delete_object, create_vres_buffer_box
from mod.tools.stdout_tools import debug


class VariableResConfig:

    def __init__(self):
        self.active : bool = False
        self.bufferbox_list:list[BufferBox] = []
        self.n_boxes: int = 0
        self.vres_buffer_size_h:int = 2

    def add_bufferbox(self):
        bufferbox=BufferBox(self.n_boxes)
        bufferbox.fc_object_name=create_vres_buffer_box(bufferbox)
        self.n_boxes = self.n_boxes + 1
        self.bufferbox_list.append(bufferbox)
        return bufferbox

    def remove_bufferbox_list(self,rm_list):
        for id in rm_list:
            self.bufferbox_list.pop(id)
        self.update_ids()

    def remove_bufferbox(self,id: int):
        buff=self.bufferbox_list.pop(id)
        delete_object(buff.fc_object_name)
        self.update_ids()

    def remove_with_children(self,id:int):
        to_remove = [id]
        while to_remove :
            rem = to_remove.pop()
            rem_obj = self.get_bufferbox_by_id(rem)
            sons = self.get_children(rem)
            self.remove_bufferbox(rem_obj.id)
            #self.bufferbox_list.remove(rem_obj)
            #if sons
            for son in sons:
                to_remove.append(son.id)
        #self.update_ids()

    def get_children(self, id: int):
        sons_list = []
        for bf in self.bufferbox_list:
            if bf.parent is not None:
                if bf.parent.id == id:
                    sons_list.append(bf)
        return sons_list

    def get_descendance(self,id: int):
        sons_list=[self.get_bufferbox_by_id(id)]
        return_list=[]
        while sons_list:
            son=sons_list.pop(0)
            new_sons=self.get_children(son.id)
            sons_list= sons_list + new_sons
            return_list = return_list + new_sons
        return return_list



    def get_bufferbox_by_id(self,id:int):
        for bf in self.bufferbox_list:
            if id ==bf.id:
                return bf
        return None

    def update_ids(self):
        for bf in self.bufferbox_list:
            bf.id=self.bufferbox_list.index(bf)
        self.n_boxes = len(self.bufferbox_list)

