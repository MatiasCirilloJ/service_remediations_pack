import sys
import os
import time
import json

from st2common.runners.base_action import Action

def send_command(service, service_data):
    remote_with_service = remote.format(service_data[service]['host'], service_data[service]['username'], service_data[service]['private_key'], '{}')
    os.system(io_rule.format('disable'))    #Disable webhook rule
    for cmd in service_data[service]['cmd']:
        #os.system(remote_with_service.format(service_data[service]['cmd'][cmd]))
        with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
            f.write(remote_with_service.format(service_data[service]['cmd'][cmd]) + "\n")
        time.sleep(20)
    os.system(io_rule.format('enable'))    #Enable webhook rule

class ServiceRemediationsAction(Action):
    def run(self, message, id=None, idTag=None, levelTag=None, messageField=None, durationField=None):
        try:
            with open("/opt/stackstorm/packs/service_remediations_pack/actions/logs.txt", "a") as f:
                f.write(message + "\n")

            with open('/opt/stackstorm/packs/service_remediations_pack/actions/service_data.json') as file:
                service_data = json.load(file)
            io_rule = service_data['Commands']['IO_rule']
            remote = service_data['Commands']['remote']

            service = message.split()[0]
            value = int(message[-1])

            if service in service_data and value != 0:
                send_command(service, service_data)

            return (True, "Success")

        except IOError:
            return (False, "File not accessible")
        except:
            return (False)