# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import extension

import os
import subprocess

from libqtile import hook

@hook.subscribe.startup_complete
def autostart():
    shdohome = os.path.expanduser('~/.config/qtile/autostart.sh');
    subprocess.Popen([shdohome])

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
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
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # User Keybinds
    Key([mod], "p", lazy.run_extension(extension.RunCommand(
        command='flameshot gui',
    )), desc="Screen shot with flameshot!"),
    Key([mod], "XF86AudioMute", lazy.run_extension(extension.RunCommand(
        command='pactl set-sink-mute @DEFAULT_SINK@ toggle',
    )), desc="get mutable with pulseaudio"),
    Key([mod], "XF86AudioLowerVolume", lazy.run_extension(extension.RunCommand(
        command='pactl set-sink-volume @DEFAULT_SINK@ -5%',
    )), desc="get decr vol with pulseaudio"),
    Key([mod], "XF86AudioRaiseVolume", lazy.run_extension(extension.RunCommand(
        command='pactl set-sink-volume @DEFAULT_SINK@ +5%',
    )), desc="get incr vol with pulseaudio"),
    Key([mod], "XF86AudioMicMute", lazy.run_extension(extension.RunCommand(
        command='pactl set-sink-input-mute @DEFAULT_SINK@ toggle',
    )), desc="get mic mutable with pulseaudio"),
    Key([mod], "XF86MonBrightnessDown", lazy.run_extension(extension.RunCommand(
        command='xbacklight -dec 5',
    )), desc="backlight decrement with xbacklight"),
    Key([mod], "XF86MonBrightnessUp", lazy.run_extension(extension.RunCommand(
        command='xbacklight -inc 5',
    )), desc="backlight increment with xbacklight"),
    Key([mod], "XF86Search", lazy.run_extension(extension.RunCommand(
        command='firefox-developer-edition',
    )), desc="search with firefox"),
    Key([mod], "XF86Explorer", lazy.run_extension(extension.RunCommand(
        command='thunar',
    )), desc="explore files with thunar"),
    Key([mod], "XF86LaunchA", lazy.run_extension(extension.RunCommand(
        command='discord',
    )), desc="speak with discord"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=1
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
    fontshadow='#553333',
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(highlight_method='line'),
                widget.Prompt(highlight_method='line'),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#aaaaaa", "#333333"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.WidgetBox(
                    font='Adobe Heiti Std',
                    text_closed='[(查看)]',
                    text_open='[ 关闭 ]',
                    foreground='90cfff',
                    widgets=[
                    	widget.Spacer(length=5),
                		widget.ThermalZone(
                		    font='Impact Condensed',
                		),
                		widget.CPU(
                		    font='Comic Sans MS',
                		    fontshadow='#007700',
                		    format='{freq_current}GHz',
                		),
                		widget.CPUGraph(),
                		#widget.DF(),
                		widget.Memory(
                		    measure_mem='M',
                		    font='Noto Serif',
                		    foreground='b9a5ff',
                		    format='{MemUsed: .0f}{mm}'
                		),
                		#widget.MemoryGraph(),
                		widget.Net(
                		    font='IPAPMincho',
                		    foreground='3edbff',
                		    format='{up} 卡{down}',
                		    prefix='M',
                		),
                		widget.HDDBusyGraph(),
                		#widget.NetGraph(),
                	],
                	close_button_location='right',
                ),
                widget.Spacer(length=5),
                widget.Sep(), 
                widget.Battery(
                    battery=0,
                    foreground='55dc55',
                    low_background='d60000',
                    low_foreground='ffcc17',
                    format='{char} {percent:2.0%}',
                    full_char='😁',
                ),
                widget.Spacer(length=5),
                widget.Battery(
                    battery=1,
                    foreground='8affab',
                    low_background='d60000',
                    low_foreground='ffcc17',
                    format='{char} {percent:2.0%}',
                    full_char='✊',
                ),
                widget.Spacer(length=8),
                widget.PulseVolume(
                    fmt='🔊: {}',
                ),
                widget.Backlight(
                    backlight_name='intel_backlight',
                    fmt='🔆: {}',
                ),
                widget.Cmus(
                    font='Serif',
                    play_color='#41f8b8',
                ),
                widget.Systray(),
                # widget.Notify(),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Clock(format="%m-%d %a %H:%M.%S"),
                widget.WidgetBox(
                    font='Adobe Heiti Std',
                    text_closed='[当地信息]',
                    text_open='[  关闭  ]',
                    foreground='45aeff',
                    widgets=[
                        widget.Spacer(length=5),
                        widget.KhalCalendar(),
                        widget.OpenWeather(
                            cityid='Amagasaki',
                            foreground='2222ff',
                            format='{location_city}: {icon} {main_temp} °{units_temperature} [{main_temp_max} °{units_temperature} / {main_temp_min} °{units_temperature}]  {humidity}% {weather_details}',
                        ),
                    ],
                    close_button_location='right',
                ),
                widget.Spacer(length=5),
                widget.QuickExit(
                    default_text='(´･_･`)',
                    countdown_format='(՞ة{}ڼ◔)',
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
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
wmname = "LG3D"
