from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence
import os

class GIFMaker:
    def __init__(self):
        self.window = Tk()
        self.window.title("GIF Maker Pro")
        self.window.geometry("800x600")
        
        # UI Setup
        Label(self.window, text="🎬 GIF MAKER", font=("Arial", 24, "bold")).pack(pady=20)
        
        self.preview_frame = Frame(self.window, bg="white")
        self.preview_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = Canvas(self.preview_frame, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)
        
        # Buttons
        Button(self.window,
              text="🖼️ SELECT IMAGES",
              command=self.load_images,
              bg="#4CAF50",
              fg="white",
              font=("Arial", 12),
              padx=20,
              pady=10).pack(pady=10)
        
        self.save_btn = Button(self.window,
                             text="💾 SAVE GIF",
                             command=self.save_gif,
                             bg="#2196F3",
                             fg="white",
                             font=("Arial", 12),
                             padx=20,
                             pady=10,
                             state=DISABLED)
        self.save_btn.pack(pady=20)
        
        self.images = []
        self.gif_frames = []
        self.current_frame = 0
        self.window.mainloop()
    
    def load_images(self):
        """Load images and create animated preview"""
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if len(paths) < 2:
            messagebox.showerror("Error", "Select at least 2 images!")
            return
        
        self.images = []
        for path in paths:
            try:
                img = Image.open(path)
                self.images.append(img)
            except:
                print(f"Skipped {os.path.basename(path)}")
        
        if len(self.images) >= 2:
            self.create_animated_preview()
            self.save_btn.config(state=NORMAL)
    
    def create_animated_preview(self):
        """Generate and display animated preview"""
        # Create temp GIF
        temp_path = "temp_preview.gif"
        self.images[0].save(
            temp_path,
            save_all=True,
            append_images=self.images[1:],
            duration=300,
            loop=0
        )
        
        # Load frames for animation
        self.gif_frames = []
        gif = Image.open(temp_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.copy()
            frame.thumbnail((600, 400))  # Resize for preview
            self.gif_frames.append(ImageTk.PhotoImage(frame))
        
        # Start animation
        self.current_frame = 0
        self.animate_preview()
    
    def animate_preview(self):
        """Update GIF animation"""
        if self.gif_frames:
            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_width()//2,
                self.canvas.winfo_height()//2,
                image=self.gif_frames[self.current_frame]
            )
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.window.after(300, self.animate_preview)  # 300ms delay between frames
    
    def save_gif(self):
        """Save final GIF"""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif")]
        )
        if save_path:
            self.images[0].save(
                save_path,
                save_all=True,
                append_images=self.images[1:],
                duration=300,
                loop=0,
                optimize=True
            )
            messagebox.showinfo("Success", f"GIF saved to:\n{save_path}")

if __name__ == "__main__":
    GIFMaker()
