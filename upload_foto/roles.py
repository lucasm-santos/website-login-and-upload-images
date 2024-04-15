from rolepermissions.roles import AbstractUserRole



class Noivos(AbstractUserRole):
    available_permissions = {'enviar_fotos': True, 'ver_galeria': True}


class Convidados(AbstractUserRole):
    available_permissions = {'ver_galeria': True}