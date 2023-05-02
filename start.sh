gnome-terminal --tab -- bash -ic "cd secureSurvillianceBlockChainModule; python MainNodeServer.py; exec bash"
gnome-terminal --tab -- bash -ic "cd secureSurvillianceMonitoringModule; python MainMonitoring.py; exec bash"
gnome-terminal --tab -- bash -ic "cd secureSurvillianceFaceRecognitionModule; python MainFaceRecognition.py; exec bash"
