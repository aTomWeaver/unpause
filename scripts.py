import subprocess


class TmuxBuilder:
    def __init__(self, name: str, layout: str = "tiled"):
        self.name = name
        if layout not in ["tiled", "tiled", "even-vertical",
                          "even-horizontal", "main-vertical",
                          "main-horizontal"]:
            print(f"Invalid layout \"{layout}\". Using \"tiled\".")
            self.layout = "tiled"
        else:
            self.layout = layout

        self.num_windows = 0    # maybe start with 1
        self.windows = {}

    def new_window(self, name: str, panes: list[str]):
        self.windows[self.num_windows] = {
                "name": name,
                "panes": panes
                }
        self.num_windows += 1

    def build_window(self, window_num: int, tabs: str = "\t"):
        string = ""
        window = self.windows[window_num]
        # if not first window, create window with first pane path
        if window_num > 0:
            string += f"\ttmux new-window -n '{window["name"]}'" \
                    f" -c `realpath {window["panes"][0]}`\n"

        string += f"{tabs}tmux select-window -t ${window["name"]}\n"
        if not len(window["panes"]) > 1:
            return string
        for pane in window["panes"][1:]:
            print(f"initializing pane: {pane}")
            string += f"{tabs}tmux split-window -h -c `realpath {pane}`\n"
        return string

    def to_string(self):
        string = "### VARS\n"
        string += f"session=\"{self.name}\"\n"
        for window in self.windows.keys():
            string += f"{self.windows[window]["name"]}={window}\n"
        string += "\n"
        string += "### TMUX\n"
        string += "tmux attach -t $session || {\n"
        first_win_pane = self.windows[0]["panes"][0]
        first_win_name = self.windows[0]["name"]
        string += f"\ttmux new-session -d -s $session -c `realpath {first_win_pane}`\n\n"
        string += f"\ttmux rename-window -t $session:${first_win_name} '{first_win_name}'\n"
        for window in self.windows:
            string += self.build_window(window)
            string += f"\ttmux select-layout {self.layout}\n"
            if self.layout == "main-vertical":
                string += "\ttmux resize-pane -t 0 -x 50%\n"
            string += "\n"
        string += "\ttmux select-window -t 0\n"
        string += "\ttmux select-pane -t 0\n"
        string += "\ttmux attach-session -t $session\n}\n"
        return string


def make_exec(fpath: str):
    subprocess.run(["chmod", "+x", fpath])


if __name__ == "__main__":
    # testing
    sesh = TmuxBuilder("sesh", layout="main-vertical")
    sesh.new_window("win1", [
        "~/documents/",
        "~/pictures",
        "~/testing/",
        "~/downloads/"
        ])
    sesh.new_window("test", [
        "~", "~/desktop/"
        ])
    print(sesh.windows)
    with open("testing.sh", "w+") as file:
        file.write(sesh.to_string())
