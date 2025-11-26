import flet as ft
from datetime import datetime
import random
import math

class SmartHomeController:
    def __init__(self):
        self.current_view = "overview"
        self.devices = {
            "light1": {"name": "Living Room Light", "type": "light", "status": "OFF", "power": 60},
            "light2": {"name": "Bedroom Light", "type": "light", "status": "OFF", "power": 40},
            "light3": {"name": "Kitchen Light", "type": "light", "status": "OFF", "power": 50},
            "door1": {"name": "Front Door", "type": "door", "status": "LOCKED", "power": 5},
            "door2": {"name": "Back Door", "type": "door", "status": "LOCKED", "power": 5},
            "thermostat1": {"name": "Thermostat", "type": "thermostat", "value": 22.0, "power": 200},
            "fan1": {"name": "Ceiling Fan", "type": "fan", "value": 0, "power": 0},
            "tv1": {"name": "Smart TV", "type": "tv", "status": "OFF", "power": 150},
            "camera1": {"name": "Security Camera", "type": "camera", "status": "OFF", "power": 10}
        }
        self.action_log = []
        self.power_data = self.generate_power_data()

    def add_action(self, device, action, user="User"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.action_log.insert(0, {
            "time": timestamp,
            "device": device,
            "action": action,
            "user": user
        })

    def generate_power_data(self):
        # Generate realistic power consumption data (24 hours)
        data = []
        for i in range(24):
            base = 100
            if 6 <= i <= 22:  # Daytime usage
                base = 200 + random.randint(-50, 50)
            else:  # Nighttime
                base = 80 + random.randint(-20, 20)
            data.append(base)
        return data

    def get_current_power(self):
        total = 0
        for device_id, device in self.devices.items():
            if device["type"] in ["light", "door", "tv", "camera"]:
                if device["status"] == "ON" or (device["type"] == "door" and device["status"] == "LOCKED"):
                    total += device["power"]
            elif device["type"] == "thermostat":
                total += device["power"]
            elif device["type"] == "fan":
                total += device["value"] * 50
        return total

def main(page: ft.Page):
    page.title = "Smart Home Controller + Simulator"
    page.padding = 0
    page.bgcolor = "#0A1929"
    
    controller = SmartHomeController()
    
    def update_summary():
        active_devices = sum(1 for d in controller.devices.values() 
                           if (d.get("status") == "ON" or d.get("status") == "UNLOCKED" or 
                               (d["type"] == "fan" and d.get("value", 0) > 0)))
        total_devices = len(controller.devices)
        current_power = controller.get_current_power()
        
        summary_active.value = f"{active_devices}"
        summary_total.value = f"{total_devices}"
        summary_power.value = f"{current_power}W"
        page.update()
    
    def toggle_light(device_id, status_text, button, card):
        def handler(e):
            device = controller.devices[device_id]
            if device["status"] == "OFF":
                device["status"] = "ON"
                controller.add_action(device_id, "Turn ON")
                status_text.value = "Status: ON"
                button.text = "Turn OFF"
                card.bgcolor = "#1E3A5F"
            else:
                device["status"] = "OFF"
                controller.add_action(device_id, "Turn OFF")
                status_text.value = "Status: OFF"
                button.text = "Turn ON"
                card.bgcolor = "#132F4C"
            update_summary()
            page.update()
        return handler
    
    def toggle_door(device_id, status_text, button, card):
        def handler(e):
            device = controller.devices[device_id]
            if device["status"] == "LOCKED":
                device["status"] = "UNLOCKED"
                controller.add_action(device_id, "Unlock")
                status_text.value = "Door: UNLOCKED"
                button.text = "Lock"
                card.bgcolor = "#2E1534"
            else:
                device["status"] = "LOCKED"
                controller.add_action(device_id, "Lock")
                status_text.value = "Door: LOCKED"
                button.text = "Unlock"
                card.bgcolor = "#132F4C"
            update_summary()
            page.update()
        return handler
    
    def toggle_tv(e):
        if controller.devices["tv1"]["status"] == "OFF":
            controller.devices["tv1"]["status"] = "ON"
            controller.add_action("tv1", "Turn ON")
            tv_status.value = "Status: ON"
            tv_button.text = "Turn OFF"
            tv_card.bgcolor = "#1E3A5F"
        else:
            controller.devices["tv1"]["status"] = "OFF"
            controller.add_action("tv1", "Turn OFF")
            tv_status.value = "Status: OFF"
            tv_button.text = "Turn ON"
            tv_card.bgcolor = "#132F4C"
        update_summary()
        page.update()
    
    def toggle_camera(e):
        if controller.devices["camera1"]["status"] == "OFF":
            controller.devices["camera1"]["status"] = "ON"
            controller.add_action("camera1", "Turn ON")
            camera_status.value = "Status: ON"
            camera_button.text = "Turn OFF"
            camera_card.bgcolor = "#1E3A5F"
        else:
            controller.devices["camera1"]["status"] = "OFF"
            controller.add_action("camera1", "Turn OFF")
            camera_status.value = "Status: OFF"
            camera_button.text = "Turn ON"
            camera_card.bgcolor = "#132F4C"
        update_summary()
        page.update()
    
    def change_temperature(e):
        controller.devices["thermostat1"]["value"] = e.control.value
        temp_value.value = f"Set point: {e.control.value:.1f} °C"
        controller.add_action("thermostat1", f"Set to {e.control.value:.1f}°C")
        update_summary()
        page.update()
    
    def change_fan_speed(e):
        controller.devices["fan1"]["value"] = int(e.control.value)
        fan_value.value = f"Fan speed: {int(e.control.value)}"
        controller.add_action("fan1", f"Set speed to {int(e.control.value)}")
        update_summary()
        page.update()
    
    def show_overview(e):
        controller.current_view = "overview"
        overview_tab.style.color = "#66B2FF"
        statistics_tab.style.color = "#B0BEC5"
        content_area.content = overview_content
        update_summary()
        page.update()
    
    def show_statistics(e):
        controller.current_view = "statistics"
        statistics_tab.style.color = "#66B2FF"
        overview_tab.style.color = "#B0BEC5"
        
        # Update action log table
        log_rows = []
        for action in controller.action_log[:10]:
            log_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(action["time"], size=12, color="#E0E0E0")),
                    ft.DataCell(ft.Text(action["device"], size=12, color="#E0E0E0")),
                    ft.DataCell(ft.Text(action["action"], size=12, color="#E0E0E0")),
                    ft.DataCell(ft.Text(action["user"], size=12, color="#E0E0E0")),
                ])
            )
        action_table.rows = log_rows
        
        content_area.content = statistics_content
        page.update()
    
    def show_device_details(device_id):
        def back_to_overview(e):
            show_overview(None)
        
        device = controller.devices[device_id]
        recent_actions = [a for a in controller.action_log if a["device"] == device_id][:5]
        
        details_view = ft.Container(
            content=ft.Column([
                ft.Text(f"{device['name']} details", size=32, weight=ft.FontWeight.BOLD, color="#66B2FF"),
                ft.Container(height=20),
                ft.Text(f"ID: {device_id}", size=16, color="#E0E0E0"),
                ft.Text(f"Type: {device['type']}", size=16, color="#E0E0E0"),
                ft.Text(f"State: {device['status'] if 'status' in device else device['value']}", size=16, color="#E0E0E0"),
                ft.Text(f"Power: {device['power']}W", size=16, color="#E0E0E0"),
                ft.Container(height=40),
                ft.Text("Recent actions", size=24, weight=ft.FontWeight.BOLD, color="#66B2FF"),
                ft.Container(height=10),
                ft.Column([
                    ft.Text(f"{action['time']} - {action['action']} ({action['user']})", color="#B0BEC5")
                    for action in recent_actions
                ] if recent_actions else [ft.Text("No recent actions", color="#78909C")]),
                ft.Container(height=20),
                ft.ElevatedButton("Back to overview", on_click=back_to_overview, bgcolor="#66B2FF", color="#0A1929")
            ], scroll=ft.ScrollMode.AUTO),
            padding=40,
            bgcolor="#132F4C",
            border_radius=10,
        )
        
        content_area.content = details_view
        page.update()
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.HOME, color="#66B2FF"),
            ft.Text("Smart Home Controller + Simulator", size=14, color="#B0BEC5"),
        ]),
        padding=10,
        bgcolor="#132F4C",
    )
    
    # Title and tabs
    title_bar = ft.Container(
        content=ft.Row([
            ft.Text("Smart Home Controller", size=24, weight=ft.FontWeight.BOLD, color="#66B2FF"),
            ft.Container(expand=True),
            overview_tab := ft.TextButton("Overview", on_click=show_overview, 
                                         style=ft.ButtonStyle(color="#66B2FF")),
            statistics_tab := ft.TextButton("Statistics", on_click=show_statistics,
                                           style=ft.ButtonStyle(color="#B0BEC5")),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(left=20, right=20, top=20, bottom=10),
        bgcolor="#132F4C",
    )
    
    # Summary cards
    summary_active = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color="#66B2FF")
    summary_total = ft.Text("9", size=32, weight=ft.FontWeight.BOLD, color="#66B2FF")
    summary_power = ft.Text("0W", size=32, weight=ft.FontWeight.BOLD, color="#66B2FF")
    
    summary_cards = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.POWER, color="#4CAF50", size=40),
                summary_active,
                ft.Text("Active Devices", size=12, color="#B0BEC5"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#132F4C",
            border_radius=10,
            width=150,
        ),
        ft.Container(width=10),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.DEVICES, color="#66B2FF", size=40),
                summary_total,
                ft.Text("Total Devices", size=12, color="#B0BEC5"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#132F4C",
            border_radius=10,
            width=150,
        ),
        ft.Container(width=10),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.BOLT, color="#FFA726", size=40),
                summary_power,
                ft.Text("Current Power", size=12, color="#B0BEC5"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#132F4C",
            border_radius=10,
            width=150,
        ),
    ], wrap=True)
    
    # Light cards
    light1_status = ft.Text("Status: OFF", size=14, color="#E0E0E0")
    light1_button = ft.TextButton("Turn ON", style=ft.ButtonStyle(color="#66B2FF"))
    light1_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color="#FFB74D"),
                ft.Text("Living Room Light", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            light1_status,
            ft.Text("Tap to switch the light.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("light1"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                light1_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    light1_button.on_click = toggle_light("light1", light1_status, light1_button, light1_card)
    
    light2_status = ft.Text("Status: OFF", size=14, color="#E0E0E0")
    light2_button = ft.TextButton("Turn ON", style=ft.ButtonStyle(color="#66B2FF"))
    light2_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color="#FFB74D"),
                ft.Text("Bedroom Light", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            light2_status,
            ft.Text("Tap to switch the light.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("light2"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                light2_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    light2_button.on_click = toggle_light("light2", light2_status, light2_button, light2_card)
    
    light3_status = ft.Text("Status: OFF", size=14, color="#E0E0E0")
    light3_button = ft.TextButton("Turn ON", style=ft.ButtonStyle(color="#66B2FF"))
    light3_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color="#FFB74D"),
                ft.Text("Kitchen Light", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            light3_status,
            ft.Text("Tap to switch the light.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("light3"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                light3_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    light3_button.on_click = toggle_light("light3", light3_status, light3_button, light3_card)
    
    # Door cards
    door1_status = ft.Text("Door: LOCKED", size=14, color="#E0E0E0")
    door1_button = ft.TextButton("Unlock", style=ft.ButtonStyle(color="#66B2FF"))
    door1_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.DOOR_FRONT_DOOR, color="#A1887F"),
                ft.Text("Front Door", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            door1_status,
            ft.Text("Tap to lock / unlock the door.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("door1"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                door1_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    door1_button.on_click = toggle_door("door1", door1_status, door1_button, door1_card)
    
    door2_status = ft.Text("Door: LOCKED", size=14, color="#E0E0E0")
    door2_button = ft.TextButton("Unlock", style=ft.ButtonStyle(color="#66B2FF"))
    door2_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.DOOR_BACK_DOOR, color="#A1887F"),
                ft.Text("Back Door", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            door2_status,
            ft.Text("Tap to lock / unlock the door.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("door2"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                door2_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    door2_button.on_click = toggle_door("door2", door2_status, door2_button, door2_card)
    
    # TV card
    tv_status = ft.Text("Status: OFF", size=14, color="#E0E0E0")
    tv_button = ft.TextButton("Turn ON", on_click=toggle_tv, style=ft.ButtonStyle(color="#66B2FF"))
    tv_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.TV, color="#64B5F6"),
                ft.Text("Smart TV", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            tv_status,
            ft.Text("Tap to switch the TV.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("tv1"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                tv_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    
    # Camera card
    camera_status = ft.Text("Status: OFF", size=14, color="#E0E0E0")
    camera_button = ft.TextButton("Turn ON", on_click=toggle_camera, style=ft.ButtonStyle(color="#66B2FF"))
    camera_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.CAMERA_ALT, color="#EF5350"),
                ft.Text("Security Camera", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            camera_status,
            ft.Text("Tap to switch the camera.", size=12, color="#B0BEC5"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("camera1"), style=ft.ButtonStyle(color="#66B2FF")),
                ft.Container(expand=True),
                camera_button,
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    
    # Thermostat card
    temp_value = ft.Text("Set point: 22.0 °C", size=14, color="#E0E0E0")
    thermostat_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.THERMOSTAT, color="#FF7043"),
                ft.Text("Thermostat", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            temp_value,
            ft.Text("Use slider to change temperature.", size=12, color="#B0BEC5"),
            ft.Slider(min=15, max=30, value=22, divisions=30, on_change=change_temperature, active_color="#FF7043"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("thermostat1"), style=ft.ButtonStyle(color="#66B2FF")),
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    
    # Fan card
    fan_value = ft.Text("Fan speed: 0", size=14, color="#E0E0E0")
    fan_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.AIR, color="#4DD0E1"),
                ft.Text("Ceiling Fan", size=18, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
            ]),
            fan_value,
            ft.Text("0 = OFF, 3 = MAX.", size=12, color="#B0BEC5"),
            ft.Slider(min=0, max=3, value=0, divisions=3, on_change=change_fan_speed, active_color="#4DD0E1"),
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: show_device_details("fan1"), style=ft.ButtonStyle(color="#66B2FF")),
            ]),
        ]),
        padding=20,
        bgcolor="#132F4C",
        border_radius=10,
        width=280,
    )
    
    # Overview content
    overview_content = ft.Container(
        content=ft.Column([
            summary_cards,
            ft.Container(height=20),
            ft.Text("On/Off devices", size=20, weight=ft.FontWeight.BOLD, color="#66B2FF"),
            ft.Container(height=10),
            ft.Row([light1_card, ft.Container(width=15), light2_card, ft.Container(width=15), light3_card], wrap=True),
            ft.Container(height=10),
            ft.Row([door1_card, ft.Container(width=15), door2_card, ft.Container(width=15), tv_card], wrap=True),
            ft.Container(height=10),
            ft.Row([camera_card], wrap=True),
            ft.Container(height=30),
            ft.Text("Slider controlled devices", size=20, weight=ft.FontWeight.BOLD, color="#66B2FF"),
            ft.Container(height=10),
            ft.Row([thermostat_card, ft.Container(width=15), fan_card], wrap=True),
        ], scroll=ft.ScrollMode.AUTO),
        padding=20,
        bgcolor="#0A1929",
    )
    
    # Create power consumption line chart
    def create_line_chart():
        max_power = max(controller.power_data)
        
        # Create line points
        points = []
        for i, value in enumerate(controller.power_data):
            x = 50 + (i * 26)
            y = 240 - (value / max_power * 200)
            points.append(f"{x},{y}")
        
        line_path = " ".join(points)
        
        chart_container = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Stack([
                        # Grid lines
                        ft.Column([
                            ft.Container(height=1, bgcolor="#1E3A5F", width=650),
                            ft.Container(height=48),
                            ft.Container(height=1, bgcolor="#1E3A5F", width=650),
                            ft.Container(height=48),
                            ft.Container(height=1, bgcolor="#1E3A5F", width=650),
                            ft.Container(height=48),
                            ft.Container(height=1, bgcolor="#1E3A5F", width=650),
                            ft.Container(height=48),
                            ft.Container(height=1, bgcolor="#1E3A5F", width=650),
                        ]),
                        # Y-axis labels
                        ft.Row([
                            ft.Column([
                                ft.Text(f"{int(max_power)}W", size=10, color="#B0BEC5"),
                                ft.Container(height=35),
                                ft.Text(f"{int(max_power*0.75)}W", size=10, color="#B0BEC5"),
                                ft.Container(height=35),
                                ft.Text(f"{int(max_power*0.5)}W", size=10, color="#B0BEC5"),
                                ft.Container(height=35),
                                ft.Text(f"{int(max_power*0.25)}W", size=10, color="#B0BEC5"),
                                ft.Container(height=35),
                                ft.Text("0W", size=10, color="#B0BEC5"),
                            ]),
                            ft.Container(width=10),
                            # Line chart using containers
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Container(expand=True),
                                            ft.Container(
                                                height=max(2, (value / max_power) * 200),
                                                width=2,
                                                bgcolor="#66B2FF",
                                                border_radius=1,
                                            ),
                                        ]),
                                        expand=True,
                                    )
                                    for value in controller.power_data
                                ], spacing=24),
                                width=630,
                                height=240,
                            ),
                        ]),
                    ]),
                    height=250,
                    padding=10,
                ),
                ft.Container(height=10),
                ft.Row([
                    ft.Container(width=40),
                    ft.Text("0h", size=10, color="#B0BEC5"),
                    ft.Container(expand=True),
                    ft.Text("6h", size=10, color="#B0BEC5"),
                    ft.Container(expand=True),
                    ft.Text("12h", size=10, color="#B0BEC5"),
                    ft.Container(expand=True),
                    ft.Text("18h", size=10, color="#B0BEC5"),
                    ft.Container(expand=True),
                    ft.Text("24h", size=10, color="#B0BEC5"),
                ], width=700),
            ]),
            padding=20,
            bgcolor="#132F4C",
            border_radius=10,
        )
        return chart_container
    
    # Statistics content
    action_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Time", weight=ft.FontWeight.BOLD, color="#66B2FF")),
            ft.DataColumn(ft.Text("Device", weight=ft.FontWeight.BOLD, color="#66B2FF")),
            ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.BOLD, color="#66B2FF")),
            ft.DataColumn(ft.Text("User", weight=ft.FontWeight.BOLD, color="#66B2FF")),
        ],
        rows=[],
        border=ft.border.all(1, "#1E3A5F"),
        border_radius=10,
        heading_row_color="#1E3A5F",
    )
    
    statistics_content = ft.Container(
        content=ft.Column([
            ft.Text("Power consumption (simulated)", size=20, weight=ft.FontWeight.BOLD, color="#66B2FF"),
            ft.Container(height=10),
            create_line_chart(),
            ft.Container(height=30),
            ft.Text("Action log", size=20, weight=ft.FontWeight.BOLD, color="#66B2FF"),
            ft.Container(height=10),
            ft.Container(
                content=action_table,
                bgcolor="#132F4C",
                padding=10,
                border_radius=10,
            ),
        ], scroll=ft.ScrollMode.AUTO),
        padding=20,
        bgcolor="#0A1929",
    )
    
    # Main content area
    content_area = ft.Container(
        content=overview_content,
        expand=True,
    )
    
    # Main layout
    page.add(
        ft.Column([
            header,
            title_bar,
            content_area,
        ], expand=True, spacing=0)
    )
    
    update_summary()

ft.app(target=main)