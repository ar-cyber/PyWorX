# PyWorX
A Raspberry Pi-deployable script to create the Interlogix NetworX infastructure with Python and JS.<br><br>
## THIS IS WORK IN PROGRESS AND SOME FEATURES DO NOT WORK.


## Installation
1. Install dependecies:
```bash
pip install -r requirements.txt
```

## Configuration
This is the sample JSON config with comments:
```jsonc
// The PyWorX supports up to 16 zones.

/* READ THIS BEFORE CONTINUING 

- NO DEVICES CAN BE CONNECTED TO GPIO 15 OR 16; THIS IS FOR CODEPAD UART
- EACH CODEPAD NEEDS TO BE DEPLOYED WITH THE CODEPAD SOFTWARE ON THE REPO; IT CAN RUN ON ANY DEVICE SUPPORTING REST APIS OR UART
*/
{
    "name": "Mypanel",
    "timeout" 15, // default timeout interval
    "zones": [

        /* Available values for 'type'
        
        - 'none' for no input connected
        - 'switch' for momentary input (e.g. PIR, reed switch etc.)
        - 'latch' for toggle switches
        */
        {
            "zone": 1, // make sure you change this number when you add more zones
            "pin": 4, // GPIO pin
            "type": "none",
            "flags": [
                /* The following flags may be added:
                'fire': fire zone. MUST HAVE LATCH AS THE TYPE
                'instant': sounds the alarm if tripped no matter what
                'handover': triggers the alarm if tripped before any entryexit zone. 
                'partial': not secured in stay/partial mode. May be triggered without alarm going off.
                'entryexit': does not trigger the alarm until the set entry time is up 
                'forced_arming': NOT COMPATIBLE WITH INSTANT. Can be armed whilst the zone is tripped.
                
                The default flags are partial and entryexit. IF ENTRYEXIT IS NOT SPECIFIED THEN INSTANT MUST BE SPECIFIED AND VICE VERSA.
                */
                "partial",
                "entryexit"
            ]
        }
        
    ],
    "inputs": [
        /*
        Input 1 must be type siren on pin 3

        Available types:
        - 'momentary': monentary keyswitch
        - 'siren': siren
        - 'toggle': toggleable input
        */
        {
            "type": "siren",
            "pin": "3"
        }
    ],
    "codepads": [
        /* Codepads communicate through internet connectivity using UART or a REST endpoint. 
        
        ONE CODEPAD MUST BE CONNECTED TO ENSURE PROPER FUNCTION*/
        {
            "id": "1", // This is either the IP address of the codepad or a special address generated on the codepad for uart. This MUST be a string.
            "type": "rest" // Must be either `ser` or `rest`
        }
    ]
}
```