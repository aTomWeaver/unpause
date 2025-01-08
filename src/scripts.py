import os
import subprocess
from crud import write_file


class VarExistsError(Exception):
    '''Raised when trying to register var with an already existing key.'''

    def __init__(self, key):
        super().__init__()
        print(f"'{key}' already exists in vars.")


class ScriptBuilder:
    def __init__(self, name: str):
        self.name = name
        self.vars = {}

        self.tmux = None
        self.browser = None
        self.url_queue = []

    def tmux_init(self, start_directory: str = "~/"):
        self.tmux = TmuxBuilder(self)
        self.add_var("tx_session", self.name)

    def browser_init(self, driver: str = "firefox", kiosk_mode: bool = False):
        self.browser = BrowserBuilder(self, driver=driver, kiosk_mode=kiosk_mode)

    def build(self):
        return {
                "dir_path": f"{self.name}",
                "url_queue": self.url_queue,
                "script": self.to_string()
                }
        os.makedirs(f"projects/{self.name}", exist_ok=False)
        if self.url_queue != []:
            self.get_url_queue()
        return self.to_string()

    def to_string(self):
        string = "#!/bin/bash\n\n"
        string += "### Variables\n"
        for var in self.vars:
            if type(self.vars[var]) is str:
                if self.vars[var][0] == "`":
                    string += f"{var}={self.vars[var]}\n"
                else:
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

    def add_to_url_queue(self, var_name: str, url: str):
        self.url_queue.append((var_name, url))

    def get_url_queue(self):
        for item in self.url_queue:
            name, url = item
            write_file(url, f"projects/{self.name}/{name}")

    def add_var(self, key, value):
        if key in self.vars:
            raise VarExistsError(key)
            return
        self.vars[key] = value


class BrowserBuilder:
    def __init__(self,
                 parent: ScriptBuilder,
                 driver: str = "firefox",
                 kiosk_mode=False):
        # currently only supporting firefox
        self.parent = parent
        self.driver = driver
        self.kiosk_mode = kiosk_mode
        self.num_windows = 0
        self.windows = {}

    def add_window(self, tabs: list[tuple[str, str]]):
        for tab in tabs:
            print(tab)
            name, url = tab
            self.parent.add_var(f"url_{name}", f"`cat ./url_{name}`")
            self.parent.add_to_url_queue(f"url_{name}", url)
        self.windows[self.num_windows] = {
                "tabs": tabs,
                }
        self.num_windows += 1

    def to_string(self):
        string = ""
        for window in self.windows:
            tabs = self.windows[window]["tabs"]
            string += self.__new_window(f"url_{tabs[0][0]}")
            if len(tabs) > 1:
                for tab in tabs[1:]:
                    name, _ = tab
                    string += self.__new_tab(f"url_{name}")
        string += "\n"
        return string

    def __new_window(self, var_name: str, kiosk: bool = False):
        if kiosk:
            return f"{self.driver} -new-window -kiosk ${var_name}\n"
        return f"{self.driver} -new-window ${var_name}\n"

    def __new_tab(self, var_name: str):
        return f"{self.driver} -new-tab ${var_name}\n"


class TmuxBuilder:
    def __init__(self, parent: ScriptBuilder):
        self.parent = parent
        self.name = parent.name
        self.num_windows = 0
        self.windows = {}
        self.command_queue = []

    def add_window(self, name: str, layout: str, panes: list[tuple[str, str]]):
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
            string += self.__new_window(window["name"], window["panes"][0][0])
        string += self.__select_window(window["name"])
        for i, pane in enumerate(window["panes"]):
            directory, command = pane
            if command != "":
                target = f"${window["name"]}.{i}"
                self.command_queue.append((target, command))
            if i > 0:
                string += self.__split_window(directory, direction="h")
        string += self.__select_layout(window["layout"])
        return string

    def to_string(self):
        OPEN_BRACE = "{"
        CLOSE_BRACE = "}"
        SLEEP_INTERVAL = 0.3
        string = self.__attach_session() + " || "
        string += OPEN_BRACE + "\n"
        if len(self.windows) > 0:
            # Session with user-created windows
            first_pane_dir = self.windows[0]["panes"][0][0]
            first_pane_name = self.windows[0]["name"]
            string += self.__new_session(first_pane_dir)
            string += self.__rename_window(first_pane_name)
            for window in self.windows:
                string += self.build_window(window)
                string += "\n"
        else:
            # Blank session
            string += self.__new_session()
        string += "\t# Commands\n"
        string += f"\tsleep {SLEEP_INTERVAL}\n"
        for target, command in self.command_queue:
            string += self.__run_command(command, target=target)
        string += "\n"
        if len(self.windows) > 0:
            string += self.__select_window(self.windows[0]["name"])
            string += self.__select_pane(0)
        string += self.__attach_session(prefix="\t", suffix="\n")
        string += CLOSE_BRACE
        return string

    def __new_session(self, first_win_pane_dir: str = "~/"):
        return f"\ttmux new-session -d -s $tx_session -c `realpath {first_win_pane_dir}`\n"

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

    def __run_command(self, command: str, target: str = ""):
        if target:
            return f"\ttmux send-keys -t {target} '{command}' C-m\n"
        else:
            return f"\ttmux send-keys '{command}' C-m\n"


if __name__ == "__main__":
    # testing
    script = ScriptBuilder("sesh", "~/documents/")
    script.tmux_init()
    script.browser_init(driver="firefox", kiosk_mode=False)
    script.browser.add_window([
        ("youtube", "https://www.youtube.com"),
        ("google", "https://www.google.com"),
        ])
    script.browser.add_window([
        ("wikipedia", "https://en.wikipedia.org/wiki/Plus-Tech_Squeeze_Box"),
        ])
    script.tmux.add_window("win1", "even-horizontal", [
        ("~/pictures/", "cmatrix"),
        ])
    print(script.vars)
    write_file(script.build(), "projects/sesh/sesh.sh")
