import subprocess


class VarExistsError(Exception):
    '''Raised when trying to register var with an already existing key.'''

    def __init__(self, key):
        super().__init__()
        print(f"'{key}' already exists in vars.")


class ScriptBuilder:
    def __init__(self, name: str, working_dir: str):
        self.name = name
        self.working_dir = working_dir
        self.vars = {}

        self.tmux = None
        self.browser = None

    def tmux_init(self):
        self.tmux = TmuxBuilder(self)
        self.add_var("tx_session", self.name)

    def browser_init(self, kiosk_mode: bool = False):
        self.browser = BrowserBuilder(self, kiosk_mode=kiosk_mode)

    def to_string(self):
        string = "#!/bin/bash\n\n"
        string += "### Variables\n"
        for var in self.vars:
            if type(self.vars[var]) is str:
                string += f"{var}='{self.vars[var]}'\n"
            else:
                string += f"{var}={self.vars[var]}\n"
        string += "\n"
        if self.browser is not None:
            string += "### Browser\n"
            string += self.browser.to_string()
        if self.tmux is not None:
            string += "### Tmux\n"
            string += self.tmux.to_string()
        return string

    def get_browser_windows(self):
        if self.browser is None:
            print("No browser exists.")
            return
        return self.browser.windows

    def add_var(self, key, value):
        if key in self.vars:
            raise VarExistsError(key)
            return
        self.vars[key] = value


class BrowserBuilder:
    def __init__(self, parent: ScriptBuilder, driver: str = "firefox", kiosk_mode=False):
        # currently only supporting firefox
        self.parent = parent
        self.driver = driver
        self.kiosk_mode = kiosk_mode
        self.num_windows = 0
        self.windows = {}
        self.vars = {}

    def add_window(self, tabs: list[str]):
        self.windows[self.num_windows] = {
                "tabs": tabs,
                }
        self.num_windows += 1

    def to_string(self):
        string = ""
        for window in self.windows:
            tabs = self.windows[window]["tabs"]
            string += self.__new_window(tabs[0])
            if not len(tabs) > 1:
                return string
            for tab in tabs[1:]:
                string += self.__new_tab(tab)

    def __new_window(self, url: str):
        return f"{self.driver} -new-window {url}\n"

    def __new_tab(self, url: str):
        return f"{self.driver} -new-tab {url}\n"


class TmuxBuilder:
    def __init__(self, parent: ScriptBuilder):
        self.parent = parent
        self.name = parent.name
        self.num_windows = 0
        self.windows = {}

    def add_window(self, name: str, layout: str, panes: list[str]):
        try:
            self.parent.add_var(name, self.num_windows)
        except VarExistsError:
            name = f"{name}_2"
            self.parent.add_var(name, self.num_windows)
        self.windows[self.num_windows] = {
                "name": name,
                "panes": panes,
                "layout": layout,
                }
        self.num_windows += 1

    def build_window(self, window_num: int, tabstops: str = "\t"):
        string = ""
        window = self.windows[window_num]
        # if not first window, create window with first pane path
        if window_num > 0:
            string += self.__new_window(window["name"], window["panes"][0])

        string += self.__select_window(window["name"])
        if not len(window["panes"]) > 1:
            return string
        for pane in window["panes"][1:]:
            string += self.__split_window(pane, direction="h")
        string += self.__select_layout(window["layout"])
        return string

    def to_string(self):
        OPEN_BRACE = "{"
        CLOSE_BRACE = "}"
        string = self.__attach_session() + " || "
        string += OPEN_BRACE + "\n"
        if len(self.windows) > 1:
            # Session with user-created windows
            string += self.__new_session(self.windows[0]["panes"][0])
            string += self.__rename_window(self.windows[0]["name"])
            for window in self.windows:
                string += self.build_window(window)
                string += "\n"
            string += self.__select_window(self.windows[0]["name"])
            string += self.__select_pane(0)
        else:
            # Blank session
            string += self.__new_session()
        string += self.__attach_session(prefix="\t", suffix="\n")
        string += CLOSE_BRACE
        return string

    def __new_session(self, first_win_pane_dir: str = "~/"):
        return f"\ttmux new-session -d -s $tx_session -c `realpath {first_win_pane_dir}`\n\n"

    def __attach_session(self, prefix: str = "", suffix: str = ""):
        return f"{prefix}tmux attach -t $tx_session{suffix}"

    def __new_window(self, name: str, working_dir: str):
        return f"\ttmux new-window -n '{name}' -c `realpath {working_dir}`\n"

    def __rename_window(self, name: str):
        return f"\ttmux rename-window -t $tx_session:${name} '{name}'\n"

    def __select_window(self, name: str):
        return f"\ttmux select-window -t ${name}\n"

    def __split_window(self, working_dir: str, direction: str = "h"):
        return f"\ttmux split-window -{direction} -c `realpath {working_dir}`\n"

    def __select_pane(self, num: int):
        return f"\ttmux select-pane -t {num}\n"

    def __select_layout(self, layout: str):
        string = ""
        if layout not in ["tiled", "tiled", "even-vertical",
                          "even-horizontal", "main-vertical",
                          "main-horizontal"]:
            print(f"Invalid layout \"{layout}\". Using \"tiled\".")
            self.layout = "tiled"
        string += f"\ttmux select-layout {layout}\n"
        if layout == "main-vertical":
            string += "\ttmux resize-pane -t 0 -x 50%\n"
        return string


def make_exec(fpath: str):
    subprocess.run(["chmod", "+x", fpath])


if __name__ == "__main__":
    # testing
    script = ScriptBuilder("sesh", "~/documents/")
    script.tmux_init()
    print(script.vars)
    with open("testing.sh", "w+") as file:
        file.write(script.to_string())
