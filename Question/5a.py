import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import itertools
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

tourist_spots = pd.DataFrame({
    "name": [
        "Pashupatinath Temple",
        "Swayambhunath Stupa",
        "Garden of Dreams",
        "Chandragiri Hills",
        "Kathmandu Durbar Square"
    ],
    "latitude": [27.7104, 27.7149, 27.7125, 27.6616, 27.7048],
    "longitude": [85.3488, 85.2906, 85.3170, 85.2458, 85.3076],
    "entry_fee": [100, 200, 150, 700, 100],
    "tags": [
        ["culture", "religious"],
        ["culture", "heritage"],
        ["nature", "relaxation"],
        ["nature", "adventure"],
        ["culture", "heritage"]
    ]
})

def distance(a, b):
    return math.sqrt(
        (a["latitude"] - b["latitude"]) ** 2 +
        (a["longitude"] - b["longitude"]) ** 2
    )

def greedy_itinerary(interests, budget, max_hours):
    selected = []
    total_cost = 0
    total_time = 0
    explanations = []

    remaining_spots = tourist_spots.copy()

    if len(remaining_spots) == 0:
        return selected, total_cost, total_time, explanations

    current_spot = remaining_spots.iloc[0]

    while True:
        best_spot = None
        best_score = -999999

        for _, row in remaining_spots.iterrows():
            if row["name"] in [spot["name"] for spot in selected]:
                continue

            travel_time = distance(current_spot, row) * 10
            visit_time = 1.0
            total_needed_time = travel_time + visit_time

            if total_cost + row["entry_fee"] > budget:
                continue

            if total_time + total_needed_time > max_hours:
                continue

            tag_match = len(set(interests) & set(row["tags"]))
            score = (tag_match * 10) - (travel_time * 2) - (row["entry_fee"] / 100)

            if score > best_score:
                best_score = score
                best_spot = row

        if best_spot is None:
            break

        travel_time = distance(current_spot, best_spot) * 10
        visit_time = 1.0
        total_needed_time = travel_time + visit_time

        selected.append(best_spot)
        total_cost += best_spot["entry_fee"]
        total_time += total_needed_time

        matched_tags = list(set(interests) & set(best_spot["tags"]))
        explanations.append(
            f"{best_spot['name']} selected because it matches {matched_tags} and fits within budget/time."
        )

        current_spot = best_spot

    return selected, total_cost, total_time, explanations

def brute_force(interests, budget, max_hours):
    best_route = []
    best_cost = 0
    best_time = 0
    best_score = -999999

    for perm in itertools.permutations(tourist_spots.index):
        route = []
        cost = 0
        time_used = 0
        score = 0

        current_spot = tourist_spots.iloc[perm[0]]

        for idx in perm:
            row = tourist_spots.loc[idx]
            travel_time = distance(current_spot, row) * 10
            visit_time = 1.0
            total_needed_time = travel_time + visit_time

            if cost + row["entry_fee"] > budget:
                continue
            if time_used + total_needed_time > max_hours:
                continue

            tag_match = len(set(interests) & set(row["tags"]))
            route.append(row)
            cost += row["entry_fee"]
            time_used += total_needed_time
            score += (tag_match * 10) - (travel_time * 2) - (row["entry_fee"] / 100)

            current_spot = row

        if len(route) > len(best_route) or (len(route) == len(best_route) and score > best_score):
            best_route = route
            best_cost = cost
            best_time = time_used
            best_score = score

    return best_route, best_cost, best_time

class TouristOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourist Spot Optimizer")
        self.root.geometry("1100x700")

        input_frame = ttk.LabelFrame(root, text="User Preferences", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame, text="Total Time Available (hours):").grid(row=0, column=0, sticky="w", pady=5)
        self.time_entry = ttk.Entry(input_frame)
        self.time_entry.grid(row=0, column=1, pady=5)
        self.time_entry.insert(0, "6")

        ttk.Label(input_frame, text="Maximum Budget (NPR):").grid(row=1, column=0, sticky="w", pady=5)
        self.budget_entry = ttk.Entry(input_frame)
        self.budget_entry.grid(row=1, column=1, pady=5)
        self.budget_entry.insert(0, "500")

        ttk.Label(input_frame, text="Select Interests:").grid(row=2, column=0, sticky="w", pady=5)

        self.interest_vars = {}
        interests = ["culture", "nature", "heritage", "adventure", "religious", "relaxation"]
        for i, interest in enumerate(interests):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(input_frame, text=interest, variable=var)
            chk.grid(row=2 + i // 3, column=1 + i % 3, sticky="w")
            self.interest_vars[interest] = var

        ttk.Button(input_frame, text="Generate Itinerary", command=self.generate_itinerary).grid(
            row=5, column=0, columnspan=2, pady=10
        )

        output_frame = ttk.LabelFrame(root, text="Results", padding=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.result_text = tk.Text(output_frame, height=15, width=70)
        self.result_text.pack(side="left", fill="both", expand=True)

        graph_frame = ttk.Frame(output_frame)
        graph_frame.pack(side="right", fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def generate_itinerary(self):
        try:
            max_hours = float(self.time_entry.get())
            budget = float(self.budget_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for time and budget.")
            return

        interests = [interest for interest, var in self.interest_vars.items() if var.get()]
        if not interests:
            messagebox.showerror("Input Error", "Please select at least one interest.")
            return

        heuristic_route, h_cost, h_time, explanations = greedy_itinerary(interests, budget, max_hours)
        brute_route, b_cost, b_time = brute_force(interests, budget, max_hours)

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "Heuristic Itinerary:\n")
        for i, spot in enumerate(heuristic_route, start=1):
            self.result_text.insert(
                tk.END,
                f"{i}. {spot['name']} | Fee: {spot['entry_fee']} | Tags: {', '.join(spot['tags'])}\n"
            )
            self.result_text.insert(tk.END, f"   {explanations[i-1]}\n")

        self.result_text.insert(tk.END, f"\nTotal Cost: NPR {h_cost}\n")
        self.result_text.insert(tk.END, f"Total Time: {h_time:.2f} hours\n")

        self.result_text.insert(tk.END, "\nBrute Force Best Route:\n")
        for i, spot in enumerate(brute_route, start=1):
            self.result_text.insert(
                tk.END,
                f"{i}. {spot['name']} | Fee: {spot['entry_fee']} | Tags: {', '.join(spot['tags'])}\n"
            )

        self.result_text.insert(tk.END, f"\nBrute Force Cost: NPR {b_cost}\n")
        self.result_text.insert(tk.END, f"Brute Force Time: {b_time:.2f} hours\n")

        self.result_text.insert(tk.END, "\nComparison Summary:\n")
        self.result_text.insert(tk.END, f"Spots Visited: Heuristic = {len(heuristic_route)}, Brute Force = {len(brute_route)}\n")
        self.result_text.insert(tk.END, f"Cost: Heuristic = NPR {h_cost}, Brute Force = NPR {b_cost}\n")
        self.result_text.insert(tk.END, f"Time: Heuristic = {h_time:.2f} hrs, Brute Force = {b_time:.2f} hrs\n")

        self.plot_route(heuristic_route)

    def plot_route(self, route):
        self.ax.clear()
        self.ax.set_title("Suggested Tourist Route")
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")

        if route:
            longitudes = [spot["longitude"] for spot in route]
            latitudes = [spot["latitude"] for spot in route]

            self.ax.plot(longitudes, latitudes, marker="o")

            for spot in route:
                self.ax.text(spot["longitude"], spot["latitude"], spot["name"], fontsize=8)

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = TouristOptimizerApp(root)
    root.mainloop()