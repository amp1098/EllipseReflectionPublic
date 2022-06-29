import tkinter as tk

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import main

root = tk.Tk()
root.title("Elliptical Reflection Simulator")
root.geometry('850x550')

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky=N)
root.grid_rowconfigure(0, weight=5)
root.grid_columnconfigure(0, weight=2)

plot_frame = tk.Frame(root)
plot_frame.grid(row=0, column=1, rowspan=1, columnspan=2)
root.grid_columnconfigure(1, weight=1)

toolbarFrame = Frame(master=root)
toolbarFrame.grid(row=2, column=0, columnspan=2, sticky=W)

# --- variable assignment ---
vel_var = tk.StringVar(name="Velocity", value="1")
angle_min_var = tk.StringVar(name="Minimum Angle", value="0")
angle_max_var = tk.StringVar(name="Maximum Angle", value="30")
part_var = tk.StringVar(name="Partition", value="100")
j_var = tk.StringVar(name="Horizontal Starting Value", value="0")
k_var = tk.StringVar(name="Vertical Starting Value", value="0")
h_var = tk.StringVar(name="Horizontal Scaling Factor", value="1")
r_var = tk.StringVar(name="Number of Reflections", value="5")
fin_check_var = tk.BooleanVar(name="Only render final reflection?", value=True)
start_check_var = tk.BooleanVar(name="Render starting point?", value=True)
width_var = tk.StringVar(name="Ray width", value="0.0001")
decay_var = tk.BooleanVar(name="Decay on or off?", value=True)
foci_var = tk.BooleanVar(name="Render foci?", value=True)

# --- Labels and Entry Fields ---

# I need to eventually validate the entry fields using the validate method from Tkinter located here:
# https://www.tcl.tk/man/tcl8.5/TkCmd/entry.html#M-validate

tk.Label(frame, text="Velocity").grid(sticky="W", row=0, column=0)
tk.Label(frame, text="Min Angle").grid(sticky="W", row=1, column=0)
tk.Label(frame, text="Max Angle").grid(sticky="W", row=2, column=0)
tk.Label(frame, text="Partition").grid(sticky="W", row=3, column=0)
tk.Label(frame, text="Horizontal Start").grid(sticky="W", row=4, column=0)
tk.Label(frame, text="Vertical Start").grid(sticky="W", row=5, column=0)
tk.Label(frame, text="Ellipse Scaling").grid(sticky="W", row=6, column=0)
tk.Label(frame, text="Number of Reflections").grid(sticky="W", row=7, column=0)
tk.Label(frame, text="Ray Width").grid(sticky="W", row=8, column=0)

tk.Entry(frame, textvariable=vel_var).grid(sticky="W", row=0, column=1)
tk.Entry(frame, textvariable=angle_min_var).grid(sticky="W", row=1, column=1)
tk.Entry(frame, textvariable=angle_max_var).grid(sticky="W", row=2, column=1)
tk.Entry(frame, textvariable=part_var).grid(sticky="W", row=3, column=1)
tk.Entry(frame, textvariable=j_var).grid(sticky="W", row=4, column=1)
tk.Entry(frame, textvariable=k_var).grid(sticky="W", row=5, column=1)
tk.Entry(frame, textvariable=h_var).grid(sticky="W", row=6, column=1)
tk.Entry(frame, textvariable=r_var).grid(sticky="W", row=7, column=1)
tk.Entry(frame, textvariable=width_var).grid(sticky="W", row=8, column=1)

tk.Checkbutton(frame, text="Render Final Reflection Only", variable=fin_check_var, onvalue=True, offvalue=False).grid(sticky="W", row=9, column=0)
tk.Checkbutton(frame, text="Toggle Start Point", variable=start_check_var, onvalue=True, offvalue=False).grid(sticky="W", row=10, column=0
                                                                                             )
tk.Checkbutton(frame, text="Toggle Decaying Brightness", variable=decay_var, onvalue=True, offvalue=False).grid(sticky="W", row=11, column=0)
tk.Checkbutton(frame, text="Toggle Foci", variable=foci_var, onvalue=True, offvalue=False).grid(sticky="W", row=12, column=0)


# --- figures/frames to be placed in the root window ---

fig = Figure(figsize=(6, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.

toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)  # helpful toolbar to let people zoom in and stuff
toolbar.grid(row=1, column=2, ipadx=10)


# --- updates and plotting ---
def update():  # updates plot info

    fig.clear()

    # --- updating variables for main to read ---

    vel_gui = float(vel_var.get())
    angle_min_gui = float(angle_min_var.get())
    angle_max_gui = float(angle_max_var.get())
    part_gui = int(part_var.get())
    j_gui = float(j_var.get())
    k_gui = float(k_var.get())
    h_gui = float(h_var.get())
    r_gui = float(r_var.get())
    fin_check_gui = fin_check_var.get()
    start_check_gui = start_check_var.get()
    width_gui = float(width_var.get())
    decay_gui = decay_var.get()
    foci_gui = foci_var.get()

    angles = np.linspace((angle_min_gui * np.pi) / 180, (angle_max_gui * np.pi) / 180, part_gui)

    # --- plotting ---
    ax = fig.add_subplot()
    ax.set_facecolor('black')
    ax.axis("Equal")
    ax.grid(False)
    ax.set_title(
        "("+str(j_gui)+"," + str(k_gui) + ")" + ", Horizontal Scaling=" + str(h_gui) + ", Partitions=" + str(part_gui)
    )

    t1 = np.linspace(0, 2 * np.pi, 100)

    ax.plot(h_gui * np.cos(t1), np.sin(t1), color='white')

    if start_check_gui:
        ax.plot(j_gui, k_gui, marker='o', markerfacecolor='blue', markersize=5)

    if foci_gui:
        if h_gui > 1:
            ax.plot(np.sqrt(h_gui ** 2 - 1), 0, marker='o', markerfacecolor='green', markersize=2)
            ax.plot(-np.sqrt(h_gui ** 2 - 1), 0, marker='o', markerfacecolor='green', markersize=2)
        if h_gui < 1:
            ax.plot(0, np.sqrt(1 - h_gui ** 2), marker='o', markerfacecolor='green', markersize=2)
            ax.plot(0, -np.sqrt(1 - h_gui ** 2), marker='o', markerfacecolor='green', markersize=2)
        if h_gui == 1:
            ax.plot(0, 0, marker='o', markerfacecolor='green', markersize=2)

    # --- iterate function ---

    def iterate(vel, theta, x, y, r, c, d, w, h):
        while r > 0:

            # checking for decay parameter's truth value
            if d:
                decay_val = (0.5 ** (r_gui - r))
            else:
                decay_val = 1

            # impact parameter (basically, how will the velocity vector stretch to land on the ellipse?)
            i_param = main.impact(vel, theta, x, y, h)

            # initial vector

            V = np.array(
                [[vel * np.cos(theta) * i_param, vel * np.sin(theta) * i_param]]
            )
            # if only final reflection is allowed and more reflections need to be rendered
            if c and r > 1:
                # impact point updater
                x = vel * np.cos(theta) * i_param + x
                y = vel * np.sin(theta) * i_param + y

                # angle of reflection updater
                theta = main.ang_ref(vel, theta, x, y, h)

                # r value updater
                r -= 1
            # if only final reflection is allowed and a single reflection is left
            elif c and r == 1:
                # plotter
                ax.quiver(
                    x, y, V[:, 0], V[:, 1], color='white',
                    angles='xy', scale_units='xy', scale=1,
                    headwidth=1, headlength=0,
                    width=w,
                    alpha=decay_val
                )
                # impact point updater
                x = vel * np.cos(theta) * i_param + x
                y = vel * np.sin(theta) * i_param + y

                # angle of reflection updater
                theta = main.ang_ref(vel, theta, x, y, h)

                # r value updater
                r -= 1
            # plotting all reflections
            else:
                # plotter
                ax.quiver(
                    x, y, V[:, 0], V[:, 1], color='white',
                    angles='xy', scale_units='xy', scale=1,
                    headwidth=1, headlength=0,
                    width=w,
                    alpha=decay_val
                )
                # impact point updater
                x = vel * np.cos(theta) * i_param + x
                y = vel * np.sin(theta) * i_param + y

                # angle of reflection updater
                theta = main.ang_ref(vel, theta, x, y, h)

                # r value updater

                r -= 1

    # --- end of iterate function ---

    for i in angles:
        iterate(vel_gui, i, j_gui, k_gui, r_gui, fin_check_gui, decay_gui, width_gui, h_gui)

    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)


# --- buttons ---
submit_button = Button(master=frame, text="Update", command=update)
submit_button.grid(row=13, column=0)

root.mainloop()
