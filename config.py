from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess
import os
from libqtile import hook

mod = "mod4"
mod1 = "mod1"
terminal = "alacritty"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(['sh', home])

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Key(
    #     [mod, "shift"],
    #     "Return",
    #     lazy.layout.toggle_split(),
    #     desc="Toggle between split and unsplit sides of stack",
    # ),

    # Launch apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "f", lazy.spawn("firefox"), desc="Launch firefox"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "s", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard()),
]

groups = [                                                                 
    Group("1", label = "", matches=[Match(wm_class=["firefox"])]),
    Group("2", label = ""),
    Group("3", label = "󰨞", matches=[Match(wm_class=["code-oss"])]),
    Group("4", label = "󰙯", matches=[Match(wm_class=["discord"])]),
    Group("5", label = "", matches=[Match(wm_class=["TelegramDesktop"])]),
    Group("6", label = "", matches=[Match(wm_class=["yandex-music-player"])]),
    Group("7", label = "󰓓", matches=[Match(wm_class=["Steam"])])
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

#Colors
catppuccin = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "mauve": "#cba6f7",
    "pink": "#f5c2e7",
    "maroon": "#eba0ac",
    "red": "#f38ba8",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "blue": "#89b4fa",
    "sky": "#89dceb",
    "lavender": "#b4befe",
    "white": "#d9e0ee",
    "gray": "#6e6c7e",
    "black": "#1a1826" 
}

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "#f9f9f9",
    "border_normal": "#263238", #263238
    "insert_position": 1
}


layouts = [
    # layout.MonadTall(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(margin=8),
    # layout.Floating(border_width=0, border_focus='#000000', border_normal='#000000'),
    # layout.Stack(num_stacks=2, margin=10),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="Roboto Mono",
    fontsize=14,
    padding=8,
    foreground="#f9f9f9", ##ebdbb2, #fbf1c7
    background="#263238"
)
extension_defaults = widget_defaults.copy()

widgets = [
    widget.Prompt(),
    widget.WindowName(
        max_chars=30
        ),
    widget.GroupBox(
        fontsize=23,
        borderwidth=4,
        #padding=10,
        rounded=True,
        margin_x=2,
        highlight_method="block",
        block_highlight_text_color="#f9f9f9", #263238
        this_current_screen_border="#263238", #45475a
        active="#79dfce",
        #inactive=catppuccin["white"],
        ),
    widget.Spacer(length=bar.STRETCH),
    widget.Systray(
        #icon_size=25,
        padding=10,
        ),
    widget.Spacer(length=10),
    widget.PulseVolume(
        padding=10,
        ),
    widget.KeyboardLayout(
        configured_keyboards=["us", "ru"],
        padding=5
        ),
    widget.Clock(
        padding=10,
        format="%d %a %H:%M %p"
       ) 
]

screens = [
    Screen(
        top=bar.Bar(
            widgets,
            size=28,
            margin=[8, 8, 0, 8],
            border_width=[5, 5, 5, 5],  # Толщина рамок панели
            border_color="263238",  # Цвет рамок панели
            background="#263238",  #263238, catppuccin["black"]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_width=0,
    float_rules=[ 
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile 0.22.1"
