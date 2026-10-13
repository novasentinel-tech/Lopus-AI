"""Ponte conceitual entre plugins e o sistema de permissões do runtime.

Plugins não devem conceder permissões por conta própria. Eles devem declarar
quais permissões precisam e deixar a concessão/revogação sob controle do
usuário e do PermissionStore do runtime.
"""

from lopus.actions import Permission

PLUGIN_PERMISSION_EXAMPLES: dict[str, tuple[Permission, ...]] = {
    "mouse_pointer": (Permission.GUI_CONTROL,),
    "google_drive": (),
}

# Google Drive terá permissões próprias quando seu contrato de autenticação
# e escopos for implementado. Até lá, não há concessão automática.
