import random
import tkinter as tk
from tkinter import messagebox

class GuessTheNumberGUI:
    def __init__(self, master):
        self.master = master
        master.title("Guess the Number")

        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Range Selection
        self.range_frame = tk.Frame(self.master)
        self.range_frame.pack(pady=10)

        tk.Label(self.range_frame, text="Lower Bound:").grid(row=0, column=0, padx=5, pady=5)
        self.lower_entry = tk.Entry(self.range_frame)
        self.lower_entry.grid(row=0, column=1, padx=5, pady=5)
        self.lower_entry.insert(0, "1")

        tk.Label(self.range_frame, text="Upper Bound:").grid(row=0, column=2, padx=5, pady=5)
        self.upper_entry = tk.Entry(self.range_frame)
        self.upper_entry.grid(row=0, column=3, padx=5, pady=5)
        self.upper_entry.insert(0, "100")

        tk.Button(self.range_frame, text="Start Game", command=self.start_game).grid(row=0, column=4, padx=5, pady=5)

        # Guess Input
        self.guess_frame = tk.Frame(self.master)
        self.guess_frame.pack(pady=10)

        tk.Label(self.guess_frame, text="Your Guess:").grid(row=0, column=0, padx=5, pady=5)
        self.guess_entry = tk.Entry(self.guess_frame)
        self.guess_entry.grid(row=0, column=1, padx=5, pady=5)
        self.guess_entry.bind('<Return>', lambda event: self.check_guess())

        tk.Button(self.guess_frame, text="Submit Guess", command=self.check_guess).grid(row=0, column=2, padx=5, pady=5)

        # Feedback and Attempts
        self.feedback_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=5)

        self.attempts_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        # Restart Button
        self.restart_button = tk.Button(self.master, text="Restart Game", command=self.reset_game)
        self.restart_button.pack(pady=10)

    def start_game(self):
        try:
            self.lower_bound = int(self.lower_entry.get())
            self.upper_bound = int(self.upper_entry.get())
            if self.lower_bound >= self.upper_bound:
                messagebox.showerror("Invalid Range", "Lower bound must be less than upper bound.")
                return
            self.target_number = random.randint(self.lower_bound, self.upper_bound)
            self.max_attempts = 10
            self.attempts = 0
            self.update_attempts_label()
            self.feedback_label.config(text=f"Guess a number between {self.lower_bound} and {self.upper_bound}.")
            self.guess_entry.config(state='normal')
            self.guess_entry.focus_set()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for bounds.")

    def check_guess(self):
        if not hasattr(self, 'target_number'):
            messagebox.showwarning("Game Not Started", "Please start the game by setting the range.")
            return
        try:
            guess = int(self.guess_entry.get())
            if guess < self.lower_bound or guess > self.upper_bound:
                self.feedback_label.config(text=f"Please guess a number within {self.lower_bound} to {self.upper_bound}.")
                return
            self.attempts += 1
            remaining_attempts = self.max_attempts - self.attempts

            if guess < self.target_number:
                feedback = "Too low!"
            elif guess > self.target_number:
                feedback = "Too high!"
            else:
                feedback = f"Congratulations! You guessed it in {self.attempts} attempts."
                self.end_game(win=True)

            self.feedback_label.config(text=feedback)
            self.update_attempts_label()

            if guess == self.target_number:
                self.end_game(win=True)
            elif remaining_attempts <= 0:
                self.feedback_label.config(text=f"Sorry, you've used all attempts. The number was {self.target_number}.")
                self.end_game(win=False)

            self.guess_entry.delete(0, tk.END)

        except ValueError:
            self.feedback_label.config(text="Invalid input. Please enter an integer.")

    def update_attempts_label(self):
        remaining = self.max_attempts - self.attempts
        self.attempts_label.config(text=f"Remaining Attempts: {remaining}")

    def end_game(self, win):
        if win:
            messagebox.showinfo("Game Over", f"Congratulations! You guessed the number in {self.attempts} attempts.")
        else:
            messagebox.showinfo("Game Over", f"Sorry, you've used all attempts. The number was {self.target_number}.")
        self.guess_entry.config(state='disabled')

    def reset_game(self):
        self.target_number = None
        self.feedback_label.config(text="Set the range and start the game.")
        self.attempts_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheNumberGUI(root)
    root.mainloop()
