import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

APP_NAME = "Bloom & Bliss | Flower Bouquet Maker"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
RECEIPTS_DIR = os.path.join(BASE_DIR, "receipts")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(RECEIPTS_DIR, exist_ok=True)


# ============================================================
# 2. COLORS
# ============================================================

COLORS = {
    "plum": "#79365F",
    "plum_dark": "#5B2448",
    "pink": "#F8E7F0",
    "pink_light": "#FFF8FB",
    "pink_mid": "#EAC8D9",
    "magenta": "#A63C89",
    "text": "#332833",
    "muted": "#877985",
    "white": "#FFFFFF",
    "green": "#16866B",
    "border": "#EADDE5",
    "gold": "#DDA84B",
}


# ============================================================
# 3. FLOWER DATA
# ============================================================

FLOWERS = {
    "Rose": {
        "price": 50,
        "image": "rose",
        "emoji": "🌹",
    },
    "Tulip": {
        "price": 60,
        "image": "Tulip",
        "emoji": "🌷",
    },
    "Sunflower": {
        "price": 70,
        "image": "sunflower",
        "emoji": "🌻",
    },
    "Lily": {
        "price": 80,
        "image": "lily",
        "emoji": "🌺",
    },
    "Daisy": {
        "price": 40,
        "image": "Daisy",
        "emoji": "🌼",
    },
    "Orchid": {
        "price": 90,
        "image": "orchid",
        "emoji": "🪻",
    },
}


# ============================================================
# 4. WRAPPING OPTIONS
# ============================================================

WRAPPINGS = {
    "Classic Paper": {
        "price": 50,
        "color": "#F7C7D6",
        "emoji": "🎀",
    },
    "Jute Wrap": {
        "price": 70,
        "color": "#D6B58D",
        "emoji": "🌾",
    },
    "Mesh Wrap": {
        "price": 60,
        "color": "#D6C9F2",
        "emoji": "🪻",
    },
    "Luxury Box": {
        "price": 100,
        "color": "#3B3035",
        "emoji": "🎁",
    },
}


# ============================================================
# 5. ADD-ONS
# ============================================================

ADD_ONS = {
    "Greeting Card": {
        "price": 30,
        "emoji": "💌",
    },
    "Chocolates": {
        "price": 80,
        "emoji": "🍫",
    },
    "Teddy Bear": {
        "price": 150,
        "emoji": "🧸",
    },
    "LED Lights": {
        "price": 50,
        "emoji": "✨",
    },
}


# ============================================================
# 6. FIND FLOWER IMAGES
# ============================================================

def find_image(filename):
    """Find an image by filename, ignoring case and extension."""

    if not os.path.isdir(ASSETS_DIR):
        return None

    target_name = os.path.splitext(filename)[0].lower()

    for actual_file in os.listdir(ASSETS_DIR):
        name, extension = os.path.splitext(actual_file) 

        if (
            name.lower() == target_name
            and extension.lower() in (
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
            )
        ):
            return os.path.join(ASSETS_DIR, actual_file)

    return None


# ============================================================
# 7. MAIN APPLICATION
# ============================================================

class BouquetMaker:

    def __init__(self, root):

        self.root = root

        self.root.title(APP_NAME)
        self.root.geometry("1180x790")
        self.root.minsize(1000, 700)
        self.root.configure(bg=COLORS["pink_light"])

        # Flower quantities
        self.quantities = {
            name: tk.IntVar(value=0)
            for name in FLOWERS
        }

        # Wrapping selection
        self.selected_wrapping = tk.StringVar(
            value="Classic Paper"
        )

        # Add-ons selection
        self.selected_addons = {
            name: tk.BooleanVar(value=False)
            for name in ADD_ONS
        }

        # Customer details
        self.customer_name = tk.StringVar()
        self.phone = tk.StringVar()
        self.address = tk.StringVar()

        self.delivery = tk.StringVar(
            value="Home Delivery"
        )

        self.greeting = tk.StringVar(
            value="Wishing you a beautiful day!"
        )

        self.photos = {}
        self.current_page = "home"

        self.build_header()
        self.build_main_area()
        self.build_footer()

        self.render_page("home")


    # ========================================================
    # 8. HEADER
    # ========================================================

    def build_header(self):

        self.header = tk.Frame(
            self.root,
            bg=COLORS["white"],
            height=82,
        )

        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        brand = tk.Frame(
            self.header,
            bg=COLORS["white"],
        )

        brand.pack(
            side="left",
            padx=24,
            pady=12,
        )

        tk.Label(
            brand,
            text="✿  Bloom & Bliss",
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 22, "bold"),
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="FLOWERS FOR YOUR SPECIAL MOMENTS",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Arial", 8, "bold"),
        ).pack(
            anchor="w",
            padx=35,
        )

        tk.Label(
            self.header,
            text="Fresh flowers  •  Beautiful bouquets  •  Made with love",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Arial", 10),
        ).pack(
            side="right",
            padx=20,
        )


    # ========================================================
    # 9. MAIN AREA
    # ========================================================

    def build_main_area(self):

        self.step_bar = tk.Frame(
            self.root,
            bg=COLORS["pink_light"],
        )

        self.step_bar.pack(
            fill="x",
            padx=24,
            pady=(8, 0),
        )

        self.page_area = tk.Frame(
            self.root,
            bg=COLORS["pink_light"],
        )

        self.page_area.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=10,
        )


    # ========================================================
    # 10. FOOTER
    # ========================================================

    def build_footer(self):

        tk.Label(
            self.root,
            text="Made with love  ♥  Bloom & Bliss Flower Studio",
            bg=COLORS["pink_light"],
            fg="#A58A9C",
            font=("Arial", 8),
        ).pack(pady=(0, 5))


    # ========================================================
    # 11. BUTTON CREATION
    # ========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        primary=True,
        **kwargs,
    ):

        if primary:
            background = COLORS["plum"]
            foreground = COLORS["white"]
            active_background = COLORS["plum_dark"]
        else:
            background = COLORS["white"]
            foreground = COLORS["plum"]
            active_background = COLORS["pink"]

        options = {
            "bg": background,
            "fg": foreground,
            "activebackground": active_background,
            "activeforeground": foreground,
            "font": ("Arial", 10, "bold"),
            "relief": "flat",
            "bd": 0,
            "padx": 16,
            "pady": 9,
            "cursor": "hand2",
            "takefocus": True,
        }

        # Custom button settings override defaults.
        options.update(kwargs)

        return tk.Button(
            parent,
            text=text,
            command=command,
            **options,
        )


    # ========================================================
    # 12. PAGE MANAGEMENT
    # ========================================================

    def clear_page(self):

        for widget in self.step_bar.winfo_children():
            widget.destroy()

        for widget in self.page_area.winfo_children():
            widget.destroy()

        self.photos.clear()


    def render_page(self, page):

        self.current_page = page


        # Hide the normal header on the home screen.
        # Show it again on the remaining pages.
        if page == "home":
            self.header.pack_forget()

        else:
            if not self.header.winfo_manager():
                self.header.pack(
                    fill="x",
                    before=self.step_bar,
                )

        self.clear_page()
        self.draw_steps(page)

        if page == "home":
            self.render_home()

        elif page == "flowers":
            self.render_flowers()

        elif page == "wrapping":
            self.render_wrapping()

        elif page == "order":
            self.render_order()


    def draw_steps(self, active_page):

        if active_page == "home":
            return

        steps = [
            ("flowers", "1", "Select Flowers"),
            ("wrapping", "2", "Wrapping & Add-ons"),
            ("order", "3", "Preview & Order"),
        ]

        for page, number, title in steps:

            active = page == active_page

            background = (
                COLORS["plum"]
                if active
                else COLORS["white"]
            )

            foreground = (
                COLORS["white"]
                if active
                else COLORS["muted"]
            )

            item = tk.Frame(
                self.step_bar,
                bg=background,
            )

            item.pack(
                side="left",
                fill="x",
                expand=True,
                padx=4,
            )

            tk.Label(
                item,
                text=f"{number}   {title}",
                bg=background,
                fg=foreground,
                font=(
                    "Arial",
                    10,
                    "bold" if active else "normal",
                ),
                pady=10,
            ).pack(fill="x")


    # ========================================================
    # 13. PAGE HEADING
    # ========================================================

    def heading(self, parent, title, subtitle):

        tk.Label(
            parent,
            text=title,
            bg=COLORS["pink_light"],
            fg=COLORS["plum"],
            font=("Georgia", 21, "bold"),
        ).pack(anchor="w")

        tk.Label(
            parent,
            text=subtitle,
            bg=COLORS["pink_light"],
            fg=COLORS["muted"],
            font=("Arial", 10),
        ).pack(
            anchor="w",
            pady=(3, 12),
        )


    # ========================================================
    # 14. LOAD FLOWER PICTURES
    # ========================================================

    def load_photo(self, flower, size=(125, 85)):

        if Image is None or ImageTk is None:
            return None

        filename = FLOWERS[flower]["image"]
        path = find_image(filename)

        if path is None:
            return None

        key = (path, size)

        if key in self.photos:
            return self.photos[key]

        try:
            image = Image.open(path).convert("RGB")

            resampling = getattr(
                Image,
                "Resampling",
                Image,
            )

            image.thumbnail(
                size,
                resampling.LANCZOS,
            )

            background = Image.new(
                "RGB",
                size,
                "white",
            )

            x = (size[0] - image.width) // 2
            y = (size[1] - image.height) // 2

            background.paste(
                image,
                (x, y),
            )

            photo = ImageTk.PhotoImage(background)

            self.photos[key] = photo

            return photo

        except (OSError, ValueError, AttributeError) as error:

            print(
                f"Unable to load image for {flower}: {error}"
            )

            return None


    def add_flower_image(
        self,
        parent,
        flower,
        size=(125, 85),
    ):

        photo = self.load_photo(flower, size)

        if photo is not None:

            label = tk.Label(
                parent,
                image=photo,
                bg=COLORS["white"],
            )

            # Keep a reference to prevent image disappearance.
            label.image = photo

            return label

        return tk.Label(
            parent,
            text=FLOWERS[flower]["emoji"],
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Arial", 38),
            width=6,
            height=2,
        )


    # ========================================================
    # 15. HOME SCREEN
    # ========================================================

    # ========================================================
    # 15. HOME SCREEN - REFERENCE-INSPIRED DESIGN
    # ========================================================

    def render_home(self):

        # Main home screen background
        home = tk.Frame(
            self.page_area,
            bg="#FFF0F6",
        )

        home.pack(
            fill="both",
            expand=True,
        )

        # ----------------------------------------------------
        # TOP TITLE BANNER
        # ----------------------------------------------------

        banner = tk.Frame(
            home,
            bg="#F8DDEB",
            height=112,
        )

        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="❀  ✿  ❀",
            font=("Georgia", 15),
            bg="#F8DDEB",
            fg="#A63C89",
        ).place(
            x=12,
            y=8,
        )

        tk.Label(
            banner,
            text="❀  ✿  ❀",
            font=("Georgia", 15),
            bg="#F8DDEB",
            fg="#A63C89",
        ).place(
            relx=1.0,
            x=-12,
            y=8,
            anchor="ne",
        )

        tk.Label(
            banner,
            text="Flower Bouquet Maker",
            font=("Segoe Script", 27, "bold"),
            bg="#F8DDEB",
            fg="#84316F",
        ).place(
            relx=0.5,
            y=15,
            anchor="n",
        )

        tk.Label(
            banner,
            text="Fresh Flowers   •   Beautiful Bouquets   •   Special Moments",
            font=("Arial", 10),
            bg="#F8DDEB",
            fg="#65465D",
        ).place(
            relx=0.5,
            y=69,
            anchor="n",
        )

        # ----------------------------------------------------
        # TWO-COLUMN CONTENT
        # ----------------------------------------------------

        content = tk.Frame(
            home,
            bg="#FFF0F6",
        )

        content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        content.grid_columnconfigure(0, weight=1, uniform="home_columns")
        content.grid_columnconfigure(1, weight=1, uniform="home_columns")
        content.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # LEFT: LARGE BOUQUET IMAGE CARD
        # ----------------------------------------------------

        image_panel = tk.Frame(
            content,
            bg="#FFFFFF",
            highlightbackground="#E8C4D8",
            highlightthickness=1,
        )

        image_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8),
        )

        tk.Label(
            image_panel,
            text="A bouquet made with love",
            font=("Georgia", 16, "bold"),
            bg="#FFFFFF",
            fg="#84316F",
        ).pack(
            pady=(12, 2),
        )

        tk.Label(
            image_panel,
            text="Fresh flowers for your special someone",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#998393",
        ).pack(
            pady=(0, 6),
        )

        # The Rose asset is used as the hero image. If it is not
        # found, add_flower_image displays a rose emoji instead.
        hero_image = self.add_flower_image(
            image_panel,
            "Rose",
            (340, 300),
        )

        hero_image.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=4,
        )

        tk.Label(
            image_panel,
            text="For You  ♡",
            font=("Segoe Script", 17, "bold"),
            bg="#FFFFFF",
            fg="#A63C89",
        ).pack(
            pady=(3, 0),
        )

        tk.Label(
            image_panel,
            text="Because every flower tells a story...",
            font=("Georgia", 10, "italic"),
            bg="#FFFFFF",
            fg="#8B7184",
        ).pack(
            pady=(0, 10),
        )

        # ----------------------------------------------------
        # RIGHT: WELCOME TEXT AND NAVIGATION BUTTONS
        # ----------------------------------------------------

        right_panel = tk.Frame(
            content,
            bg="#FFF0F6",
        )

        right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0),
        )

        tk.Label(
            right_panel,
            text="Welcome to Bloom & Bliss",
            font=("Georgia", 21, "bold"),
            bg="#FFF0F6",
            fg="#84316F",
            wraplength=440,
            justify="center",
        ).pack(
            pady=(24, 6),
        )

        tk.Label(
            right_panel,
            text=(
                "Design a bouquet as unique as your special someone.\n"
                "Choose beautiful flowers, add elegant wrapping,\n"
                "and make every moment memorable."
            ),
            font=("Arial", 10),
            bg="#FFF0F6",
            fg="#806E7D",
            wraplength=430,
            justify="center",
        ).pack(
            padx=10,
            pady=(0, 16),
        )

        # Feature list card
        feature_card = tk.Frame(
            right_panel,
            bg="#FFFFFF",
            highlightbackground="#E8C4D8",
            highlightthickness=1,
        )

        feature_card.pack(
            fill="x",
            padx=10,
            pady=(0, 16),
        )

        feature_items = [
            "✿   Choose your favourite fresh flowers",
            "✿   Add a beautiful wrap and little extras",
            "✿   Preview your bouquet and place your order",
        ]

        for item in feature_items:
            tk.Label(
                feature_card,
                text=item,
                font=("Arial", 9),
                bg="#FFFFFF",
                fg="#65465D",
                anchor="w",
                wraplength=380,
                justify="left",
                padx=12,
                pady=8,
            ).pack(fill="x")

        # Primary button
        self.make_button(
            right_panel,
            "✿   Create New Bouquet   →",
            lambda: self.render_page("flowers"),
            padx=20,
            pady=11,
        ).pack(
            fill="x",
            padx=32,
            pady=(2, 7),
        )

        # Secondary buttons
        self.make_button(
            right_panel,
            "◷   View Order History",
            self.show_history,
            primary=False,
            padx=18,
            pady=9,
        ).pack(
            fill="x",
            padx=32,
            pady=4,
        )

        self.make_button(
            right_panel,
            "♡   About Bloom & Bliss",
            self.show_about,
            primary=False,
            padx=18,
            pady=9,
        ).pack(
            fill="x",
            padx=32,
            pady=4,
        )

        self.make_button(
            right_panel,
            "✕   Exit",
            self.root.destroy,
            primary=False,
            padx=18,
            pady=9,
        ).pack(
            fill="x",
            padx=32,
            pady=4,
        )

    # ========================================================
    # 16. SUMMARY PANEL
    # ========================================================

    def create_panel(self, parent, title):

        panel = tk.Frame(
            parent,
            bg=COLORS["white"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )

        tk.Label(
            panel,
            text=title,
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 15, "bold"),
        ).pack(
            anchor="w",
            padx=13,
            pady=(12, 8),
        )

        return panel


    def flower_count(self):

        return sum(
            variable.get()
            for variable in self.quantities.values()
        )


    def flower_subtotal(self):

        return sum(
            self.quantities[name].get() * data["price"]
            for name, data in FLOWERS.items()
        )


    def wrapping_cost(self):

        return WRAPPINGS[
            self.selected_wrapping.get()
        ]["price"]


    def addon_total(self):

        return sum(
            data["price"]
            for name, data in ADD_ONS.items()
            if self.selected_addons[name].get()
        )


    def grand_total(self):

        return (
            self.flower_subtotal()
            + self.wrapping_cost()
            + self.addon_total()
        )


    def update_summary(self):

        if (
            not hasattr(self, "summary_panel")
            or not self.summary_panel.winfo_exists()
        ):
            return

        for widget in self.summary_panel.winfo_children():
            widget.destroy()

        tk.Label(
            self.summary_panel,
            text="Your selection",
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 15, "bold"),
        ).pack(
            anchor="w",
            padx=13,
            pady=(12, 8),
        )

        tk.Label(
            self.summary_panel,
            text=f"Flowers selected: {self.flower_count()}",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Arial", 9),
        ).pack(
            anchor="w",
            padx=13,
            pady=3,
        )

        for name, data in FLOWERS.items():

            quantity = self.quantities[name].get()

            if quantity > 0:

                tk.Label(
                    self.summary_panel,
                    text=(
                        f"{name} × {quantity}    "
                        f"₹{quantity * data['price']}"
                    ),
                    bg=COLORS["white"],
                    fg=COLORS["text"],
                    font=("Arial", 9),
                ).pack(
                    anchor="w",
                    padx=13,
                    pady=3,
                )

        ttk.Separator(
            self.summary_panel,
        ).pack(
            fill="x",
            padx=12,
            pady=7,
        )

        tk.Label(
            self.summary_panel,
            text=f"Wrapping: ₹{self.wrapping_cost()}",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Arial", 9),
        ).pack(
            anchor="w",
            padx=13,
            pady=3,
        )

        tk.Label(
            self.summary_panel,
            text=f"Add-ons: ₹{self.addon_total()}",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Arial", 9),
        ).pack(
            anchor="w",
            padx=13,
            pady=3,
        )

        ttk.Separator(
            self.summary_panel,
        ).pack(
            fill="x",
            padx=12,
            pady=7,
        )

        tk.Label(
            self.summary_panel,
            text="TOTAL AMOUNT",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Arial", 9, "bold"),
        ).pack(
            anchor="w",
            padx=13,
        )

        tk.Label(
            self.summary_panel,
            text=f"₹{self.grand_total()}",
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 24, "bold"),
        ).pack(
            anchor="w",
            padx=13,
            pady=(0, 12),
        )


    # ========================================================
    # 17. FLOWER SELECTION PAGE
    # ========================================================

    def render_flowers(self):

        self.heading(
            self.page_area,
            "Choose your flowers",
            "Choose flowers and quantities for your perfect bouquet.",
        )

        layout = tk.Frame(
            self.page_area,
            bg=COLORS["pink_light"],
        )

        layout.pack(
            fill="both",
            expand=True,
        )

        layout.grid_columnconfigure(
            0,
            weight=1,
        )

        layout.grid_columnconfigure(
            1,
            weight=0,
        )

        layout.grid_rowconfigure(
            0,
            weight=1,
        )

        # Flower grid.
        grid = tk.Frame(
            layout,
            bg=COLORS["pink_light"],
        )

        grid.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12),
        )

        for column in range(3):

            grid.grid_columnconfigure(
                column,
                weight=1,
                uniform="flowers",
            )

        for row in range(2):

            grid.grid_rowconfigure(
                row,
                weight=1,
                uniform="flowers",
            )

        # Create all six flower cards.
        for index, (name, data) in enumerate(FLOWERS.items()):

            card = tk.Frame(
                grid,
                bg=COLORS["white"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
            )

            card.grid(
                row=index // 3,
                column=index % 3,
                padx=5,
                pady=5,
                sticky="nsew",
            )

            self.add_flower_image(
                card,
                name,
                (110, 72),
            ).pack(
                pady=(6, 2),
            )

            tk.Label(
                card,
                text=name,
                bg=COLORS["white"],
                fg=COLORS["plum"],
                font=("Arial", 11, "bold"),
            ).pack()

            tk.Label(
                card,
                text=f"₹{data['price']} / stem",
                bg=COLORS["white"],
                fg=COLORS["muted"],
                font=("Arial", 9),
            ).pack(
                pady=(2, 5),
            )

            # Quantity buttons.
            quantity_row = tk.Frame(
                card,
                bg=COLORS["white"],
            )

            quantity_row.pack(
                pady=(0, 8),
            )

            self.make_button(
                quantity_row,
                "−",
                lambda n=name: self.change_quantity(n, -1),
                primary=False,
                padx=10,
                pady=3,
            ).pack(
                side="left",
                padx=3,
            )

            tk.Label(
                quantity_row,
                textvariable=self.quantities[name],
                width=3,
                bg=COLORS["white"],
                fg=COLORS["text"],
                font=("Arial", 11, "bold"),
            ).pack(
                side="left",
            )

            self.make_button(
                quantity_row,
                "+",
                lambda n=name: self.change_quantity(n, 1),
                padx=10,
                pady=3,
            ).pack(
                side="left",
                padx=3,
            )

        # Right-side summary.
        self.summary_panel = self.create_panel(
            layout,
            "Your selection",
        )

        self.summary_panel.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.update_summary()

        # Bottom navigation.
        controls = tk.Frame(
            self.page_area,
            bg=COLORS["pink_light"],
        )

        controls.pack(
            fill="x",
            pady=(8, 0),
        )

        self.make_button(
            controls,
            "← Home",
            lambda: self.render_page("home"),
            primary=False,
        ).pack(
            side="left",
        )

        self.make_button(
            controls,
            "Next: Wrapping & Add-ons  →",
            lambda: self.go_to_wrapping(),
        ).pack(
            side="right",
        )


    def change_quantity(self, flower, amount):

        current = self.quantities[flower].get()

        new_quantity = max(
            0,
            min(99, current + amount),
        )

        self.quantities[flower].set(new_quantity)

        self.update_summary()


    # ========================================================
    # 18. WRAPPING AND ADD-ONS PAGE
    # ========================================================

    def render_wrapping(self):

        self.heading(
            self.page_area,
            "Wrapping & add-ons",
            "Choose the finishing touches for your bouquet.",
        )

        body = tk.Frame(
            self.page_area,
            bg=COLORS["pink_light"],
        )

        body.pack(
            fill="both",
            expand=True,
        )

        left = tk.Frame(
            body,
            bg=COLORS["pink_light"],
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12),
        )

        tk.Label(
            left,
            text="Choose your wrapping",
            bg=COLORS["pink_light"],
            fg=COLORS["plum"],
            font=("Arial", 12, "bold"),
        ).pack(
            anchor="w",
            pady=(0, 7),
        )

        wrap_grid = tk.Frame(
            left,
            bg=COLORS["pink_light"],
        )

        wrap_grid.pack(
            fill="x",
        )

        for index, (name, data) in enumerate(WRAPPINGS.items()):

            card = tk.Frame(
                wrap_grid,
                bg=COLORS["white"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
            )

            card.grid(
                row=0,
                column=index,
                padx=3,
                pady=4,
                sticky="nsew",
            )

            tk.Label(
                card,
                text=data["emoji"],
                bg=data["color"],
                fg=COLORS["plum"],
                font=("Arial", 25),
                width=4,
                pady=8,
            ).pack(
                fill="x",
                padx=5,
                pady=(5, 5),
            )

            tk.Label(
                card,
                text=name,
                bg=COLORS["white"],
                fg=COLORS["text"],
                font=("Arial", 9, "bold"),
                wraplength=90,
            ).pack(
                pady=2,
            )

            tk.Label(
                card,
                text=f"₹{data['price']}",
                bg=COLORS["white"],
                fg=COLORS["muted"],
                font=("Arial", 9),
            ).pack(
                pady=2,
            )

            tk.Radiobutton(
                card,
                text="Select",
                value=name,
                variable=self.selected_wrapping,
                command=lambda: self.render_page("wrapping"),
                bg=COLORS["white"],
                activebackground=COLORS["white"],
                selectcolor=COLORS["pink"],
                fg=COLORS["plum"],
            ).pack(
                pady=(2, 6),
            )

            wrap_grid.grid_columnconfigure(
                index,
                weight=1,
                uniform="wrap",
            )

        tk.Label(
            left,
            text="Add-ons (optional)",
            bg=COLORS["pink_light"],
            fg=COLORS["plum"],
            font=("Arial", 12, "bold"),
        ).pack(
            anchor="w",
            pady=(15, 5),
        )

        addons_grid = tk.Frame(
            left,
            bg=COLORS["pink_light"],
        )

        addons_grid.pack(
            fill="x",
        )

        for index, (name, data) in enumerate(ADD_ONS.items()):

            card = tk.Frame(
                addons_grid,
                bg=COLORS["white"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
            )

            card.grid(
                row=index // 2,
                column=index % 2,
                padx=4,
                pady=4,
                sticky="ew",
            )

            tk.Checkbutton(
                card,
                text=f"{data['emoji']} {name} (+₹{data['price']})",
                variable=self.selected_addons[name],
                command=lambda: self.render_page("wrapping"),
                bg=COLORS["white"],
                activebackground=COLORS["white"],
                selectcolor=COLORS["pink"],
                fg=COLORS["text"],
                font=("Arial", 9),
                padx=7,
                pady=8,
            ).pack(
                anchor="w",
            )

            addons_grid.grid_columnconfigure(
                index % 2,
                weight=1,
            )

        # Wrapping preview.
        preview = self.create_panel(
            body,
            "Wrapping preview",
        )

        preview.pack(
            side="right",
            fill="y",
        )

        selected_wrap = WRAPPINGS[
            self.selected_wrapping.get()
        ]

        tk.Label(
            preview,
            text=selected_wrap["emoji"],
            font=("Arial", 55),
            bg=selected_wrap["color"],
            width=4,
            pady=20,
        ).pack(
            padx=15,
            pady=(5, 8),
        )

        tk.Label(
            preview,
            text=self.selected_wrapping.get(),
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 12, "bold"),
        ).pack(
            pady=4,
        )

        tk.Label(
            preview,
            text=f"Wrapping: ₹{self.wrapping_cost()}\nAdd-ons: ₹{self.addon_total()}",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Arial", 10),
            justify="left",
        ).pack(
            padx=12,
            pady=8,
        )

        tk.Label(
            preview,
            text=f"TOTAL  ₹{self.grand_total()}",
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 18, "bold"),
        ).pack(
            pady=10,
        )

        controls = tk.Frame(
            self.page_area,
            bg=COLORS["pink_light"],
        )

        controls.pack(
            fill="x",
            pady=(8, 0),
        )

        self.make_button(
            controls,
            "← Back to Flowers",
            lambda: self.render_page("flowers"),
            primary=False,
        ).pack(
            side="left",
        )

        self.make_button(
            controls,
            "Next: Preview & Order  →",
            lambda: self.go_to_order(),
        ).pack(
            side="right",
        )


    def go_to_wrapping(self):

        self.render_page("wrapping")


    def go_to_order(self):

        if self.flower_count() == 0:

            messagebox.showwarning(
                "Choose flowers",
                "Please select at least one flower first.",
            )

            return

        self.render_page("order")


    # ========================================================
    # 19. PREVIEW AND CUSTOMER DETAILS
    # ========================================================

    def render_order(self):

        self.heading(
            self.page_area,
            "Preview & order",
            "Check your bouquet and enter your customer details.",
        )

        layout = tk.Frame(
            self.page_area,
            bg=COLORS["pink_light"],
        )

        layout.pack(
            fill="both",
            expand=True,
        )

        left = self.create_panel(
            layout,
            "Your bouquet",
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12),
        )

        for name, data in FLOWERS.items():

            quantity = self.quantities[name].get()

            if quantity > 0:

                line = tk.Frame(
                    left,
                    bg=COLORS["white"],
                )

                line.pack(
                    fill="x",
                    padx=12,
                    pady=3,
                )

                tk.Label(
                    line,
                    text=f"{data['emoji']}  {name} × {quantity}",
                    bg=COLORS["white"],
                    fg=COLORS["text"],
                    font=("Arial", 10),
                ).pack(
                    side="left",
                )

                tk.Label(
                    line,
                    text=f"₹{quantity * data['price']}",
                    bg=COLORS["white"],
                    fg=COLORS["plum"],
                    font=("Arial", 10, "bold"),
                ).pack(
                    side="right",
                )

        ttk.Separator(left).pack(
            fill="x",
            padx=12,
            pady=8,
        )

        tk.Label(
            left,
            text="Customer information",
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Arial", 12, "bold"),
        ).pack(
            anchor="w",
            padx=12,
            pady=(5, 8),
        )

        form = tk.Frame(
            left,
            bg=COLORS["white"],
        )

        form.pack(
            fill="x",
            padx=12,
            pady=(0, 10),
        )

        fields = [
            ("Full name", self.customer_name),
            ("Phone number (10 digits)", self.phone),
            ("Delivery address", self.address),
            ("Greeting message", self.greeting),
        ]

        for row, (label, variable) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                bg=COLORS["white"],
                fg=COLORS["muted"],
                font=("Arial", 9),
            ).grid(
                row=row * 2,
                column=0,
                sticky="w",
                pady=(3, 1),
            )

            ttk.Entry(
                form,
                textvariable=variable,
            ).grid(
                row=row * 2 + 1,
                column=0,
                sticky="ew",
                pady=(0, 3),
            )

        tk.Label(
            form,
            text="Delivery type",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Arial", 9),
        ).grid(
            row=8,
            column=0,
            sticky="w",
            pady=(3, 1),
        )

        ttk.Combobox(
            form,
            textvariable=self.delivery,
            values=["Home Delivery", "Pickup"],
            state="readonly",
        ).grid(
            row=9,
            column=0,
            sticky="ew",
            pady=(0, 3),
        )

        form.grid_columnconfigure(
            0,
            weight=1,
        )

        # Order total panel.
        right = self.create_panel(
            layout,
            "Order summary",
        )

        right.pack(
            side="right",
            fill="y",
        )

        tk.Label(
            right,
            text=f"Flower subtotal: ₹{self.flower_subtotal()}",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Arial", 9),
        ).pack(
            anchor="w",
            padx=12,
            pady=4,
        )

        tk.Label(
            right,
            text=(
                f"Wrapping ({self.selected_wrapping.get()}): "
                f"₹{self.wrapping_cost()}"
            ),
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Arial", 9),
            wraplength=220,
            justify="left",
        ).pack(
            anchor="w",
            padx=12,
            pady=4,
        )

        for name, data in ADD_ONS.items():

            if self.selected_addons[name].get():

                tk.Label(
                    right,
                    text=f"{name}: ₹{data['price']}",
                    bg=COLORS["white"],
                    fg=COLORS["text"],
                    font=("Arial", 9),
                ).pack(
                    anchor="w",
                    padx=12,
                    pady=3,
                )

        ttk.Separator(right).pack(
            fill="x",
            padx=12,
            pady=8,
        )

        tk.Label(
            right,
            text="TOTAL AMOUNT",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Arial", 9, "bold"),
        ).pack(
            anchor="w",
            padx=12,
        )

        tk.Label(
            right,
            text=f"₹{self.grand_total()}",
            bg=COLORS["white"],
            fg=COLORS["plum"],
            font=("Georgia", 25, "bold"),
        ).pack(
            anchor="w",
            padx=12,
            pady=5,
        )

        controls = tk.Frame(
            self.page_area,
            bg=COLORS["pink_light"],
        )

        controls.pack(
            fill="x",
            pady=(8, 0),
        )

        self.make_button(
            controls,
            "← Back to Wrapping",
            lambda: self.render_page("wrapping"),
            primary=False,
        ).pack(
            side="left",
        )

        self.make_button(
            controls,
            "Place Order  ✓",
            self.place_order,
        ).pack(
            side="right",
        )


    # ========================================================
    # 20. PLACE ORDER AND GENERATE RECEIPT
    # ========================================================

    def place_order(self):

        name = self.customer_name.get().strip()
        phone = self.phone.get().strip()
        address = self.address.get().strip()

        if not name:

            messagebox.showwarning(
                "Missing name",
                "Please enter your full name.",
            )

            return

        if not phone.isdigit() or len(phone) != 10:

            messagebox.showwarning(
                "Invalid phone",
                "Please enter a valid 10-digit phone number.",
            )

            return

        if (
            self.delivery.get() == "Home Delivery"
            and not address
        ):

            messagebox.showwarning(
                "Missing address",
                "Please enter your delivery address.",
            )

            return

        if self.flower_count() == 0:

            messagebox.showwarning(
                "Empty bouquet",
                "Please select at least one flower.",
            )

            self.render_page("flowers")

            return

        order_id = datetime.now().strftime(
            "BB%Y%m%d%H%M%S"
        )

        receipt_lines = [
            "=" * 42,
            "             BLOOM & BLISS",
            "              ORDER RECEIPT",
            "=" * 42,
            f"Order ID: {order_id}",
            f"Date: {datetime.now():%d-%m-%Y %I:%M %p}",
            f"Customer: {name}",
            f"Phone: {phone}",
            f"Delivery: {self.delivery.get()}",
            f"Address: {address or 'Pickup'}",
            "-" * 42,
            "FLOWERS:",
        ]

        for flower, data in FLOWERS.items():

            quantity = self.quantities[flower].get()

            if quantity > 0:

                amount = quantity * data["price"]

                receipt_lines.append(
                    f"{flower} x {quantity} = Rs. {amount}"
                )

        receipt_lines.append(
            f"Wrapping ({self.selected_wrapping.get()}): "
            f"Rs. {self.wrapping_cost()}"
        )

        receipt_lines.append("ADD-ONS:")

        selected = [
            name
            for name in ADD_ONS
            if self.selected_addons[name].get()
        ]

        if selected:

            for addon in selected:

                receipt_lines.append(
                    f"{addon}: Rs. {ADD_ONS[addon]['price']}"
                )

        else:

            receipt_lines.append("None")

        receipt_lines.extend([
            f"Greeting: {self.greeting.get().strip() or 'None'}",
            "-" * 42,
            f"GRAND TOTAL: Rs. {self.grand_total()}",
            "=" * 42,
            "Thank you for choosing Bloom & Bliss!",
        ])

        receipt_text = "\n".join(receipt_lines)

        receipt_path = os.path.join(
            RECEIPTS_DIR,
            f"{order_id}.txt",
        )

        try:

            with open(
                receipt_path,
                "w",
                encoding="utf-8",
            ) as file:

                file.write(receipt_text)

        except OSError as error:

            messagebox.showerror(
                "Receipt error",
                f"Could not save receipt:\n{error}",
            )

            return

        self.show_confirmation(
            name,
            order_id,
            receipt_text,
            receipt_path,
        )


    # ========================================================
    # 21. ORDER CONFIRMATION
    # ========================================================

    def show_confirmation(
        self,
        name,
        order_id,
        receipt_text,
        receipt_path,
    ):

        popup = tk.Toplevel(self.root)

        popup.title("Order Placed Successfully")
        popup.geometry("550x620")
        popup.configure(bg=COLORS["pink_light"])

        tk.Label(
            popup,
            text="✓",
            bg=COLORS["green"],
            fg=COLORS["white"],
            font=("Arial", 25, "bold"),
            width=3,
            pady=5,
        ).pack(pady=(15, 8))

        tk.Label(
            popup,
            text="Order placed successfully!",
            bg=COLORS["pink_light"],
            fg=COLORS["green"],
            font=("Georgia", 19, "bold"),
        ).pack(pady=3)

        tk.Label(
            popup,
            text=f"Thank you, {name}!",
            bg=COLORS["pink_light"],
            fg=COLORS["muted"],
            font=("Arial", 10),
        ).pack(pady=3)

        tk.Label(
            popup,
            text=f"Order ID: {order_id}",
            bg=COLORS["pink_light"],
            fg=COLORS["plum"],
            font=("Arial", 10, "bold"),
        ).pack(pady=5)

        receipt_box = tk.Text(
            popup,
            height=18,
            font=("Consolas", 9),
            wrap="word",
            bg=COLORS["white"],
            fg=COLORS["text"],
            bd=0,
            padx=12,
            pady=12,
        )

        receipt_box.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=8,
        )

        receipt_box.insert(
            "1.0",
            receipt_text,
        )

        receipt_box.config(
            state="disabled",
        )

        tk.Label(
            popup,
            text=f"Receipt saved in: {receipt_path}",
            bg=COLORS["pink_light"],
            fg=COLORS["muted"],
            font=("Arial", 8),
            wraplength=500,
        ).pack(pady=3)

        self.make_button(
            popup,
            "Back to Home",
            lambda: self.back_to_home(popup),
        ).pack(pady=(5, 12))


    def back_to_home(self, popup):

        popup.destroy()

        for variable in self.quantities.values():
            variable.set(0)

        for variable in self.selected_addons.values():
            variable.set(False)

        self.selected_wrapping.set("Classic Paper")

        self.customer_name.set("")
        self.phone.set("")
        self.address.set("")
        self.delivery.set("Home Delivery")
        self.greeting.set("Wishing you a beautiful day!")

        self.render_page("home")


    # ========================================================
    # 22. ORDER HISTORY
    # ========================================================

    def show_history(self):

        popup = tk.Toplevel(self.root)

        popup.title("Order History")
        popup.geometry("650x480")
        popup.configure(bg=COLORS["pink_light"])

        tk.Label(
            popup,
            text="Order History",
            bg=COLORS["pink_light"],
            fg=COLORS["plum"],
            font=("Georgia", 20, "bold"),
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 8),
        )

        receipt_files = sorted(
            [
                file
                for file in os.listdir(RECEIPTS_DIR)
                if file.lower().endswith(".txt")
            ],
            reverse=True,
        )

        text_box = tk.Text(
            popup,
            font=("Consolas", 9),
            wrap="word",
            bg=COLORS["white"],
            fg=COLORS["text"],
            bd=0,
            padx=12,
            pady=12,
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15),
        )

        if not receipt_files:

            text_box.insert(
                "1.0",
                "No orders have been placed yet.\n"
                "Your future orders will appear here.",
            )

        else:

            for filename in receipt_files:

                path = os.path.join(
                    RECEIPTS_DIR,
                    filename,
                )

                try:

                    with open(
                        path,
                        "r",
                        encoding="utf-8",
                    ) as file:

                        text_box.insert(
                            "end",
                            file.read() + "\n\n",
                        )

                except OSError:
                    continue

        text_box.config(
            state="disabled",
        )


    # ========================================================
    # 23. ABOUT APPLICATION
    # ========================================================

    def show_about(self):

        messagebox.showinfo(
            "About Bloom & Bliss",
            "Bloom & Bliss - Flower Bouquet Maker\n\n"
            "Create your own beautiful flower bouquet.\n\n"
            "Features:\n"
            "• Six flower varieties\n"
            "• Adjustable flower quantities\n"
            "• Different wrapping styles\n"
            "• Optional add-ons\n"
            "• Automatic price calculation\n"
            "• Customer order details\n"
            "• Order receipt and order history\n\n"
            "Made with love!",
        )


# ============================================================
# 24. START APPLICATION
# ============================================================

def main():

    root = tk.Tk()

    app = BouquetMaker(root)

    root.mainloop()


if __name__ == "__main__":
    main()