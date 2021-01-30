import requests
import json

user = 'admin'
password = 'admin'
spineList = ['192.168.1.4','192.168.1.5']
leafList = ['192.168.1.10','192.168.1.11','192.168.1.12']
payload = {'ins_api': {'version': '1.0', 'type': '', 'chunk': '0','sid': '1', 'input': '', 'output_format': 'json', }}
# - User inputs - #
vlanNum = ''
vlanName = ''
accesoLeaf = '3'

def ejecutar (payload, nexusList):
	respuesta = []
	try:
		for nexus in nexusList:
			print ('Nexus: ' + nexus)
			url = 'https://' + nexus + '/ins'
			headers = {'content-type': 'application/json'}
			response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(user, password), timeout=1, verify=False,).json()
			respuesta.append(json.dumps(response))
		return {'respuesta':respuesta}
	except Exception as e: 
		#print ("Se produjo un error: " + str(e))
		return {'respuesta': [{'nexus':'algo salio mal'}]}

def configurar (comando, nexusList):
	cliType = {'type': 'cli_conf'}
	payload['ins_api'].update(cliType)
	# - EX: vlan 10 ; name test - #
	commandInput = str(comando)
	commandInput = {'input': commandInput}
	payload['ins_api'].update(commandInput)
	respuesta = ejecutar(payload, nexusList)
	return respuesta

def verificar (comando, nexusList):
	cliType = {'type': 'cli_show'}
	payload['ins_api'].update(cliType)
	# - EX: show vlan id 10 - #
	commandInput = str(comando)
	commandInput = {'input': commandInput}
	payload['ins_api'].update(commandInput)
	respuesta = ejecutar(payload, nexusList)
	return respuesta

print ('Configurando vlan ' + vlanNum + ' en Spines')
comando = 'vlan ' + vlanNum + ' ; ' + 'name ' + vlanName
ejecuta = configurar(comando, spineList)

print ('Agregando vlan ' + vlanNum + ' en vPC de Peer Link')
comando = 'interface port-channel 3966' + ' ; ' + 'switchport trunk allowed vlan add ' + vlanName
ejecuta = configurar(comando, spineList)

print ('Agregando vlan ' + vlanNum + ' en vPC hacia Router')
comando = 'interface port-channel 10' + ' ; ' + 'switchport trunk allowed vlan add ' + vlanName
ejecuta = configurar(comando, spineList)

print ('Agregando vlan ' + vlanNum + ' en vPC hacia Leaf 0' + accesoLeaf)
comando = 'interface port-channel 1' + accesoLeaf + ' ; ' + 'switchport trunk allowed vlan add ' + vlanName
ejecuta = configurar(comando, spineList)

print ('Configurando vlan ' + vlanNum + ' en Leaf 0' + accesoLeaf)
comando = 'vlan ' + vlanNum + ' ; ' + 'name ' + vlanName
ejecuta = configurar(comando, [leafList[(int(accesoLeaf)-1)]])

print ('Configurando vlan ' + vlanNum + ' en Leaf 0' + accesoLeaf + ' hacia Spines')
comando = 'interface port-channel 1' + accesoLeaf + ' ; ' + 'switchport trunk allowed vlan add ' + vlanName
ejecuta = configurar(comando, [leafList[(int(accesoLeaf)-1)]])

#Falta agregar el puerto de acceso en leaf 

#https://developer.cisco.com/docs/cisco-nexus-9000-series-nx-api-cli-reference-release-9-2x/
#https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/programmability/guide/b_Cisco_Nexus_9000_Series_NX-OS_Programmability_Guide/b_Cisco_Nexus_9000_Series_NX-OS_Programmability_Configuration_Guide_chapter_0101.pdf
#https://github.com/DataKnox/CodeSamples/blob/master/Python/Networking/NX-API/nxapi.py
#https://github.com/DataKnox/CodeSamples/blob/master/Python/Networking/NX-API/NXAPI-RealWorld.py