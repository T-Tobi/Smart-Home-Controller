# Smart-Home-Controller

A Flet-based interactive simulation of a modern smart home interface.

**Project Description**

This project is a fully interactive **Smart Home Controller** built using the **Flet** framework.
It simulates a modern home automation dashboard where the user can:

* Monitor device states
* Switch devices on or off
* Adjust smart appliances such as thermostats and fans
* Track power usage
* View detailed logs of user actions
* Inspect individual device information

The app features a clean, responsive UI styled with dark-mode colors, iconography, and modular control cards.
It is suitable for learning **GUI development**, **event handling**, **state management**, and **data visualization** in Python.

**Key Features**

**Overview Dashboard**

* Displays all smart home devices in categories:

  * Lights (3 rooms)
  * Doors (front & back)
  * Smart TV
  * Security Camera
  * Thermostat (temperature control)
  * Ceiling Fan (speed control)

**Real-Time Power Summary**

* Counts active devices
* Shows total number of devices
* Computes current power consumption dynamically

**Device Control Cards**

Each device has:

* Status display
* Context-aware action buttons
* Themed colors for ON/OFF states
* “Details” page with power rating and action history

**24-Hour Power Consumption Chart**

* Simulated energy usage for a full day
* Custom-built line/bar visualization using Flet containers
* Dynamic scaling based on peak power

**Action Log & Statistics View**

* Records every user action with timestamp
* Displays latest actions in a sortable table
* Separate tab for statistics and power graph

**Device Detail View**

Each device page includes:

* Device name, type, state, power rating
* Most recent actions
* Return button to main UI

**Slider-Controlled Devices**

* Thermostat: 15–30°C
* Fan: 0–3 speed levels with visual feedback


**Technologies Used**

* **Python 3**
* **Flet** (Flutter for Python)
* **Datetime** for logging
* **Random & math** for simulation data
