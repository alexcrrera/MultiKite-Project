from nicegui import ui
import threading
import asyncio
import ais_backend

from layout import createLayout
from updater import updateMap
from track_line import initializeTrackDots


ui.query('body').classes('bg-black m-0 p-0 overflow-hidden')


(
    m,
    timeLabel,
    vesselCountLabel,
    lastUpdateLabel,
    vesselPanel,
    lastVesselPanel,
    vesselInfoLabel
) = createLayout()


ui.timer(
    2,
    lambda: updateMap(
        m,
        vesselCountLabel,
        vesselPanel,
        lastUpdateLabel,
        timeLabel,
        lastVesselPanel,
        vesselInfoLabel
    )
)


def startAisBackend():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ais_backend.main())


threading.Thread(target=startAisBackend, daemon=True).start()

initializeTrackDots(m)


ui.run(reload=False)