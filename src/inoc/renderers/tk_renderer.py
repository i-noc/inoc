import tkinter as tk

class TkRenderer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.interpreter = runtime.interpreter
        self.root = None
        self.main_container = None
        self._last_ui_version = -1
        self._last_screen = None

    def start(self):
        self.root = tk.Tk()
        self.root.title(self.runtime.app_name)
        self.root.geometry("450x700")
        self._check_for_updates()
        self.root.mainloop()

    def _check_for_updates(self):
        cur_screen = self.interpreter.current_screen
        ui_ver = self.interpreter.ui_version
        if not self.main_container or self._last_screen != cur_screen or self._last_ui_version != ui_ver:
            self.render_screen(cur_screen)
            self._last_screen = cur_screen
            self._last_ui_version = ui_ver
        self.root.after(200, self._check_for_updates)

    def render_screen(self, screen_name):
        if screen_name not in self.interpreter.ui_registry: return
        if self.main_container:
            self.main_container.destroy()
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        self.runtime.input_widgets = []
        self.runtime.input_by_id_widgets = {}
        self._render_recursive(self.main_container, self.interpreter.ui_registry[screen_name])

    def _render_recursive(self, parent, elements):
        rows = {}
        for data in elements:
            if data["type"] == "janela":
                self._apply_window_props(data["props"])
                continue
            line = data.get("line", 0)
            if line not in rows: rows[line] = []
            rows[line].append(data)

        max_cols = 1
        for line_num in rows: max_cols = max(max_cols, len(rows[line_num]))
        for c in range(max_cols): parent.grid_columnconfigure(c, weight=1, uniform="equal")

        for r_idx, line_num in enumerate(sorted(rows.keys())):
            elements_in_row = rows[line_num]
            for c_idx, data in enumerate(elements_in_row):
                col_span = max_cols if len(elements_in_row) == 1 else 1
                self._render_element(parent, data, r_idx, c_idx, col_span)

    def _apply_window_props(self, props):
        bg = self.runtime.color_map.get(props.get("cor"), props.get("cor"))
        if bg:
            self.root.config(bg=bg)
            self.main_container.config(bg=bg)

    def _render_element(self, parent, data, row, col, colspan):
        el_type, value, props, action = data["type"], data["value"], data.get("props", {}), data.get("action")
        bg, fg = self.runtime.color_map.get(props.get("cor")), self.runtime.color_map.get(props.get("cor_texto"))
        font = (props.get("fonte", "Arial"), int(props.get("tamanho", 12)))
        w = None
        if el_type == "container":
            w = tk.Frame(parent, bd=int(props.get("borda", 0)), relief="solid" if props.get("borda") else "flat")
            self._render_recursive(w, data["children"])
        elif el_type == "texto":
            w = tk.Label(parent, text=value, font=font)
        elif el_type == "botao":
            def cmd():
                for tid, entry in self.runtime.input_by_id_widgets.items():
                    self.interpreter._builtin_definir([tid, entry.get()])

                for entry in self.runtime.input_widgets:
                    self.runtime.input_queue.put(entry.get())
                if action and action["type"] == "navegacao":
                    self.interpreter.current_screen = action["target"]
                elif action and action["type"] == "funcao":
                    self.interpreter.event_queue.put({"type": "call", "name": action["name"]})
                else:
                    self.interpreter.event_queue.put(value)
            w = tk.Button(parent, text=value, font=font, command=cmd)
        elif el_type == "input":
            w = tk.Entry(parent, font=font)
            w.insert(0, value)
            if props.get("id"):
                self.runtime.input_by_id_widgets[props.get("id")] = w
            else:
                self.runtime.input_widgets.append(w)

        if w:
            if bg: w.config(bg=bg)
            if fg: w.config(fg=fg)
            sticky, align = "nsew", self.runtime.align_map.get(props.get("alinhamento", ""))
            if align == "w": sticky = "w"
            elif align == "e": sticky = "e"
            w.grid(row=row, column=col, columnspan=colspan, padx=int(props.get("margem", 2)), pady=int(props.get("margem", 2)), sticky=sticky)
