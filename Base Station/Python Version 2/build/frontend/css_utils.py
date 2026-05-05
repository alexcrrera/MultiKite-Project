from nicegui import ui
# Global CSS

def add_global_css():
    ui.add_head_html("""
    <style>
    .leaflet-attribution-off .leaflet-control-attribution { 
        display: none !important; 
    }
    </style>
    """, shared=True)

    ui.add_head_html("""
    <style>
    html, body, #q-app, .q-page-container { height: 100vh !important; margin: 0; padding: 0; }
    .nicegui-main-container { height: 100vh !important; }
    </style>
    """, shared=True)
    # Your existing CSS...
    ui.add_head_html("""
    <style>
    .leaflet-attribution-off .leaflet-control-attribution { display: none !important; }
    html, body, #q-app, .q-page-container { height: 100vh !important; margin: 0; padding: 0; }
    .nicegui-main-container { height: 100vh !important; }
    </style>
    """, shared=True)

