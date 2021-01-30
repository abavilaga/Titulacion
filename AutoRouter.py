from ncclient import manager
import xmltodict

user = 'admin'
password = 'admin'

router = {'host': '192.168.1.252', 'port': '830',
          'username': user, 'password': password}

netconf_filter = """
 <filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet4</name>
    </interface>
  </interfaces>
  <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet4</name>
    </interface>
  </interfaces-state>
</filter>
"""

netconf_config = """
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
	<interface>
	  <name>{interface_name}</name>
	  <description>{interface_desc}</description>	  
	  <enabled>true</enabled>	  
	</interface>
  </interfaces>
</config>
"""

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
	print('Connected')
	interface_netconf_old = m.get(netconf_filter)
	#m.close_session()

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
	print('Connected')
	netconf_config = netconf_config.format(
	interface_name="GigabitEthernet4", interface_desc="Config from netconf")
	device_reply = m.edit_config(netconf_config, target="running")
	#print(device_reply)

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
	print('Connected')
	interface_netconf_new = m.get(netconf_filter)
	#m.close_session()

# XMLTODICT for converting xml output to a python dictionary
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ interface_python antes: ')
# print(interface_netconf)
interface_data_old = xmltodict.parse(interface_netconf_old.xml)["rpc-reply"]["data"]
interface_config_reply = xmltodict.parse(device_reply.xml)["rpc-reply"]
interface_data_new = xmltodict.parse(interface_netconf_new.xml)["rpc-reply"]["data"]

#print('################################################ interface_config_reply: ')
#print(interface_config_reply)
print(interface_config_reply.get('ok'))
if 'ok' in interface_config_reply:
	print ('Configuration applied')
else:
	print ('Something went wrong')
print('#########################################################################')

config_old = interface_data_old["interfaces"]["interface"]
config_new = interface_data_new["interfaces"]["interface"]
op_state_old = interface_data_old["interfaces-state"]["interface"]
op_state_new = interface_data_new["interfaces-state"]["interface"]

print("Old")
print(f"Name: {config_old['name']['#text']}")
print(f"Description: {config_old['description']}")
print(f"Pakcets In {op_state_old['statistics']['in-unicast-pkts']}")

print("New")
print(f"Name: {config_new['name']['#text']}")
print(f"Description: {config_new['description']}")
print(f"Pakcets In {op_state_new['statistics']['in-unicast-pkts']}")