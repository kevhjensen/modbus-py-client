EVSE_COIL_ADDR_SAVE_CONFIG = 0
EVSE_COIL_ADDR_REBOOT = 1

CONNECTOR_COIL_ADDR_START = 0
CONNECTOR_COIL_ADDR_STOP = 1

EVSE_REG_ADDR_MODEL_NAME = 0
EVSE_REG_ADDR_SN = 32
EVSE_REG_ADDR_LOGIN_PASSWORD = 64
EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L1 = 96
EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L2 = 98
EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L3 = 100
EVSE_REG_ADDR_DC_PUT_VOLTAGE = 102
EVSE_REG_ADDR_AUTH_MODE = 564
EVSE_REG_ADDR_AUTH_EVCCID = 565
EVSE_REG_ADDR_MAX_ENERGY = 566
EVSE_REG_ADDR_MAX_POWER = 567
EVSE_REG_ADDR_MAX_CURRENT = 568
EVSE_REG_ADDR_MAX_DURATION = 569
EVSE_REG_ADDR_RFID_ENDIAN = 570
EVSE_REG_ADDR_15118_ENABLE = 571
EVSE_REG_ADDR_15118_PNC = 572

CONNECTOR_REG_ADDR_SYSTEM_STATE = 0
CONNECTOR_REG_ADDR_PLUG_STATUS = 1
CONNECTOR_REG_ADDR_PRESENT_SOC = 2
CONNECTOR_REG_ADDR_PRESENT_POWER = 3
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_DC = 5
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L1 = 7
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L2 = 9
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L3 = 11
CONNECTOR_REG_ADDR_PRESENT_CURRENT_DC = 13
CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L1 = 15
CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L2 = 17
CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L3 = 19
CONNECTOR_REG_ADDR_CHARGED_ENERGY = 21
CONNECTOR_REG_ADDR_CHARGED_DURATION = 25
CONNECTOR_REG_ADDR_PRESENT_REMAIN_TIME = 27
CONNECTOR_REG_ADDR_PRESENT_IDTAG = 29
CONNECTOR_REG_ADDR_STATUS_CODE = 50


CONNECTOR_SYSTEM_STATE_MAP = {
    0: "Booting",
    1: "Idle",
    2: "Authorizing",
    5: "Preparing",
    8: "Charging",
    9: "Terminating",
    10: "Complete",
    11: "Alarm",
    13: "Reservation",
    15: "Maintain",
    19: "Upgrade"
}