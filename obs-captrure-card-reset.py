from asyncio.windows_events import NULL
import obspython as obs
from pygrabber.dshow_graph import FilterGraph
from time import sleep
from threading import Thread

inputName = ""
sourceName = ""
resolutionName = ""
enableFlag = False
resolutionFlag = False

def script_description():
    return "This script automatically resets the capture card when the resolution is changed."

def script_properties():
    props = obs.obs_properties_create()
    enable = obs.obs_properties_add_bool(props,"enable","Enable")
    obs.obs_property_set_modified_callback(enable, callbackEnable)

    inputList = obs.obs_properties_add_list(props, "inputList", "Input device", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    inputDevices = getInputDevices()
    for device in inputDevices:
        obs.obs_property_list_add_string(inputList, device, device)
    obs.source_list_release(inputDevices)

    sourceList = obs.obs_properties_add_list(props, "sourceList", "Source", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(props,"resolution","On-screen resolution \n (Add a GDI+ text source to use)")
    resolutionList = obs.obs_properties_add_list(props, "resolutionList", "Text source", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    for source in sources:
        name = obs.obs_source_get_name(source)
        if (obs.obs_source_get_id(source) == "dshow_input"):
            obs.obs_property_list_add_string(sourceList, name, name)
        if (obs.obs_source_get_id(source) == "text_gdiplus_v2"):
            obs.obs_property_list_add_string(resolutionList, name, name)
    obs.source_list_release(sources)

    return props

def script_update(settings):
    global inputName
    global sourceName
    global resolutionName
    global enableFlag
    global resolutionFlag
    inputName = obs.obs_data_get_string(settings, "inputList")
    sourceName = obs.obs_data_get_string(settings, "sourceList")
    resolutionName = obs.obs_data_get_string(settings, "resolutionList")
    enableFlag = obs.obs_data_get_bool(settings, "enable")
    resolutionFlag = obs.obs_data_get_bool(settings, "resolution")
    # printResolution("")

def script_load(settings):
    print("Script loaded")
    callbackEnable(NULL, NULL, settings)

def script_unload():
    global enableFlag
    global resolutionFlag
    enableFlag = False
    resolutionFlag = False
    printResolution("")
    print("Script unloaded")

def callbackEnable(props, prop, settings):
    global enableFlag
    if (obs.obs_data_get_bool(settings, "enable")):
        enableFlag = True
        th1 = Thread(target=main)
        th1.daemon = True
        th1.start()
    else:
        enableFlag = False

def getInputDevices():
    graph = FilterGraph()
    inputDevices = graph.get_input_devices()
    # print(*inputDevices, sep='\n')
    return inputDevices

def resolutionCheck():
    try:
        graph = FilterGraph()
        inputDevices = graph.get_input_devices()
        cardIndex = inputDevices.index(inputName)
        graph.add_video_input_device(cardIndex)
        return graph.get_input_device().get_current_format()
    except:
        return 0

def cardReset():
    source = obs.obs_get_source_by_name(sourceName)
    settings = obs.obs_data_create()
    obs.obs_source_update(source, settings)
    obs.obs_source_release(source)
    obs.obs_data_release(settings)

def printResolution(res):
    try:
        source = obs.obs_get_source_by_name(resolutionName)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", res)
        obs.obs_source_update(source, settings)
        obs.obs_source_release(source)
        obs.obs_data_release(settings)
    except:
        pass

def main():
    global enableFlag
    res1 = resolutionCheck()
    print("Current resolution: ", res1)
    
    while(enableFlag):
        sleep(0.5)
        res2 = resolutionCheck()
        if (res2 != 0):
            if (res1 != res2):
                cardReset()
                res1 = res2
                print("Current resolution: ", res1)
                if (resolutionFlag):
                    printResolution(str(res1[0]) + 'x' + str(res1[1]))
                    sleep(2)
                    printResolution("")
                