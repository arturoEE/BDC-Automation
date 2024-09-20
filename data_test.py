import Saleae.saleae_utils as saleae_utils

data = SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Results", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 10)

data.loadData()
data.convertDataToHex()
print(data.dataHEX)
data = SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Results\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 10)
data.loadData()
data.convertDataToHex()
print(data.dataHEX)
print(data.readHexAtFirstTriggerEdge())
data.readHexAtTriggerEdges()
print(data.synchronousDataHex)