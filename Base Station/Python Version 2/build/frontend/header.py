from datetime import datetime, timezone
from nicegui import ui


def buildHeader(globalData):
    # Main header
    with ui.header().classes('bg-gray-800 text-white px-4').style('height:70px'):
        with ui.row().classes('items-center justify-between w-full h-full'):
            # LEFT: Logo + Title
            with ui.row().classes('items-center gap-3'):
                logo_path = getattr(globalData, 'logo_image', '/static/logo.png')
                ui.image(logo_path).style('width:40px; height:40px; object-fit:contain;')
                label = globalData.app_name 
                ui.label(label).classes('text-lg font-bold')

            # RIGHT: Status + UTC
            with ui.row().classes('items-center gap-4 text-sm'):
                conn_label = ui.label('Conn: Online').classes('bg-green-500 px-2 py-1 rounded text-xs font-mono')
                uptime_label = ui.label('Uptime: 2d 03h').classes('bg-blue-500 px-2 py-1 rounded text-xs font-mono')
                utc_label = ui.label('UTC: --:--:--').classes('font-mono')

    # FIXED FAB (NO badge param - use props if needed)
    fab = ui.fab('menu', label='Controls').classes(
        'fixed top-20 right-4 z-[999] bg-blue-600 hover:bg-blue-700 text-white shadow-xl'
    ).props('size-xl rounded').tooltip('Navigation')

    with fab:
        ui.fab_action('dashboard', label='Dashboard', on_click=lambda: switchTab('dashboard'))
        ui.fab_action('sailing', label='USV Status', on_click=lambda: switchTab('status'))
        ui.fab_action('info', label='System Info', on_click=lambda: switchTab('info'))
        ui.fab_action('description', label='Logs', on_click=lambda: switchTab('logs'))
        ui.fab_action('settings', label='Settings', on_click=lambda: ui.open('/settings'))

    # Store references
    globalData.header_fab = fab
    globalData.header_labels = {'conn': conn_label, 'uptime': uptime_label, 'utc': utc_label}

    # Timers
    ui.timer(1.0, lambda: updateUtcTime(utc_label, globalData))
    ui.timer(5.0, lambda: updateStatus(conn_label, uptime_label, globalData))


def switchTab(tab_name):
    ui.notify(f'Switched to {tab_name}', type='positive')


def updateUtcTime(label, globalData):
    utc_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
    setattr(globalData, 'currentTimeUTC', utc_time)
    label.set_text(f'UTC: {utc_time}')


def updateStatus(conn_label, uptime_label, globalData):
    status = getattr(globalData, 'connection_status', 'Online')
    color = 'green' if 'Online' in status else 'red'
    conn_label.set_text(f'Conn: {status}')
    conn_label.classes(f'bg-{color}-500 px-2 py-1 rounded text-xs font-mono')
    uptime_label.set_text(f'Uptime: {getattr(globalData, "system_uptime", "2d 03h")}')
