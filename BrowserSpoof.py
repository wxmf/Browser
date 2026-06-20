# by dopa @22gs


import os, time, random, socket, threading, json, tempfile, pathlib, shutil, sys
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.rule import Rule
    from rich import box
except ImportError:
    os.system("pip install rich --break-system-packages -q")
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.rule import Rule
    from rich import box
# by dopa @22gs
try:
    from pypresence import Presence
    RPC_OK = True
except ImportError:
    RPC_OK = False

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    SELENIUM_OK = True
except ImportError:
    SELENIUM_OK = False

console  = Console(highlight=False)
HOSTNAME = socket.gethostname()

CLIENT_ID = "1506767738499109014"
IMAGE_KEY  = "51c357e62a551d6af553635bcb8948a3"
rpc        = None

FIRST_NAMES = ["Anis","Oliver","Liam","Noa","mohaa","Ethan","luca","Mason","Logan","Elijah","Aiden","Jack","Sebastian","Michael","Owen","Daniel","Carter","Wyatt","Julian","Levi","Emma","Olivia","Ava","Sophia","Isabella","Mia","Charlotte","Amelia","Harper","Evelyn","Abigail","Emily","Ella","Elizabeth","Sofia","Madison","Avery","Luna","Chloe","Penelope"]
LAST_NAMES  = ["Smiti","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Moore","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Phillips","Evans","Turnuo"]

LOCATIONS = {
    "1": {"label": "United States",  "flag": "US", "timezone": "America/New_York", "locale": "en-US", "lat":  40.7128, "lon":  -74.0060},
    "2": {"label": "Germany",        "flag": "DE", "timezone": "Europe/Berlin",    "locale": "de-DE", "lat":  52.5200, "lon":   13.4050},
    "3": {"label": "France",         "flag": "FR", "timezone": "Europe/Paris",     "locale": "fr-FR", "lat":  48.8566, "lon":    2.3522},
    "4": {"label": "United Kingdom", "flag": "GB", "timezone": "Europe/London",    "locale": "en-GB", "lat":  51.5074, "lon":   -0.1278},
    "5": {"label": "Japan",          "flag": "JP", "timezone": "Asia/Tokyo",       "locale": "ja-JP", "lat":  35.6762, "lon":  139.6503},
    "6": {"label": "Canada",         "flag": "CA", "timezone": "America/Toronto",  "locale": "en-CA", "lat":  43.6532, "lon":  -79.3832},
    "7": {"label": "Australia",      "flag": "AU", "timezone": "Australia/Sydney", "locale": "en-AU", "lat": -33.8688, "lon":  151.2093},
    "8": {"label": "Netherlands",    "flag": "NL", "timezone": "Europe/Amsterdam", "locale": "nl-NL", "lat":  52.3676, "lon":    4.9041},
}

USER_AGENTS = {
    "Chrome Windows":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Chrome macOS":    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Chrome Linux":    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Firefox Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Firefox macOS":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Safari macOS":    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Edge Windows":    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "iPhone Safari":   "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Android Chrome":  "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
}

RESOLUTIONS = {
    "1": {"label": "Default",            "w": None, "h": None},
    "2": {"label": "1920x1080  FHD",     "w": 1920, "h": 1080},
    "3": {"label": "1280x720   HD",      "w": 1280, "h": 720},
    "4": {"label": "2560x1440  QHD",     "w": 2560, "h": 1440},
    "5": {"label": "390x844    iPhone",  "w": 390,  "h": 844},
    "6": {"label": "412x915    Android", "w": 412,  "h": 915},
    "7": {"label": "768x1024   iPad",    "w": 768,  "h": 1024},
}

THEMES = {
    "1": "default",
    "2": "dark",
    "3": "light",
}

BROWSER_TYPES = {
    "1": {"label": "Chrome", "driver": "chrome"},
    "2": {"label": "Firefox", "driver": "firefox"},
    "3": {"label": "Edge", "driver": "edge"},
}
# by dopa @22gs
state = {
    "location":      LOCATIONS["1"],
    "proxy":         None,
    "proxy_type":    "http",
    "ua":            None,
    "ua_label":      "default",
    "webrtc":        True,
    "resolution":    None,
    "res_label":     "Default",
    "theme":         "default",
    "browser_type":  "chrome",
    "browser_label": "Chrome",
    "headless":      False,
    "incognito":     False,
    "extension_path": None,
}

try:
    import pyfiglet
    ASCII_LINES = pyfiglet.figlet_format("BROWSER", font="slant").split("\n")
except ImportError:
    ASCII_LINES = ["  BROWSER "]

PRESETS_FILE = pathlib.Path(__file__).parent / "presets.json"

                  

def presets_load_all() -> dict:
    if PRESETS_FILE.exists():
        try:
            return json.loads(PRESETS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def presets_save_all(data: dict):
    PRESETS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
# by dopa @22gs
def state_to_preset() -> dict:
    return {
        "location_label": state["location"]["label"],
        "proxy":          state["proxy"],
        "proxy_type":     state["proxy_type"],
        "ua":             state["ua"],
        "ua_label":       state["ua_label"],
        "webrtc":         state["webrtc"],
        "resolution":     list(state["resolution"]) if state["resolution"] else None,
        "res_label":      state["res_label"],
        "theme":          state["theme"],
        "browser_type":   state["browser_type"],
        "browser_label":  state["browser_label"],
        "headless":       state["headless"],
        "incognito":      state["incognito"],
        "extension_path": state["extension_path"],
    }

def preset_to_state(p: dict):
    loc = next((v for v in LOCATIONS.values() if v["label"] == p.get("location_label")), LOCATIONS["1"])
    state["location"]       = loc
    state["proxy"]          = p.get("proxy")
    state["proxy_type"]     = p.get("proxy_type", "http")
    state["ua"]             = p.get("ua")
    state["ua_label"]       = p.get("ua_label", "default")
    state["webrtc"]         = p.get("webrtc", True)
    res = p.get("resolution")
    state["resolution"]     = tuple(res) if res else None
    state["res_label"]      = p.get("res_label", "Default")
    state["theme"]          = p.get("theme", "default")
    state["browser_type"]   = p.get("browser_type", "chrome")
    state["browser_label"]  = p.get("browser_label", "Chrome")
    state["headless"]       = p.get("headless", False)
    state["incognito"]      = p.get("incognito", False)
    state["extension_path"] = p.get("extension_path")

def draw_presets():
    rpc_update(details="Presets", state_text="Managing presets")
    while True:
        clear()
        console.print(Rule(Text("Presets", style="bold white"), style="dim white"))
        console.print()

        presets = presets_load_all()

        for num, label in [("1", "Save current config as preset"),
                           ("2", "Load a preset"),
                           ("3", "Delete a preset"),
                           ("4", "Back")]:
            t = Text()
            t.append(f"  [ {num} ]  ", "bold white")
            t.append(label, "white")
            console.print(t)
# by dopa @22gs
        if presets:
            console.print()
            console.print(Text(f"  {len(presets)} preset(s) saved", "dim white"))

        choice = prompt("presets")

             
        if choice == "1":
            console.print()
            name = console.input(Text("  preset name → ", "dim white")).strip()
            if not name:
                console.print(Text("\n  name vide, annulé.", "red"))
                time.sleep(0.8)
                continue
            presets = presets_load_all()
            presets[name] = state_to_preset()
            presets_save_all(presets)
            console.print(Text(f"\n  preset '{name}' sauvegardé.", "dim white"))
            time.sleep(1)

        
        elif choice == "2":
            presets = presets_load_all()
            if not presets:
                console.print(Text("\n  aucun preset.", "red"))
                time.sleep(0.8)
                continue
            clear()
            console.print(Rule(Text("Load Preset", style="bold white"), style="dim white"))
            console.print()
            keys = list(presets.keys())
            for i, pname in enumerate(keys, 1):
                p = presets[pname]
                t = Text()
                t.append(f"  [ {i} ]  ", "bold white")
                t.append(pname, "white")
                t.append("  —  ", "dim white")
                t.append(p.get("location_label", "?"), "dim white")
                t.append(" / ", "dim white")
                t.append(p.get("browser_label", "?"), "dim white")
                if p.get("proxy"):
                    t.append("  proxy", "cyan")
                console.print(t)
            pick = prompt("load")
            if pick.isdigit() and 1 <= int(pick) <= len(keys):
                preset_to_state(presets[keys[int(pick)-1]])
                console.print(Text(f"\n  preset '{keys[int(pick)-1]}' chargé.", "dim white"))
                time.sleep(1)

                      
        elif choice == "3":
            presets = presets_load_all()
            if not presets:
                console.print(Text("\n  aucun preset.", "red"))
                time.sleep(0.8)
                continue
            clear()
            console.print(Rule(Text("Delete Preset", style="bold white"), style="dim white"))
            console.print()
            keys = list(presets.keys())
            for i, pname in enumerate(keys, 1):
                t = Text()
                t.append(f"  [ {i} ]  ", "bold white")
                t.append(pname, "white")
                console.print(t)
            pick = prompt("delete")
            if pick.isdigit() and 1 <= int(pick) <= len(keys):
                deleted = keys[int(pick)-1]
                del presets[deleted]
                presets_save_all(presets)
                console.print(Text(f"\n  preset '{deleted}' supprimé.", "dim white"))
                time.sleep(1)

        elif choice in ("4", "q", "back"):
            break

                                                                                

def rpc_connect():
    global rpc
    if not RPC_OK:
        return
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
    except Exception:
        rpc = None

def rpc_update(details="Browser", state_text="Idle"):
    if not rpc:
        return
    try:
        rpc.update(details=details, state=state_text,
                   large_image=IMAGE_KEY, large_text="Browser",
                   start=int(time.time()))
    except Exception:
        pass

def rpc_close():
    if not rpc:
        return
    try:
        rpc.close()
    except Exception:
        pass

                                                                                

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def ts():
    return datetime.now().strftime("%H:%M:%S")

def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def prompt(label=""):
    console.print()
    t = Text()
    t.append("┌──(", "dim white")
    t.append("root", "bold white")
    t.append("@", "dim white")
    t.append(HOSTNAME, "bold cyan")
    t.append(")-[", "dim white")
    t.append(label, "white")
    t.append("]", "dim white")
    console.print(t)
    t2 = Text()
    t2.append("└─", "dim white")
    t2.append("$ ", "bold white")
    return console.input(t2).strip()

def animate_ascii():
    for line in ASCII_LINES:
        console.print(Text(line, style="bold white"))
        time.sleep(0.04)

                                                                                

def draw_main():
    rpc_update(details="Browser", state_text="in main menu")
    clear()
    animate_ascii()
    console.print(Rule(style="dim white"))
    console.print()

    loc = state["location"]
    prx = f"{state['proxy_type']}://{state['proxy']}" if state["proxy"] else "none"

    content = Text()
    content.append("  location    ", "dim white"); content.append(f"{loc['flag']}  {loc['label']}\n", "white")
    content.append("  browser     ", "dim white"); content.append(f"{state['browser_label']}\n", "cyan" if state["browser_type"] != "chrome" else "dim white")
    content.append("  headless    ", "dim white"); content.append(f"{'enabled' if state['headless'] else 'disabled'}\n", "cyan" if state["headless"] else "dim white")
    content.append("  incognito   ", "dim white"); content.append(f"{'enabled' if state['incognito'] else 'disabled'}\n", "cyan" if state['incognito'] else "dim white")
    content.append("  proxy       ", "dim white"); content.append(f"{prx}\n", "cyan" if state["proxy"] else "dim white")
    content.append("  agent       ", "dim white"); content.append(f"{state['ua_label']}\n", "cyan" if state["ua"] else "dim white")
    content.append("  resolution  ", "dim white"); content.append(f"{state['res_label']}\n", "cyan" if state["resolution"] else "dim white")
    content.append("  webrtc      ", "dim white"); content.append("blocked\n" if state["webrtc"] else "enabled\n", "cyan" if state["webrtc"] else "dim white")
    content.append("  theme       ", "dim white"); content.append(f"{state['theme']}\n", "cyan" if state["theme"] != "default" else "dim white")
    content.append("  time        ", "dim white"); content.append(ts(), "white")
    console.print(Panel(content, box=box.ROUNDED, border_style="dim white", padding=(0, 1)))
    console.print()
# by dopa @22gs
    for num, label in [("1","Launch browser"),("2","Location"),("3","User agent"),("4","Proxy"),("5","Browser settings"),("6","Presets"),("7","Exit")]:
        t = Text()
        t.append(f"  [ {num} ]  ", "bold white")
        t.append(label, "white")
        console.print(t)

                         
    buf = ""
    while True:
        t2 = Text()
        t2.append("\n┌──(", "dim white"); t2.append("root", "bold white")
        t2.append("@", "dim white");      t2.append(HOSTNAME, "bold cyan")
        t2.append(")-[", "dim white");    t2.append("main", "white")
        t2.append("]  ", "dim white");    t2.append(ts(), "dim white")
        console.print(t2)
        p = Text()
        p.append("└─", "dim white"); p.append("$ ", "bold white"); p.append(buf, "white")
        console.print(p, end="")

        if os.name == "nt":
            import msvcrt
            deadline = time.time() + 1
            while time.time() < deadline:
                if msvcrt.kbhit():
                    ch = msvcrt.getwche()
                    if ch in ("\r", "\n"):
                        console.print()
                        return buf.strip()
                    elif ch == "\x08":
                        buf = buf[:-1]
                    else:
                        buf += ch
                    break
                time.sleep(0.05)
            sys.stdout.write("\x1b[2A")
            sys.stdout.flush()
        else:
            import select
            rlist, _, _ = select.select([sys.stdin], [], [], 1)
            if rlist:
                return sys.stdin.readline().rstrip("\n").strip()
            sys.stdout.write("\x1b[2A")
            sys.stdout.flush()

                                                                                

def draw_location():
    rpc_update(details="Selecting Location", state_text="Browsing countries")
    clear()
    console.print(Rule(Text("Location", style="bold white"), style="dim white"))
    console.print()
    for num, loc in LOCATIONS.items():
        active = loc["label"] == state["location"]["label"]
        t = Text()
        t.append("  > " if active else "    ", "bold cyan" if active else "white")
        t.append(f"[ {num} ]  ", "bold white")
        t.append(f"{loc['flag']}  {loc['label']}", "white")
        console.print(t)
    choice = prompt("location")
    if choice in LOCATIONS:
        state["location"] = LOCATIONS[choice]

                                                                                

def draw_ua():
    rpc_update(details="Changing User Agent", state_text="Picking browser identity")
    clear()
    console.print(Rule(Text("User Agent", style="bold white"), style="dim white"))
    console.print()
    for num, label in [("1","Random"),("2","Choose from list"),("3","Type custom"),("4","Reset to default")]:
        t = Text()
        t.append(f"  [ {num} ]  ", "bold white")
        t.append(label, "white")
        console.print(t)
    choice = prompt("user-agent")

    if choice == "1":
        label, ua = random.choice(list(USER_AGENTS.items()))
        state["ua"] = ua
        state["ua_label"] = f"random ({label})"
        console.print(Text(f"\n  set → {label}", "dim white"))
        time.sleep(1)

    elif choice == "2":
        console.print()
        keys = list(USER_AGENTS.keys())
        for i, name in enumerate(keys, 1):
            active = USER_AGENTS[name] == state["ua"]
            t = Text()
            t.append("  > " if active else "    ", "bold cyan" if active else "white")
            t.append(f"[ {i} ]  ", "bold white")
            t.append(name, "white")
            console.print(t)
        pick = prompt("select")
        if pick.isdigit() and 1 <= int(pick) <= len(keys):
            label = keys[int(pick)-1]
            state["ua"] = USER_AGENTS[label]
            state["ua_label"] = label
            console.print(Text(f"\n  set → {label}", "dim white"))
            time.sleep(1)
# by dopa @22gs
    elif choice == "3":
        console.print()
        custom = console.input(Text("  paste agent → ", "dim white")).strip()
        if custom:
            state["ua"] = custom
            state["ua_label"] = "custom"
            console.print(Text("\n  set → custom", "dim white"))
            time.sleep(1)

    elif choice == "4":
        state["ua"] = None
        state["ua_label"] = "default"
        console.print(Text("\n  reset to default.", "dim white"))
        time.sleep(1)

                                                                                

def draw_proxy():
    rpc_update(details="Configuring Proxy", state_text="Setting up connection")
    clear()
    console.print(Rule(Text("Proxy", style="bold white"), style="dim white"))
    console.print()
    current = f"{state['proxy_type']}://{state['proxy']}" if state["proxy"] else "none"
    console.print(Text(f"  current → {current}\n", "dim white"))
    for num, label in [("1","HTTP"),("2","SOCKS5"),("3","Clear proxy")]:
        t = Text()
        t.append(f"  [ {num} ]  ", "bold white")
        t.append(label, "white")
        console.print(t)
    ptype = prompt("proxy")

    if ptype == "3":
        state["proxy"] = None
        console.print(Text("\n  proxy cleared.", "dim white"))
        time.sleep(1)
        return

    state["proxy_type"] = "socks5" if ptype == "2" else "http"
    console.print()
    addr = console.input(Text("  host:port → ", "dim white")).strip()
    if addr:
        state["proxy"] = addr
        console.print(Text(f"\n  set → {state['proxy_type']}://{addr}", "dim white"))
    else:
        state["proxy"] = None
        console.print(Text("\n  proxy cleared.", "dim white"))
    time.sleep(1)

                                                                                

def draw_browser_settings():
    rpc_update(details="Browser Settings", state_text="Customizing browser")
    while True:
        clear()
        console.print(Rule(Text("Browser Settings", style="bold white"), style="dim white"))
        console.print()

        rows = [
            ("1", "WebRTC         ", "blocked" if state["webrtc"] else "enabled",  state["webrtc"]),
            ("2", "Resolution     ", state["res_label"],                            state["resolution"] is not None),
            ("3", "Theme          ", state["theme"],                                state["theme"] != "default"),
            ("4", "Browser Type   ", state["browser_label"],                        state["browser_type"] != "chrome"),
            ("5", "Headless       ", "enabled" if state["headless"] else "disabled", state["headless"]),
            ("6", "Incognito      ", "enabled" if state["incognito"] else "disabled", state["incognito"]),
            ("7", "Extension      ", state["extension_path"] if state["extension_path"] else "none", state["extension_path"] is not None),
        ]
        for num, label, val, active in rows:
            t = Text()
            t.append(f"  [ {num} ]  ", "bold white")
            t.append(label, "white")
            t.append(val, "cyan" if active else "dim white")
            console.print(t)

        t = Text()
        t.append("  [ 8 ]  ", "bold white")
        t.append("Back", "white")
        console.print(t)

        choice = prompt("settings")

        if choice == "1":
            state["webrtc"] = not state["webrtc"]
            console.print(Text(f"\n  WebRTC {'blocked' if state['webrtc'] else 'enabled'}.", "dim white"))
            time.sleep(0.8)

        elif choice == "2":
            clear()
            console.print(Rule(Text("Resolution", style="bold white"), style="dim white"))
            console.print()
            for num, res in RESOLUTIONS.items():
                active = state["res_label"] == res["label"]
                t = Text()
                t.append("  > " if active else "    ", "bold cyan" if active else "white")
                t.append(f"[ {num} ]  ", "bold white")
                t.append(res["label"], "white")
                console.print(t)
            pick = prompt("resolution")
            if pick in RESOLUTIONS:
                res = RESOLUTIONS[pick]
                state["resolution"] = (res["w"], res["h"]) if res["w"] else None
                state["res_label"]  = res["label"]
                console.print(Text(f"\n  set → {res['label']}", "dim white"))
                time.sleep(0.8)

        elif choice == "3":
            clear()
            console.print(Rule(Text("Theme", style="bold white"), style="dim white"))
            console.print()
            for num, theme in THEMES.items():
                active = state["theme"] == theme
                t = Text()
                t.append("  > " if active else "    ", "bold cyan" if active else "white")
                t.append(f"[ {num} ]  ", "bold white")
                t.append(theme, "white")
                console.print(t)
            pick = prompt("theme")
            if pick in THEMES:
                state["theme"] = THEMES[pick]
                console.print(Text(f"\n  set → {state['theme']}", "dim white"))
                time.sleep(0.8)

        elif choice == "4":
            clear()
            console.print(Rule(Text("Browser Type", style="bold white"), style="dim white"))
            console.print()
            for num, browser in BROWSER_TYPES.items():
                active = browser["driver"] == state["browser_type"]
                t = Text()
                t.append("  > " if active else "    ", "bold cyan" if active else "white")
                t.append(f"[ {num} ]  ", "bold white")
                t.append(browser["label"], "white")
                console.print(t)
            pick = prompt("browser")
            if pick in BROWSER_TYPES:
                browser = BROWSER_TYPES[pick]
                state["browser_type"] = browser["driver"]
                state["browser_label"] = browser["label"]
                console.print(Text(f"\n  set → {browser['label']}", "dim white"))
                time.sleep(0.8)

        elif choice == "5":
            state["headless"] = not state["headless"]
            console.print(Text(f"\n  Headless {'enabled' if state['headless'] else 'disabled'}.", "dim white"))
            time.sleep(0.8)

        elif choice == "6":
            state["incognito"] = not state["incognito"]
            console.print(Text(f"\n  Incognito {'enabled' if state['incognito'] else 'disabled'}.", "dim white"))
            time.sleep(0.8)

        elif choice == "7":
            console.print()
            console.print(Text("  current → " + (state["extension_path"] if state["extension_path"] else "none"), "dim white"))
            ext_path = console.input(Text("  extension path → ", "dim white")).strip()
            if ext_path and os.path.exists(ext_path):
                state["extension_path"] = ext_path
                console.print(Text(f"\n  extension set → {ext_path}", "dim white"))
            elif ext_path:
                console.print(Text("\n  path not found.", "red"))
            else:
                state["extension_path"] = None
                console.print(Text("\n  extension cleared.", "dim white"))
            time.sleep(0.8)

        elif choice in ("8", "q", "back"):
            break

                                                                                

def launch_browser():
    loc = state["location"]
    rpc_update(details="Launching Browser", state_text=f"Location: {loc['label']}")

    if not SELENIUM_OK:
        console.print(Text("\n  selenium not found.  Run: pip install selenium\n", "red"))
        input("  press enter...")
        return

    name = random_name()
    console.print(Text(f"\n  location   → {loc['flag']}  {loc['label']}", "white"))
    console.print(Text(f"  identity   → {name}", "dim white"))
    console.print(Text(f"  browser    → {state['browser_label']}", "dim white"))
    console.print(Text(f"  headless   → {'enabled' if state['headless'] else 'disabled'}", "dim white"))
    console.print(Text(f"  incognito  → {'enabled' if state['incognito'] else 'disabled'}", "dim white"))
    console.print(Text(f"  resolution → {state['res_label']}", "dim white"))
    console.print(Text(f"  webrtc     → {'blocked' if state['webrtc'] else 'enabled'}", "dim white"))
    console.print(Text(f"  theme      → {state['theme']}", "dim white"))
    if state["ua"]:
        console.print(Text(f"  agent      → {state['ua_label']}", "dim white"))
    if state["proxy"]:
        console.print(Text(f"  proxy      → {state['proxy_type']}://{state['proxy']}", "dim white"))
    if state["extension_path"]:
        console.print(Text(f"  extension  → {state['extension_path']}", "dim white"))
    console.print()

    driver = None
    profile_dir = None

            
    if state["browser_type"] == "chrome":
        profile_dir = pathlib.Path(tempfile.mkdtemp(prefix="chrome_profile_"))
        default_dir = profile_dir / "Default"
        default_dir.mkdir(parents=True, exist_ok=True)
        (default_dir / "Preferences").write_text(json.dumps({
            "profile": {"name": name, "managed_user_id": "", "supervised_user_id": ""}
        }))

        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-data-dir={profile_dir}")
        options.add_argument(f"--lang={loc['locale']}")

        if state["headless"]:
            options.add_argument("--headless=new")

        if state["incognito"]:
            options.add_argument("--incognito")

        if state["extension_path"]:
            options.add_argument(f"--load-extension={state['extension_path']}")

        if state["webrtc"]:
            options.add_experimental_option("prefs", {
                "intl.accept_languages": loc["locale"],
                "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                "webrtc.multiple_routes_enabled": False,
                "webrtc.nonproxied_udp_enabled": False,
            })
            options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
        else:
            options.add_experimental_option("prefs", {"intl.accept_languages": loc["locale"]})

        if state["proxy"]:
            options.add_argument(f"--proxy-server={state['proxy_type']}://{state['proxy']}")
        if state["ua"]:
            options.add_argument(f"--user-agent={state['ua']}")

        if state["theme"] == "dark":
            options.add_argument("--force-dark-mode")
            options.add_argument("--enable-features=WebUIDarkMode")
        elif state["theme"] == "light":
            options.add_argument("--disable-features=WebUIDarkMode")

        if state["resolution"]:
            w, h = state["resolution"]
            options.add_argument(f"--window-size={w},{h}")

        driver = webdriver.Chrome(options=options)

        driver.execute_cdp_cmd("Emulation.setTimezoneOverride",    {"timezoneId": loc["timezone"]})
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": loc["lat"], "longitude": loc["lon"], "accuracy": 100})
        driver.execute_cdp_cmd("Emulation.setLocaleOverride",      {"locale": loc["locale"]})
        if state["ua"]:
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": state["ua"]})
        if state["resolution"]:
            w, h = state["resolution"]
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": w, "height": h, "deviceScaleFactor": 1, "mobile": h > w,
            })

             
    elif state["browser_type"] == "firefox":
        options = FirefoxOptions()

        if state["headless"]:
            options.add_argument("--headless")

        if state["proxy"]:
            options.set_preference("network.proxy.type", 1)
            if state["proxy_type"] == "socks5":
                options.set_preference("network.proxy.socks", state["proxy"].split(":")[0])
                options.set_preference("network.proxy.socks_port", int(state["proxy"].split(":")[1]))
            else:
                options.set_preference("network.proxy.http", state["proxy"].split(":")[0])
                options.set_preference("network.proxy.http_port", int(state["proxy"].split(":")[1]))

        if state["ua"]:
            options.set_preference("general.useragent.override", state["ua"])

        if state["extension_path"]:
            options.add_argument(f"--load-extension={state['extension_path']}")

        if state["resolution"]:
            w, h = state["resolution"]
            options.add_argument(f"--width={w}")
            options.add_argument(f"--height={h}")

                                                                             
        if state["webrtc"]:
            options.set_preference("media.peerconnection.enabled", False)

        driver = webdriver.Firefox(options=options)

          
    elif state["browser_type"] == "edge":
        from selenium.webdriver.edge.options import Options as EdgeOptions

        profile_dir = pathlib.Path(tempfile.mkdtemp(prefix="edge_profile_"))
        default_dir = profile_dir / "Default"
        default_dir.mkdir(parents=True, exist_ok=True)
        (default_dir / "Preferences").write_text(json.dumps({
            "profile": {"name": name, "managed_user_id": "", "supervised_user_id": ""}
        }))

        options = EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-data-dir={profile_dir}")
        options.add_argument(f"--lang={loc['locale']}")

        if state["headless"]:
            options.add_argument("--headless=new")

        if state["incognito"]:
            options.add_argument("--inprivate")

        if state["extension_path"]:
            options.add_argument(f"--load-extension={state['extension_path']}")

        if state["webrtc"]:
            options.add_experimental_option("prefs", {
                "intl.accept_languages": loc["locale"],
                "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                "webrtc.multiple_routes_enabled": False,
                "webrtc.nonproxied_udp_enabled": False,
            })
        else:
            options.add_experimental_option("prefs", {"intl.accept_languages": loc["locale"]})

        if state["proxy"]:
            options.add_argument(f"--proxy-server={state['proxy_type']}://{state['proxy']}")
        if state["ua"]:
            options.add_argument(f"--user-agent={state['ua']}")

        if state["theme"] == "dark":
            options.add_argument("--force-dark-mode")

        if state["resolution"]:
            w, h = state["resolution"]
            options.add_argument(f"--window-size={w},{h}")

        driver = webdriver.Edge(options=options)

        driver.execute_cdp_cmd("Emulation.setTimezoneOverride",    {"timezoneId": loc["timezone"]})
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": loc["lat"], "longitude": loc["lon"], "accuracy": 100})
        driver.execute_cdp_cmd("Emulation.setLocaleOverride",      {"locale": loc["locale"]})
        if state["ua"]:
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": state["ua"]})
        if state["resolution"]:
            w, h = state["resolution"]
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": w, "height": h, "deviceScaleFactor": 1, "mobile": h > w,
            })

    if not driver:
        console.print(Text("\n  failed to launch browser.", "red"))
        input("  press enter...")
        return

    driver.get("https://somean.netlify.app/")
    driver.execute_script(f"document.title = '{name}'")
    driver.execute_script("window.open('https://whatmyuseragent.com/', '_blank')")

    console.print(Text("  browser open. press enter to close.", "dim white"))
    input()
    driver.quit()
    try:
        if profile_dir:
            shutil.rmtree(profile_dir)
    except Exception:
        pass
    console.print(Text("  closed.\n", "dim white"))
    time.sleep(0.6)

                                                                                
# by dopa @22gs
def main():
    rpc_connect()
    rpc_update(details="Browser Tool", state_text="Starting up")
    while True:
        cmd = draw_main()
        if   cmd == "1": launch_browser()
        elif cmd == "2": draw_location()
        elif cmd == "3": draw_ua()
        elif cmd == "4": draw_proxy()
        elif cmd == "5": draw_browser_settings()
        elif cmd == "6": draw_presets()
        elif cmd in ("7", "q", "exit"):
            rpc_close()
            clear()
            break

if __name__ == "__main__":
    main()
    # by dopa @22gs