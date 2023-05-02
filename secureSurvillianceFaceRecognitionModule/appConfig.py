from jproperties import Properties

configs = Properties()
with open('appConfig.properties', 'rb') as configFile:
        configs.load(configFile)

def getAppConfig(key):
    #print(configs["MINING_NODE_ADDRESS"].data)
    #print(configs.get("MINING_NODE_ADDRESS").data)
    return configs.get(key).data
    

#print(getAppConfig("MINING_NODE_ADDRESS"))



# def getAppConfig(key):
#     #print(configs["MINING_NODE_ADDRESS"].data)
#     #print(configs.get("MINING_NODE_ADDRESS").data)
#     ip_address=""
#     if(configs.get(key).data=="LOCAL_MACHINE"):        
#         ## getting the hostname by socket.gethostname() method
#         hostname = socket.gethostname()
#         ## getting the IP address using socket.gethostbyname() method
#         ip_address = socket.gethostbyname(hostname)
#         print(f"Hostname: {hostname}")
#         print(f"IP Address: {ip_address}")