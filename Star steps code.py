import tkinter as tk
from tkinter import Canvas
from datetime import datetime
from PIL import Image, ImageTk
import os

class StarStepsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Steps")
        self.root.geometry("450x900")
        self.root.configure(bg='#C8E6ED')
        
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_minutes = 0
        self.timer_hours = 0
        self.current_task = "Make your bed"
        
        self.canvas = Canvas(root, width=450, height=900, bg='#C8E6ED', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.date_text_id = None
        self.time_text_id = None
        self.task_timer_id = None
        
        self.load_background()
        
        self.current_page = "home"
        self.draw_home_page()
        self.update_datetime()
        
    def load_background(self):
        self.bg_image = None
        self.task_bg_image = None
        try:
            if os.path.exists('star_steps_bg.png'):
                bg_img = Image.open('star_steps_bg.png')
                bg_img = bg_img.resize((450, 900), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(bg_img)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW, tags='background')
            else:
                self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='')
        except Exception as e:
            self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='')
        
        try:
            if os.path.exists('task_page_bg.png'):
                task_img = Image.open('task_page_bg.png')
                task_img = task_img.resize((450, 900), Image.Resampling.LANCZOS)
                self.task_bg_image = ImageTk.PhotoImage(task_img)
        except Exception as e:
            pass
    
    def clear_page(self):
        self.canvas.delete('page_content')
        self.canvas.delete('datetime')
        self.canvas.delete('button_bg')
        self.canvas.delete('button_text')
        self.canvas.delete('button_area')
        self.canvas.delete('task_start_bg')
        self.canvas.delete('task_start_text')
        self.canvas.delete('task_finish_bg')
        self.canvas.delete('task_finish_text')
        self.canvas.delete('task_next_bg')
        self.canvas.delete('task_next_text')
        
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
        self.canvas.delete('background')
        self.current_page = "home"
        
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW, tags='background')
        else:
            self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='', tags='background')
        
        self.date_text_id = self.canvas.create_text(225, 60, text="", font=('Railey', 26, 'bold'), fill='#FF8A80', justify='center', tags='datetime')
        self.time_text_id = self.canvas.create_text(225, 100, text="", font=('Nunito', 32, 'bold'), fill='#FF8A80', justify='center', tags='datetime')
        
        if not self.bg_image:
            self.canvas.create_text(225, 500, text="Star Steps", font=('Times New Roman', 56, 'bold'), fill='#FF9999', justify='center', tags='page_content')
            button_x, button_y = 125, 650
            button_width, button_height = 200, 70
            self.draw_rounded_button(button_x, button_y, button_width, button_height)
            self.canvas.create_text(button_x + button_width//2, button_y + button_height//2, text="Start The Day", font=('Times New Roman', 28, 'bold'), fill='#FF9999', tags='button_text')
        else:
            button_area = self.canvas.create_rectangle(100, 620, 350, 720, fill='', outline='', tags='button_area')
        
        for tag in ['button_bg', 'button_text', 'button_area']:
            self.canvas.tag_bind(tag, '<Button-1>', self.go_to_task_page)
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
    
    def draw_task_page(self):
        self.clear_page()
        self.canvas.delete('background')
        self.current_page = "task"
        
        if self.task_bg_image:
            self.canvas.create_image(0, 0, image=self.task_bg_image, anchor=tk.NW, tags='background')
            button_area_start = self.canvas.create_rectangle(125, 380, 325, 460, fill='', outline='', tags='task_start_bg')
            button_area_finish = self.canvas.create_rectangle(125, 650, 325, 730, fill='', outline='', tags='task_finish_bg')
            button_area_next = self.canvas.create_rectangle(100, 800, 350, 870, fill='', outline='', tags='task_next_bg')
        else:
            self.canvas.create_rectangle(0, 0, 450, 900, fill='#C8E6ED', outline='', tags='background')
            self.canvas.create_text(225, 200, text="Get up and make\nyou're bed", font=('Arial', 36, 'bold'), fill='#333333', justify='center', tags='page_content')
            start_btn_bg = self.draw_rounded_button(125, 380, 200, 80, radius=20, tag='task_start_bg')
            self.canvas.create_text(225, 420, text="Start", font=('Comic Sans MS', 42), fill='#FF9999', tags='task_start_text')
            finish_btn_bg = self.draw_rounded_button(125, 650, 200, 80, radius=20, tag='task_finish_bg')
            self.canvas.create_text(225, 690, text="Finish", font=('Comic Sans MS', 42), fill='#FF9999', tags='task_finish_text')
            next_btn_bg = self.draw_rounded_button(100, 800, 250, 70, radius=20, tag='task_next_bg')
            self.canvas.create_text(180, 835, text="Next Step", font=('Comic Sans MS', 32), fill='#FF9999', tags='task_next_text')
            self.canvas.create_text(310, 835, text="→", font=('Arial', 36, 'bold'), fill='#FF9999', tags='task_next_text')
        
        self.task_timer_id = self.canvas.create_text(225, 550, text="00:00:00", font=('Arial', 48, 'bold'), fill='#666666', tags='page_content')
        
        for tag in ['task_start_bg', 'task_start_text']:
            self.canvas.tag_bind(tag, '<Button-1>', self.start_task_timer)
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
        
        for tag in ['task_finish_bg', 'task_finish_text']:
            self.canvas.tag_bind(tag, '<Button-1>', self.finish_task_timer)
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
        
        for tag in ['task_next_bg', 'task_next_text']:
            self.canvas.tag_bind(tag, '<Button-1>', lambda e: self.draw_timer_page())
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
    
    def start_task_timer(self, event=None):
        if not self.timer_running:
            self.timer_running = True
            self.update_task_timer()
    
    def finish_task_timer(self, event=None):
        self.timer_running = False
    
    def update_task_timer(self):
        if self.timer_running and self.current_page == "task":
            self.timer_seconds += 1
            if self.timer_seconds >= 60:
                self.timer_seconds = 0
                self.timer_minutes += 1
            if self.timer_minutes >= 60:
                self.timer_minutes = 0
                self.timer_hours += 1
            time_str = f"{self.timer_hours:02d}:{self.timer_minutes:02d}:{self.timer_seconds:02d}"
            if self.task_timer_id:
                self.canvas.itemconfig(self.task_timer_id, text=time_str)
            self.root.after(1000, self.update_task_timer)
    
    def draw_timer_page(self):
        self.clear_page()
        self.current_page = "timer"
        
        self.canvas.create_rectangle(0, 0, 450, 150, fill='#FFB3BA', outline='', tags='page_content')
        self.canvas.create_text(225, 50, text="Daily Timer", font=('Times New Roman', 42, 'bold'), fill='white', tags='page_content')
        self.date_text_id = self.canvas.create_text(225, 100, text="", font=('Arial', 18), fill='white', tags='datetime')
        
        timer_bg_x, timer_bg_y = 75, 250
        timer_bg_width, timer_bg_height = 300, 200
        self.draw_rounded_button(timer_bg_x, timer_bg_y, timer_bg_width, timer_bg_height, radius=30, tag='page_content')
        self.timer_display_id = self.canvas.create_text(225, 350, text="00:00:00", font=('Arial', 56, 'bold'), fill='#FF6B6B', tags='page_content')
        
        button_y = 520
        button_width, button_height = 120, 60
        
        self.start_stop_btn_bg = self.draw_rounded_button(60, button_y, button_width, button_height, radius=15, tag='start_stop_bg')
        self.start_stop_btn_text = self.canvas.create_text(60 + button_width//2, button_y + button_height//2, text="Start", font=('Arial', 24, 'bold'), fill='#4CAF50', tags='start_stop_text')
        
        reset_btn_bg = self.draw_rounded_button(270, button_y, button_width, button_height, radius=15, tag='reset_bg')
        reset_btn_text = self.canvas.create_text(270 + button_width//2, button_y + button_height//2, text="Reset", font=('Arial', 24, 'bold'), fill='#FF6B6B', tags='reset_text')
        
        back_btn_bg = self.draw_rounded_button(165, 680, button_width, button_height, radius=15, tag='back_bg')
        back_btn_text = self.canvas.create_text(165 + button_width//2, 680 + button_height//2, text="← Back", font=('Arial', 24, 'bold'), fill='#666', tags='back_text')
        
        for tag in ['start_stop_bg', 'start_stop_text']:
            self.canvas.tag_bind(tag, '<Button-1>', self.toggle_timer)
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
        
        for tag in ['reset_bg', 'reset_text']:
            self.canvas.tag_bind(tag, '<Button-1>', self.reset_timer)
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
        
        for tag in ['back_bg', 'back_text']:
            self.canvas.tag_bind(tag, '<Button-1>', lambda e: self.draw_home_page())
            self.canvas.tag_bind(tag, '<Enter>', self.on_button_hover)
            self.canvas.tag_bind(tag, '<Leave>', self.on_button_leave)
    
    def toggle_timer(self, event=None):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.canvas.itemconfig(self.start_stop_btn_text, text="Stop", fill='#FF6B6B')
            self.update_timer()
        else:
            self.canvas.itemconfig(self.start_stop_btn_text, text="Start", fill='#4CAF50')
    
    def reset_timer(self, event=None):
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_minutes = 0
        self.timer_hours = 0
        self.canvas.itemconfig(self.timer_display_id, text="00:00:00")
        self.canvas.itemconfig(self.start_stop_btn_text, text="Start", fill='#4CAF50')
    
    def update_timer(self):
        if self.timer_running:
            self.timer_seconds += 1
            if self.timer_seconds >= 60:
                self.timer_seconds = 0
                self.timer_minutes += 1
            if self.timer_minutes >= 60:
                self.timer_minutes = 0
                self.timer_hours += 1
            time_str = f"{self.timer_hours:02d}:{self.timer_minutes:02d}:{self.timer_seconds:02d}"
            self.canvas.itemconfig(self.timer_display_id, text=time_str)
            self.root.after(1000, self.update_timer)
    
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
    
    def go_to_task_page(self, event):
        self.draw_task_page()
        
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
