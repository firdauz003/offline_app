import math
import random
import sys
import threading
import tkinter as tk


class AnimatedSquareRobotApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Robot with Blinking & Sound")

        # Canvas configuration
        self.width = 500
        self.height = 500
        self.canvas = tk.Canvas(
            root, width=self.width, height=self.height, bg="#1e1e2e"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Robot face geometry
        self.cx = self.width // 2
        self.cy = self.height // 2
        self.face_size = 220

        # Eye parameters
        self.eye_offset_x = 50
        self.eye_offset_y = 35
        self.eye_rx = 28  # Horizontal eye radius
        self.eye_ry = 28  # Vertical eye radius (animates during blink)
        self.pupil_radius = 11
        self.max_pupil_travel = 14

        # State tracking
        self.proximity_threshold = 170
        self.current_state = "sad"
        self.is_blinking = False
        self.blink_scale = 1.0  # 1.0 = open, 0.05 = closed

        # Cursor position store
        self.mouse_x = self.cx
        self.mouse_y = self.cy

        self.setup_robot()

        # Bindings and animation loops
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.schedule_next_blink()

    def setup_robot(self):
        # Antenna
        self.canvas.create_line(
            self.cx,
            self.cy - self.face_size // 2,
            self.cx,
            self.cy - self.face_size // 2 - 30,
            width=6,
            fill="#89b4fa",
        )
        self.canvas.create_oval(
            self.cx - 10,
            self.cy - self.face_size // 2 - 40,
            self.cx + 10,
            self.cy - self.face_size // 2 - 20,
            fill="#f38ba8",
            outline="#89b4fa",
            width=3,
        )

        # Square Face
        half = self.face_size // 2
        self.canvas.create_rectangle(
            self.cx - half,
            self.cy - half,
            self.cx + half,
            self.cy + half,
            fill="#313244",
            outline="#89b4fa",
            width=6,
        )

        # Eye Sockets (Left & Right)
        self.left_eye_center = (
            self.cx - self.eye_offset_x,
            self.cy - self.eye_offset_y,
        )
        self.right_eye_center = (
            self.cx + self.eye_offset_x,
            self.cy - self.eye_offset_y,
        )

        lx, ly = self.left_eye_center
        rx, ry = self.right_eye_center

        self.left_eye_socket = self.canvas.create_oval(
            lx - self.eye_rx,
            ly - self.eye_ry,
            lx + self.eye_rx,
            ly + self.eye_ry,
            fill="#cdd6f4",
            outline="#89b4fa",
            width=3,
        )
        self.right_eye_socket = self.canvas.create_oval(
            rx - self.eye_rx,
            ry - self.eye_ry,
            rx + self.eye_rx,
            ry + self.eye_ry,
            fill="#cdd6f4",
            outline="#89b4fa",
            width=3,
        )

        # Pupils (Left & Right)
        self.left_pupil = self.canvas.create_oval(
            lx - self.pupil_radius,
            ly - self.pupil_radius,
            lx + self.pupil_radius,
            ly + self.pupil_radius,
            fill="#11111b",
        )
        self.right_pupil = self.canvas.create_oval(
            rx - self.pupil_radius,
            ry - self.pupil_radius,
            rx + self.pupil_radius,
            ry + self.pupil_radius,
            fill="#11111b",
        )

        # Mouth setup
        self.mouth_y = self.cy + 40
        self.mouth = self.canvas.create_arc(
            self.cx - 40,
            self.mouth_y,
            self.cx + 40,
            self.mouth_y + 50,
            start=0,
            extent=180,
            style=tk.ARC,
            width=6,
            outline="#f38ba8",
        )

    # ------------------ SOUND SYSTEM ------------------ #
    def play_sound_effect(self, sound_type):
        """Plays non-blocking audio cues on expression changes."""

        def _play():
            if sys.platform == "win32":
                import winsound

                if sound_type == "happy":
                    # Ascending major triad chirp
                    winsound.Beep(523, 90)  # C5
                    winsound.Beep(659, 90)  # E5
                    winsound.Beep(784, 130)  # G5
                elif sound_type == "sad":
                    # Descending moan tone
                    winsound.Beep(400, 100)
                    winsound.Beep(320, 100)
                    winsound.Beep(240, 180)
            else:
                # System bell fallback for non-Windows platforms
                self.root.bell()

        # Run sound in a background thread to prevent UI freezing
        threading.Thread(target=_play, daemon=True).start()

    # ------------------ BLINK ANIMATION ------------------ #
    def schedule_next_blink(self):
        """Schedules a random blink every 2.5 to 5.5 seconds."""
        delay_ms = random.randint(2500, 5500)
        self.root.after(delay_ms, self.trigger_blink)

    def trigger_blink(self):
        """Starts the eye-blink animation sequence."""
        if not self.is_blinking:
            self.is_blinking = True
            # Keyframe vertical scale factors: Open -> Half-closed -> Closed -> Half-closed -> Open
            sequence = [0.5, 0.05, 0.5, 1.0]
            self.animate_blink_step(sequence, 0)

    def animate_blink_step(self, sequence, index):
        if index < len(sequence):
            self.blink_scale = sequence[index]
            self.update_robot_graphics()
            # 35ms frame delay for smooth movement
            self.root.after(35, self.animate_blink_step, sequence, index + 1)
        else:
            self.is_blinking = False
            self.schedule_next_blink()

    # ------------------ INTERACTION & GRAPHICS ------------------ #
    def on_mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.update_robot_graphics()

    def update_robot_graphics(self):
        mx, my = self.mouse_x, self.mouse_y

        # 1. Redraw Eye Sockets scaled by vertical blink factor
        for center, socket_id in [
            (self.left_eye_center, self.left_eye_socket),
            (self.right_eye_center, self.right_eye_socket),
        ]:
            ex, ey = center
            curr_ry = max(1, int(self.eye_ry * self.blink_scale))
            self.canvas.coords(
                socket_id,
                ex - self.eye_rx,
                ey - curr_ry,
                ex + self.eye_rx,
                ey + curr_ry,
            )

        # 2. Update Pupils (Follow Cursor + Flatten/Hide during Blink)
        for center, pupil_id in [
            (self.left_eye_center, self.left_pupil),
            (self.right_eye_center, self.right_pupil),
        ]:
            ex, ey = center
            dx, dy = mx - ex, my - ey
            dist = math.hypot(dx, dy)

            if dist > 0:
                travel = min(dist, self.max_pupil_travel)
                offset_x = (dx / dist) * travel
                offset_y = (dy / dist) * travel
            else:
                offset_x, offset_y = 0, 0

            px, py = ex + offset_x, ey + offset_y

            # Hide pupil when eye is fully shut
            if self.blink_scale <= 0.1:
                self.canvas.itemconfig(pupil_id, state="hidden")
            else:
                self.canvas.itemconfig(pupil_id, state="normal")
                p_ry = max(1, int(self.pupil_radius * self.blink_scale))
                self.canvas.coords(
                    pupil_id,
                    px - self.pupil_radius,
                    py - p_ry,
                    px + self.pupil_radius,
                    py + p_ry,
                )

        # 3. Check Distance for State Change & Trigger Audio
        dist_from_robot = math.hypot(mx - self.cx, my - self.cy)
        new_state = (
            "happy" if dist_from_robot < self.proximity_threshold else "sad"
        )

        if new_state != self.current_state:
            self.current_state = new_state
            self.play_sound_effect(new_state)

        # 4. Render Mouth Expression
        if self.current_state == "happy":
            self.canvas.coords(
                self.mouth,
                self.cx - 40,
                self.mouth_y - 20,
                self.cx + 40,
                self.mouth_y + 35,
            )
            self.canvas.itemconfig(
                self.mouth, start=180, extent=180, outline="#a6e3a1"
            )
        else:
            self.canvas.coords(
                self.mouth,
                self.cx - 40,
                self.mouth_y,
                self.cx + 40,
                self.mouth_y + 50,
            )
            self.canvas.itemconfig(
                self.mouth, start=0, extent=180, outline="#f38ba8"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedSquareRobotApp(root)
    root.mainloop()