import tkinter as tk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkinter import *
import main
import time
import render_time

# --- creating root window for the GUI ---
root = tk.Tk()
root.title("Elliptical Ray-Tracing Simulator")
root.geometry('850x550')

frame = tk.Frame(root)  # buttons and stuff go here
frame.grid(row=0, column=0, sticky=N)
root.grid_rowconfigure(0, weight=5)
root.grid_columnconfigure(0, weight=2)

plot_frame = tk.Frame(root)  # plot window goes here
plot_frame.grid(row=0, column=1, rowspan=1, columnspan=2)
root.grid_columnconfigure(1, weight=1)

toolbarFrame = Frame(master=root)  # toolbar goes here
toolbarFrame.grid(row=2, column=0, columnspan=2, sticky=W)

# --- variable assignment ---
vel_var = tk.StringVar(name="Velocity", value="1")
angle_min_var = tk.StringVar(name="Minimum Angle", value="90")
angle_max_var = tk.StringVar(name="Maximum Angle", value="225")
part_var = tk.StringVar(name="Partition", value="1")
j_var = tk.StringVar(name="Horizontal Starting Value", value="0.1")
k_var = tk.StringVar(name="Vertical Starting Value", value="0.2")
h_var = tk.StringVar(name="Horizontal Scaling Factor", value="1.4")
r_var = tk.StringVar(name="Number of Reflections", value="5")
fin_check_var = tk.BooleanVar(name="Only render final reflection?", value=False)
start_check_var = tk.BooleanVar(name="Render starting point?", value=True)
width_var = tk.StringVar(name="Ray width", value="0.002")
decay_var = tk.BooleanVar(name="Decay on or off?", value=False)
foci_var = tk.BooleanVar(name="Render foci?", value=True)
dpi_var = tk.StringVar(name="DPI", value="300")
animate_var = tk.BooleanVar(name="Animate", value=False)
anim_dpi_var = tk.StringVar(name="Animation DPI", value="200")
frame_num_var = tk.StringVar(name="Number of Frames", value="60")
fps_var = tk.StringVar(name="FPS", value="30")

# --- Labels and Entry Fields ---

# I need to eventually validate the entry fields using the validate method from Tkinter located here:
# https://www.tcl.tk/man/tcl8.5/TkCmd/entry.html#M-validate

label_names = ["Velocity", "Min Angle", "Max Angle", "Partition", "Horizontal Start", "Vertical Start",
               "Ellipse Scaling", "Number of Reflections", "Ray Width", "Save Plot Resolution", "Animation Resolution",
               "Number of Frames", "FPS (WIP)"]

for i in label_names:
    tk.Label(frame, text=i).grid(sticky="W", row=label_names.index(i), column=0)

text_vars = [vel_var, angle_min_var, angle_max_var, part_var, j_var, k_var, h_var, r_var, width_var, dpi_var,
             anim_dpi_var, frame_num_var, fps_var]

for i in text_vars:
    tk.Entry(frame, textvariable=i).grid(sticky="W", row=text_vars.index(i), column=1)

check_vars = [fin_check_var, start_check_var, decay_var, foci_var, animate_var]
check_labels = ["Render Final Reflection Only", "Toggle Start Point", "Toggle Decaying Brightness", "Toggle Foci",
                "Animate Mode"]

row_start = len(label_names)  # the minus 1 because .grid positions start at 1
for a, b in zip(check_labels, check_vars):  # iterates through both check_vars and check_labels at once
    tk.Checkbutton(frame, text=a, variable=b, onvalue=True, offvalue=False).grid(sticky="W", row=row_start, column=0)
    row_start += 1

# --- figures/frames to be placed in the root window ---
fig = Figure(figsize=(5, 5), dpi=100, facecolor='black')
canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.

toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)  # helpful toolbar to let people zoom in and stuff
toolbar.grid(row=1, column=2, ipadx=10)


# --- updates and plotting ---
def update():  # updates plot info

    global rend_time
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
    frame_num_gui = float(frame_num_var.get())
    fps_gui = float(fps_var.get())  # currently unused

    # --- plotting ---
    # NOTE: Plot is not centered anymore when .savefig is used. It's much larger, but it not being centered is
    # rather annoying looking
    ax = fig.add_subplot()
    ax.set_facecolor('black')
    ax.axis('off')
    ax.axis('Equal')
    ax.grid(False)

    t1 = np.linspace(0, 2 * np.pi, 500)

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

    # --- animation stuff ---
    if animate_var.get():  # saving a bunch of frames
        print("Estimating render time via curve-fitting...")
        num = 0
        num_fin = frame_num_gui  # this is the number of frames drawn

        times = []
        initial = time.perf_counter_ns()
        previous = time.perf_counter_ns()
        while num <= num_fin:
            if num < 20:
                current = time.perf_counter_ns()
                new_time = current - previous
                previous = current

                times.append(new_time)

                if num == 10:
                    print("Sampling halfway completed...")

            elif num == 20:
                times = np.array(times)
                rend_time = int(render_time.render_guess(times, num_fin)) / (10 ** 9)
                # converting render time in seconds to an hour-minutes-seconds format, lots of modulos and division

                seconds = int(rend_time % 60)
                minutes = int(((seconds - rend_time) / -60) % 60)
                hours = int(((minutes - ((seconds - rend_time) / -60)) / -60) % 60)

                print("Estimated render time: " + str(hours) + " hours, " + str(minutes) + " minutes and "
                      + str(seconds) + " seconds.")  # I should subtract time elapsed during estimation

            elif num == num_fin:
                print("Render complete!")
                toc2 = time.perf_counter_ns()

                rend_time_total = ((toc2 - initial) / 10 ** 9)

                seconds_total = int(rend_time_total % 60)
                minutes_total = int(((seconds_total - rend_time_total) / -60) % 60)
                hours_total = int(((minutes_total - ((seconds_total - rend_time_total) / -60)) / -60) % 60)

                print("Actual render time was " + str(hours_total) + " hours, " + str(minutes_total) + " minutes and "
                      + str(seconds_total) + " seconds.")

                print("Estimation % error was " +
                      str(round(100 * (rend_time_total - rend_time) / ((rend_time + rend_time_total) / 2))) + "% off.")

                print("Estimation total error was " + str(int(rend_time_total - rend_time)) + " seconds.")

            ax.clear()

            # --- Animation Conditions ---
            # comment out the stuff that isn't being used.

            # angles = np.linspace((angle_min_gui * np.pi) / 180, (angle_max_gui * np.pi) / 180, part_gui)

            # Elliptical path
            # h_gui = 2 * (num / num_fin) + 1  # use to make ellipse change with num

            sync = (360 / num_fin) * num  # makes number of rotations independent of frames
            mult = 1  # scales number of rotations per animation, can be integer or float
            scale = 0.1  # scales ellipse

            dtx = scale * np.cos(mult * sync * (np.pi / 180)) + np.sqrt(h_gui ** 2 - 1)
            dty = scale * np.sin(mult * sync * (np.pi / 180))

            # to define a set number of angles at specific values, still can be iterated through
            angles = [
                ((angle_min_gui * np.pi) / 180) + np.arctan2(dty, dtx - np.sqrt(h_gui ** 2 - 1)),
                ((angle_max_gui * np.pi) / 180) + np.arctan2(dty, dtx - np.sqrt(h_gui ** 2 - 1))
            ]

            # From one focus to the other if h > 1

            # sync = main.dist(-np.sqrt(h_gui ** 2 - 1), np.sqrt(h_gui ** 2 - 1), 0, 0)
            # dtx = - np.sqrt(h_gui ** 2 - 1) + (sync * num) / num_fin
            # dty = 0

            # A stretched spiral that goes from one focus to the other, scaled for 3600 frames

            # dtx = main.spiral(2.9996, np.sqrt(3)-0.8, 0.81, 0.008, -0.002, 0.1021, num, "horiz")
            # dty = main.spiral(2.9996, 0, 0.81, 0.008, -0.002, 0.1021, num, "vert")

            # dtx = 0.2
            # dty = 0.1

            # plotting ellipse
            t1 = np.linspace(0, 2 * np.pi, 500)

            ax.plot(h_gui * np.cos(t1), np.sin(t1), color='white')

            # starting point
            if start_check_gui:
                ax.plot(dtx, dty, marker='o', markerfacecolor='blue', markersize=5)

            # foci
            if foci_gui:
                if h_gui > 1:
                    ax.plot(np.sqrt(h_gui ** 2 - 1), 0, marker='o', markerfacecolor='green', markersize=2)
                    ax.plot(-np.sqrt(h_gui ** 2 - 1), 0, marker='o', markerfacecolor='green', markersize=2)
                if h_gui < 1:
                    ax.plot(0, np.sqrt(1 - h_gui ** 2), marker='o', markerfacecolor='green', markersize=2)
                    ax.plot(0, -np.sqrt(1 - h_gui ** 2), marker='o', markerfacecolor='green', markersize=2)
                if h_gui == 1:
                    ax.plot(0, 0, marker='o', markerfacecolor='green', markersize=2)

            # displaying plot
            for ang in angles:
                iterate(vel_gui, ang, dtx, dty, r_gui, fin_check_gui, decay_gui, width_gui, h_gui)

            fig.savefig(
                "Animation Frames/img" + f"{num:03}" + ".png",
                dpi=int(anim_dpi_var.get()),
                bbox_inches='tight'
            )

            # updating counter
            num += 1
    else:
        angles = np.linspace((angle_min_gui * np.pi) / 180, (angle_max_gui * np.pi) / 180, part_gui)
        for ang in angles:
            iterate(vel_gui, ang, j_gui, k_gui, r_gui, fin_check_gui, decay_gui, width_gui, h_gui)

    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)


# --- Save figure as an image ---
def save_fig():
    fig.savefig(
        "Saved Plots/(" + str(j_var.get()) + "," + str(k_var.get()) + ")" + ", H" +
        str(h_var.get()) + ", P" + str(part_var.get()) + ".png",
        dpi=int(dpi_var.get()),
        bbox_inches='tight',
        pad_inches=0
    )


# --- buttons ---
button_start = len(check_labels) + len(label_names)
submit_button = Button(master=frame, text="Update", command=update)
submit_button.grid(row=button_start + 1, column=0)

savefig_button = Button(master=frame, text="Save plot as .png", command=save_fig)
savefig_button.grid(row=button_start + 2, column=0)




root.mainloop()
