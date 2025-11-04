import tkinter as tk
from tkinter import Canvas, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os
import time

class StarStepsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Steps")
        self.root.geometry("450x900")
        self.root.configure(bg='#C8E6ED')

        # Timer variables
        self.timer_running = False
        self.total_seconds = 2 * 60  # default 2 minutes
        self.current_step = 1

        # Canvas setup
        self.canvas = Canvas(root, width=450, height=900, bg='#C8E6ED', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Text IDs
        self.date_text_id = None
        self.time_text_id = None
        self.timer_display_id = None

        # Images
        self.bg_image = None
        self.task_bg_image = None
        self.final_image = None
        self.final_step_image = None
        self.load_background()

        # Pages
        self.current_page = "home"
        self.draw_home_page()
        self.update_datetime()

    def load_background(self):
        try:
            if os.path.exists('star_steps_bg.png'):
                bg_img = Image.open('star_steps_bg.png').resize((450, 900), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(bg_img)
            if os.path.exists('task_page_bg.png'):
                task_img = Image.open('task_page_bg.png').resize((450, 900), Image.Resampling.LANCZOS)
                self.task_bg_image = ImageTk.PhotoImage(task_img)
            if os.path.exists('StarSteps2.png'):
                final_img = Image.open('StarSteps2.png').resize((450, 900), Image.Resampling.LANCZOS)
                self.final_image = ImageTk.PhotoImage(final_img)
            if os.path.exists('StarStep3.png'):
                final_step_img = Image.open('StarStep3.png').resize((450, 900), Image.Resampling.LANCZOS)
                self.final_step_image = ImageTk.PhotoImage(final_step_img)
        except Exception as e:
            print("Image load error:", e)

    def clear_page(self):
        self.canvas.delete('all')

    def draw_rounded_button(self, x, y, width, height, radius=50, tag='button_bg'):
        points = [
            x + radius, y,
            x + width - radius, y,
            x + width, y,
            x + width, y + radius,
            x + width, y + height - radius,
            x + width, y + height,
            x + width - radius, y + height,
            x + radius, y + height,
            x, y + height,
            x, y + height - radius,
            x, y + radius,
            x, y
        ]
        return self.canvas.create_polygon(points, fill='white', outline='', smooth=True, tags=tag)

    def draw_home_page(self):
        self.clear_page()
        self.current_page = "home"
        self.current_step = 1  # Reset to step 1

        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)
        else:
            self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='')

        self.date_text_id = self.canvas.create_text(225, 60, text="", font=('Railey', 26, 'bold'), fill='#FF8A80', justify='center')
        self.time_text_id = self.canvas.create_text(225, 100, text="", font=('Nunito', 32, 'bold'), fill='#FF8A80', justify='center')

        button_x, button_y = 125, 650
        button_width, button_height = 200, 70
        self.draw_rounded_button(button_x, button_y, button_width, button_height)
        self.canvas.create_text(button_x + button_width // 2, button_y + button_height // 2, text="Start The Day",
                                font=('Times New Roman', 28, 'bold'), fill='#FF9999', tags='start_text')

        self.canvas.tag_bind('start_text', '<Button-1>', lambda e: self.draw_timer_page())
        self.canvas.tag_bind('start_text', '<Enter>', self.on_button_hover)
        self.canvas.tag_bind('start_text', '<Leave>', self.on_button_leave)

    def draw_timer_page(self):
        self.clear_page()
        self.current_page = "timer"

        self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='')

        self.date_text_id = self.canvas.create_text(225, 50, text="", font=('Arial', 20, 'bold'), fill='#FF8A80')
        self.time_text_id = self.canvas.create_text(225, 85, text="", font=('Arial', 24, 'bold'), fill='#FF8A80')

        task_data = {
            1: ("Wake Up & Make Your Bed", 5),
            2: ("Time to Brush Your Teeth\n& Wash Your Face", 5),
            3: ("Get Dressed", 5),
            4: ("Have Breakfast", 20),
            5: ("Pack All School Supplies,\nLunch Box & Water Bottle\nIn Your School Bag", 5),
            6: ("Time for School", 360),
            7: ("Dinner is Finished,\nTime To Have A Shower", 5),
            8: ("Brush Your Teeth", 2),
            9: ("Lay Out Your Clothes &\nBackPack For The Next Day", 5),
            10: ("Read Together", 15),
            11: ("Go To Bed", 0)
        }
        
        task_text, timer_minutes = task_data.get(self.current_step, ("", 2))
        self.total_seconds = timer_minutes * 60
        
        self.canvas.create_text(225, 200, text=task_text, font=('Arial', 32, 'bold'), fill='#FF8A80', justify='center')

        if self.current_step == 11:
            next_btn_bg = self.draw_rounded_button(125, 400, 200, 60, radius=15)
            next_btn_text = self.canvas.create_text(225, 430, text="Finish", font=('Arial', 24, 'bold'), fill='#666',
                                                   tags='finish_text')
            self.canvas.tag_bind('finish_text', '<Button-1>', self.go_to_next_step)
        else:
            self.draw_rounded_button(80, 280, 300, 200, radius=30)
            self.timer_display_id = self.canvas.create_text(225, 390, text=self.format_time(self.total_seconds),
                                                            font=('Arial', 56, 'bold'), fill='#FF6B6B')

            button_y = 610
            button_width, button_height = 120, 60

            self.start_stop_btn_bg = self.draw_rounded_button(60, button_y, button_width, button_height, radius=15)
            self.start_stop_btn_text = self.canvas.create_text(60 + button_width // 2, button_y + button_height // 2,
                                                               text="Start", font=('Arial', 24, 'bold'), fill='#4CAF50',
                                                               tags='start_stop_text')

            reset_btn_bg = self.draw_rounded_button(270, button_y, button_width, button_height, radius=15)
            reset_btn_text = self.canvas.create_text(270 + button_width // 2, button_y + button_height // 2,
                                                     text="Reset", font=('Arial', 24, 'bold'), fill='#FF6B6B',
                                                     tags='reset_text')

            next_btn_bg = self.draw_rounded_button(125, 750, 200, 60, radius=15)
            next_btn_text = self.canvas.create_text(225, 780, text="Next Step →", font=('Arial', 24, 'bold'), fill='#666',
                                                   tags='next_text')

            self.canvas.tag_bind('start_stop_text', '<Button-1>', self.toggle_timer)
            self.canvas.tag_bind('reset_text', '<Button-1>', self.reset_timer)
            self.canvas.tag_bind('next_text', '<Button-1>', self.go_to_next_step)

    def draw_final_page(self):
        self.clear_page()
        self.current_page = "final"
        
        if self.final_image:
            self.canvas.create_image(0, 0, image=self.final_image, anchor=tk.NW)
        else:
            self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='')
            self.canvas.create_text(225, 450, text="Well Done!", font=('Arial', 36, 'bold'), fill='#FF8A80')

        # Add Next Step button on StarSteps2 page
        next_btn_bg = self.draw_rounded_button(125, 750, 200, 60, radius=15)
        next_btn_text = self.canvas.create_text(225, 780, text="Next Step →", font=('Arial', 24, 'bold'), 
                                               fill='#FF9999', tags='final_next_text')
        
        self.canvas.tag_bind('final_next_text', '<Button-1>', self.draw_final_step_page)
        self.canvas.tag_bind('final_next_text', '<Enter>', self.on_button_hover)
        self.canvas.tag_bind('final_next_text', '<Leave>', self.on_button_leave)

    def draw_final_step_page(self, event=None):
        self.clear_page()
        self.current_page = "final_step"
        
        if self.final_step_image:
            self.canvas.create_image(0, 0, image=self.final_step_image, anchor=tk.NW)
        else:
            self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='')
            self.canvas.create_text(225, 450, text="Congratulations!", font=('Arial', 36, 'bold'), fill='#FF8A80')

        # Add Next Step button on StarStep3 page - continues to evening routine
        next_btn_bg = self.draw_rounded_button(125, 750, 200, 60, radius=15)
        next_btn_text = self.canvas.create_text(225, 780, text="Next Step →", font=('Arial', 24, 'bold'), 
                                               fill='#FF9999', tags='end_next_text')
        
        self.canvas.tag_bind('end_next_text', '<Button-1>', self.start_evening_routine)
        self.canvas.tag_bind('end_next_text', '<Enter>', self.on_button_hover)
        self.canvas.tag_bind('end_next_text', '<Leave>', self.on_button_leave)

    def start_evening_routine(self, event=None):
        self.current_step = 7  # Start evening routine at step 7
        self.timer_running = False
        self.draw_timer_page()

    #Timer Functions
    def toggle_timer(self, event=None):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.canvas.itemconfig(self.start_stop_btn_text, text="Stop", fill='#FF6B6B')
            self.run_timer()
        else:
            self.canvas.itemconfig(self.start_stop_btn_text, text="Start", fill='#4CAF50')

    def reset_timer(self, event=None):
        self.timer_running = False
        # Reset to the appropriate time for current step
        task_data = {
            1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2,
            7: 5, 8: 2, 9: 5, 10: 15, 11: 2
        }
        timer_minutes = task_data.get(self.current_step, 2)
        self.total_seconds = timer_minutes * 60
        self.canvas.itemconfig(self.timer_display_id, text=self.format_time(self.total_seconds))
        self.canvas.itemconfig(self.start_stop_btn_text, text="Start", fill='#4CAF50')

    def run_timer(self):
        if self.timer_running and self.total_seconds > 0:
            self.total_seconds -= 1
            self.canvas.itemconfig(self.timer_display_id, text=self.format_time(self.total_seconds))
            self.root.after(1000, self.run_timer)
        elif self.total_seconds <= 0:
            self.timer_running = False
            self.canvas.itemconfig(self.start_stop_btn_text, text="Start", fill='#4CAF50')
            messagebox.showinfo("Time Countdown", "Time's up!")

    def format_time(self, total_seconds):
        mins, secs = divmod(total_seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02d}:{mins:02d}:{secs:02d}" if hours > 0 else f"{mins:02d}:{secs:02d}"

    # Navigation & Date/Time Updates
    def update_datetime(self):
        now = datetime.now()
        if self.current_page == "home":
            date_str = now.strftime("%B %d, %Y")
            time_str = now.strftime("%I:%M:%S %p")
            if self.date_text_id:
                self.canvas.itemconfig(self.date_text_id, text=date_str)
            if self.time_text_id:
                self.canvas.itemconfig(self.time_text_id, text=time_str)
        elif self.current_page == "timer":
            datetime_str = now.strftime("%B %d, %Y • %I:%M %p")
            if self.date_text_id:
                self.canvas.itemconfig(self.date_text_id, text=datetime_str)
        self.root.after(1000, self.update_datetime)

    def go_to_next_step(self, event=None):
        self.current_step += 1
        
        if self.current_step == 7:
            # After step 6, show StarSteps2
            self.draw_final_page()
        elif self.current_step == 12:
            # After step 11 (Go To Bed), loop back to home
            self.draw_home_page()
        else:
            self.timer_running = False
            self.draw_timer_page()

    def on_button_hover(self, event):
        self.root.config(cursor='hand2')

    def on_button_leave(self, event):
        self.root.config(cursor='')

def main():
    root = tk.Tk()
    app = StarStepsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
