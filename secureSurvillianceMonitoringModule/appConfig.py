from jproperties import Properties

configs = Properties()
with open('appConfig.properties', 'rb') as configFile:
        configs.load(configFile)

def getAppConfig(key):
    #print(configs["MINING_NODE_ADDRESS"].data)
    #print(configs.get("MINING_NODE_ADDRESS").data)
    return configs.get(key).data
    

#print(getAppConfig("MINING_NODE_ADDRESS"))