import sys
import os
import time
import logging

from st2common.runners.base_action import Action

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write(message + "\n")
            service = message.split()[0]
            value = int(message[-1])
            if service == "NEP@L_Controller" and value != 0:
                os.system("st2 rule disable service_remediations_pack.service_remediations_rule")    #Disable webhook rule
                os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && docker-compose stop") 
                time.sleep(30)
                os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && docker-compose up -d")
                time.sleep(30)
                os.system("st2 run core.remote hosts='10.54.158.194' username='root' private_key='/home/stanley/.ssh/id_rsa' cmd='cd /opt/django-nepal-be && systemctl stop nodeserver && systemctl start nodeserver")
                os.system("st2 rule enable service_remediations_pack.service_remediations_rule")    #Enable webhook rule
                #logging.basicConfig(filename='/opt/stackstorm/packs/service_remediations_pack/actions/action.log', format='%(name)s - %(levelname)s - %(message)s')
                #logging.error(message)
            return (True, "Success")
        except IOError:
            return (False, "File not accessible")
        except:
            return (False)
        
        #os.system("st2 run core.remote hosts='10.54.158.243' username='root' password='Cordob12' cmd='cd /root ; echo $HOME")
