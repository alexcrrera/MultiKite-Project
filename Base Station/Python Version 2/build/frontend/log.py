


from nicegui import ui
def buildLog(globalData):
    
    log = ui.log(max_lines=10).classes('w-full h-20')
    
    ui.button('Log time', on_click=lambda: log.push(logMessage(globalData)))

def logMessage(globalData):
    v = globalData.vessels[-1] if globalData.vessels else {}
    print("Logging time for vessel:", v.get("name", "N/A"))
    print("vessels:", globalData.vessels)
    name = v.get("name") or "Unknown vessel"
    return f"[{name}] Time logged"