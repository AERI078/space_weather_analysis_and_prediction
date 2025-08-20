import requests
import datetime
key = ""

cme = f"https://api.nasa.gov/DONKI/CME?startDate=2025-08-10&endDate=2025-08-13&api_key={key}"
cme_analysis= f"https://api.nasa.gov/DONKI/CMEAnalysis?startDate=2025-08-10&endDate=2025-08-13&mostAccurateOnly=true&speed=500&halfAngle=30&catalog=ALL&api_key={key}"

gme = f"https://api.nasa.gov/DONKI/GST?startDate=2025-08-10&endDate=2025-08-13&api_key={key}"

flr = f"https://api.nasa.gov/DONKI/FLR?startDate=2025-08-10&endDate=2025-08-13&api_key={key}"

ips = f"https://api.nasa.gov/DONKI/IPS?startDate=2025-08-10&endDate=2025-08-13&api_key={key}"
# location: default to ALL (choices: Earth, Mars, MESSENGER, STEREO A, STEREO B)
# catalog: default to ALL (choices: M2M_CATALOG, WINSLOW_MESSENGER_ICME_CATALOG)

hss = f"https://api.nasa.gov/DONKI/HSS?startDate=2016-01-01&endDate=2016-01-31&api_key={key}"