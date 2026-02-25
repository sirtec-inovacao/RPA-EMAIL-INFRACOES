from src.ponto_mais.utilities.email.email import Email
import os


# Destinatários RS
to_listRS = ['email1@example.com', 'email2@example.com']
cc_listRS = ['cc1@example.com', 'cc2@example.com']   

# Destinatários CE
to_listCE = ['email1@example.com', 'email2@example.com']
cc_listCE = ['cc1@example.com', 'cc2@example.com']   

# Destinatários VRC
to_listVTC = ['email1@example.com', 'email2@example.com']
cc_listVTC = ['cc1@example.com', 'cc2@example.com']   

# Destinatários BAR
to_listBAR = ['email1@example.com', 'email2@example.com']
cc_listBAR = ['cc1@example.com', 'cc2@example.com']   

# Destinatários FRS
to_listFRS = ['email1@example.com', 'email2@example.com']
cc_listFRS = ['cc1@example.com', 'cc2@example.com']   

# Destinatários PEL
to_listPEL = ['email1@example.com', 'email2@example.com']
cc_listPEL = ['cc1@example.com', 'cc2@example.com']

emails_list = [
    Email("jyeversonsantos@gmail.com", "iwwf vxny whse lhee", to_listRS, cc_listRS, "RS"),
    Email("jyeversonsantos@gmail.com", "iwwf vxny whse lhee", to_listCE, cc_listCE, "RS"),
    Email("jyeversonsantos@gmail.com", "iwwf vxny whse lhee", to_listVTC, cc_listVTC, "RS"),
    Email("jyeversonsantos@gmail.com", "iwwf vxny whse lhee", to_listBAR, cc_listBAR, "RS"),
    Email("jyeversonsantos@gmail.com", "iwwf vxny whse lhee", to_listFRS, cc_listFRS, "RS"),
    Email("jyeversonsantos@gmail.com", "iwwf vxny whse lhee", to_listPEL, cc_listPEL, "RS"),
]
