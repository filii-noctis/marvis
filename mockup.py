"""
Consumer Financial Habits App
-----------------------------
This application displays how consumer spending on various products
changes with economic conditions.
"""

# Standard library imports
import os
import sys
from math import sin
from io import BytesIO

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

# Set window size to simulate a mobile device
Window.size = (400, 800)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# Sample data for products and economic indicators
products = [
    {
        'name': 'Smartphones',
        'category': 'Electronics',
        'icon': '📱',
        'spending_data': {
            'GDP_growth': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            'consumer_spending': [85, 90, 100, 110, 115, 125]
        },
        'description': 'Consumer spending on smartphones increases with economic growth as disposable income rises.'
    },
    {
        'name': 'Dining Out',
        'category': 'Services',
        'icon': '🍽️',
        'spending_data': {
            'GDP_growth': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            'consumer_spending': [70, 85, 95, 105, 120, 130]
        },
        'description': 'Restaurant spending is highly correlated with economic conditions, with sharp drops during recessions.'
    },
    {
        'name': 'Groceries',
        'category': 'Essential',
        'icon': '🛒',
        'spending_data': {
            'GDP_growth': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            'consumer_spending': [100, 102, 103, 105, 107, 108]
        },
        'description': 'Grocery spending remains relatively stable regardless of economic conditions with minimal growth during prosperity.'
    },
    {
        'name': 'Luxury Goods',
        'category': 'Non-essential',
        'icon': '💎',
        'spending_data': {
            'GDP_growth': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            'consumer_spending': [40, 60, 85, 120, 150, 190]
        },
        'description': 'Luxury goods spending shows the strongest correlation with economic growth, with substantial increases in good times.'
    },
    {
        'name': 'Healthcare',
        'category': 'Essential',
        'icon': '🏥',
        'spending_data': {
            'GDP_growth': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            'consumer_spending': [95, 98, 100, 101, 103, 105]
        },
        'description': 'Healthcare spending is relatively inelastic to economic conditions as it is considered essential.'
    },
    {
        'name': 'Entertainment',
        'category': 'Non-essential',
        'icon': '🎬',
        'spending_data': {
            'GDP_growth': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            'consumer_spending': [60, 75, 90, 110, 130, 145]
        },
        'description': 'Entertainment spending shows significant elasticity with economic conditions as consumers adjust discretionary spending.'
    },
    {
        'name': 'Housing',
        'category': 'Essential',
        'icon': '🏠',
        'spending_data': {
            'inflation_rate': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            'consumer_spending': [100, 102, 105, 110, 118, 125]
        },
        'description': 'Housing costs tend to rise with inflation, affecting consumer budgets regardless of economic growth.'
    },
    {
        'name': 'Education',
        'category': 'Investment',
        'icon': '🎓',
        'spending_data': {
            'unemployment_rate': [3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            'consumer_spending': [90, 95, 100, 105, 110, 115]
        },
        'description': 'Education spending often increases with unemployment as people seek to improve their skills during economic downturns.'
    }
]

# Economic indicators over time (quarters)
economic_data = {
    'quarters': ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024'],
    'GDP_growth': [1.2, 1.5, 1.8, 2.0, 2.3, 2.5],
    'inflation_rate': [3.5, 3.8, 4.0, 3.7, 3.5, 3.2],
    'unemployment_rate': [5.0, 4.8, 4.6, 4.5, 4.3, 4.1],
    'consumer_confidence': [95, 97, 100, 102, 105, 108]
}

def create_chart_image(product):
    """
    Creates a chart for the given product and returns it as a Kivy Image
    """
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    
    # Set color scheme
    plt.style.use('seaborn-v0_8-pastel')
    
    # Determine what economic indicator to use
    indicator = list(product['spending_data'].keys())[0]
    x_data = product['spending_data'][indicator]
    y_data = product['spending_data']['consumer_spending']
    
    # Plot data
    ax.plot(x_data, y_data, 'o-', color='#3498db', linewidth=2, markersize=8)
    ax.set_xlabel(f'{indicator.replace("_", " ").title()} (%)', fontsize=10)
    ax.set_ylabel('Consumer Spending Index', fontsize=10)
    ax.set_title(f'Spending on {product["name"]} vs {indicator.replace("_", " ").title()}', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add trend line
    z = np.polyfit(x_data, y_data, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(x_data), max(x_data), 100)
    ax.plot(x_trend, p(x_trend), "r--", alpha=0.7)
    
    # Add correlation coefficient
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    ax.text(0.05, 0.95, f'Correlation: {correlation:.2f}', 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.1))
    
    # Improve appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Save figure to a BytesIO object
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert to Kivy Image
    data = BytesIO(buf.read())
    img = CoreImage(data, ext='png')
    plt.close(fig)  # Close the figure to free memory
    
    return Image(texture=img.texture, size_hint=(1, None), height=dp(300))

class StatusBar(BoxLayout):
    """Mobile-like status bar for the top of the screen"""
    def __init__(self, **kwargs):
        super(StatusBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(30)
        self.padding = [dp(10), 0]
        
        # Add time
        from datetime import datetime
        time_label = Label(text=datetime.now().strftime("%H:%M"),
                         size_hint_x=None,
                         width=dp(50),
                         font_size=dp(14))
        
        # Add battery and signal icons as text (we'll use emojis for simplicity)
        status_icons = Label(text="📶 100% 🔋",
                           font_size=dp(14),
                           halign='right')
        
        self.add_widget(time_label)
        self.add_widget(Label()) # Spacer
        self.add_widget(status_icons)
        
        # Background
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class NavigationBar(BoxLayout):
    """Mobile-like bottom navigation bar"""
    def __init__(self, **kwargs):
        super(NavigationBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [0, dp(5)]
        self.spacing = dp(10)
        
        # Navigation icons
        icons = [
            {"icon": "🏠", "text": "Home"},
            {"icon": "📊", "text": "Analytics"},
            {"icon": "📈", "text": "Trends"},
            {"icon": "⚙️", "text": "Settings"}
        ]
        
        for item in icons:
            btn = BoxLayout(orientation='vertical')
            icon = Label(text=item["icon"], font_size=dp(20))
            text = Label(text=item["text"], font_size=dp(12))
            btn.add_widget(icon)
            btn.add_widget(text)
            self.add_widget(btn)
        
        # Background with top border
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(0.9, 0.9, 0.9, 1)
            self.line = Line(points=[self.x, self.y + self.height - 1, self.x + self.width, self.y + self.height - 1], width=1)
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.line.points = [self.x, self.y + self.height - 1, self.x + self.width, self.y + self.height - 1]

class ProductCard(Button):
    """
    Custom button class for product items in the list
    """
    def __init__(self, product, **kwargs):
        super(ProductCard, self).__init__(**kwargs)
        self.product = product
        self.size_hint_y = None
        self.height = dp(80)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.border = (10, 10, 10, 10)
        self.text = ''
        
        # Create layout for card content
        layout = BoxLayout(orientation='horizontal', 
                          spacing=dp(10), 
                          padding=[dp(15), dp(10)],
                          size=self.size,
                          pos=self.pos)
        
        # Icon
        icon_label = Label(text=product.get('icon', '📦'),
                         font_size=dp(30),
                         size_hint_x=None,
                         width=dp(50))
        
        # Text content
        text_box = BoxLayout(orientation='vertical', spacing=dp(2))
        
        # Product name
        name_label = Label(text=product['name'],
                          font_size=dp(18),
                          color=(0.1, 0.1, 0.1, 1),
                          halign='left',
                          valign='middle',
                          size_hint_y=None,
                          height=dp(25))
        name_label.bind(size=lambda s, w: setattr(name_label, 'text_size', (w[0], dp(25))))
        
        # Product category
        category_label = Label(text=product['category'],
                             font_size=dp(14),
                             color=(0.5, 0.5, 0.5, 1),
                             halign='left',
                             valign='top',
                             size_hint_y=None,
                             height=dp(20))
        category_label.bind(size=lambda s, w: setattr(category_label, 'text_size', (w[0], dp(20))))
        
        text_box.add_widget(name_label)
        text_box.add_widget(category_label)
        
        layout.add_widget(icon_label)
        layout.add_widget(text_box)
        self.add_widget(layout)
        
        # Add card effect with canvas
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.card_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8),])
            
            # Add subtle shadow effect (simulate with a slightly larger, lighter rectangle behind)
            Color(0.9, 0.9, 0.9, 1)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - dp(2)), 
                                         size=(self.width, self.height),
                                         radius=[dp(8),])
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, instance, value):
        self.shadow.pos = (instance.x, instance.y - dp(2))
        self.shadow.size = instance.size
        self.card_bg.pos = instance.pos
        self.card_bg.size = instance.size

class ProductListScreen(Screen):
    """
    Main screen showing the list of products
    """
    def __init__(self, **kwargs):
        super(ProductListScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=0)
        
        # Status bar
        status_bar = StatusBar()
        
        # Header with title
        header = BoxLayout(orientation='vertical', 
                          size_hint_y=None, 
                          height=dp(100),
                          padding=[dp(15), dp(10)])
        
        title = Label(text='Consumer Finance',
                     font_size=dp(22),
                     color=(0.1, 0.1, 0.1, 1),
                     bold=True,
                     halign='left',
                     size_hint_y=None,
                     height=dp(30))
        title.bind(size=lambda s, w: setattr(title, 'text_size', (w[0], None)))
        
        subtitle = Label(text='How spending changes with economic conditions',
                        font_size=dp(14),
                        color=(0.5, 0.5, 0.5, 1),
                        halign='left',
                        size_hint_y=None,
                        height=dp(20))
        subtitle.bind(size=lambda s, w: setattr(subtitle, 'text_size', (w[0], None)))
        
        # Search box (visual only)
        search_box = BoxLayout(size_hint_y=None, 
                              height=dp(40), 
                              padding=[0, dp(5)],
                              spacing=dp(10))
        
        search_button = Button(text="🔍 Search products...",
                             background_normal='',
                             background_color=(0.95, 0.95, 0.95, 1),
                             color=(0.5, 0.5, 0.5, 1),
                             size_hint_x=0.8,
                             halign='left',
                             text_size=(dp(200), dp(40)),
                             padding=[dp(15), 0])
        
        filter_button = Button(text="🔽",
                             background_normal='',
                             background_color=(0.95, 0.95, 0.95, 1),
                             size_hint_x=0.2)
        
        search_box.add_widget(search_button)
        search_box.add_widget(filter_button)
        
        header.add_widget(title)
        header.add_widget(subtitle)
        header.add_widget(search_box)
        
        # Products list container
        list_container = BoxLayout(orientation='vertical', 
                                  padding=[dp(15), dp(10)])
        
        # Products header
        products_header = BoxLayout(size_hint_y=None, height=dp(30))
        products_title = Label(text=f'Products ({len(products)})',
                              font_size=dp(16),
                              bold=True,
                              halign='left')
        products_title.bind(size=lambda s, w: setattr(products_title, 'text_size', (w[0], None)))
        
        products_header.add_widget(products_title)
        
        # Create scrollable list
        scroll_layout = GridLayout(cols=1, 
                                  spacing=dp(10), 
                                  size_hint_y=None,
                                  padding=[0, dp(5)])
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # Add products to the list
        for product in products:
            card = ProductCard(product=product)
            card.bind(on_release=lambda btn, p=product: self.show_product_detail(p))
            scroll_layout.add_widget(card)
        
        # Create scroll view
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll_view.add_widget(scroll_layout)
        
        list_container.add_widget(products_header)
        list_container.add_widget(scroll_view)
        
        # Navigation bar
        nav_bar = NavigationBar()
        
        # Add all elements to main layout
        main_layout.add_widget(status_bar)
        main_layout.add_widget(header)
        main_layout.add_widget(list_container)
        main_layout.add_widget(nav_bar)
        
        self.add_widget(main_layout)
    
    def show_product_detail(self, product):
        app = App.get_running_app()
        detail_screen = ProductDetailScreen(name='product_detail', product=product)
        app.root.add_widget(detail_screen)
        app.root.transition = SlideTransition(direction='left')
        app.root.current = 'product_detail'

class ProductDetailScreen(Screen):
    """
    Detail screen showing information and charts for a specific product
    """
    def __init__(self, product, **kwargs):
        super(ProductDetailScreen, self).__init__(**kwargs)
        self.product = product
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=0)
        
        # Status bar
        status_bar = StatusBar()
        
        # Content container with scroll
        content_container = BoxLayout(orientation='vertical')
        
        # Header with back button and title
        header = BoxLayout(size_hint_y=None, 
                          height=dp(60), 
                          padding=[dp(10), dp(10)])
        
        back_btn = Button(text="←",
                         font_size=dp(20),
                         size_hint=(None, None),
                         size=(dp(40), dp(40)),
                         background_normal='',
                         background_color=(0.95, 0.95, 0.95, 1))
        back_btn.bind(on_release=self.go_back)
        
        title = Label(text=product['name'],
                     font_size=dp(20),
                     bold=True)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Scrollable content
        scroll_container = ScrollView(do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', 
                                  spacing=dp(15), 
                                  padding=[dp(15), dp(15)],
                                  size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Product icon and category
        info_box = BoxLayout(orientation='horizontal', 
                            size_hint_y=None,
                            height=dp(60))
        
        icon_label = Label(text=product.get('icon', '📦'),
                         font_size=dp(40),
                         size_hint_x=None,
                         width=dp(60))
        
        category_box = BoxLayout(orientation='vertical')
        category_label = Label(text=product['category'],
                             font_size=dp(18),
                             halign='left',
                             valign='bottom',
                             size_hint_y=None,
                             height=dp(30))
        category_label.bind(size=lambda s, w: setattr(category_label, 'text_size', (w[0], dp(30))))
        
        sub_label = Label(text='Economic sensitivity: ' + ('High' if correlation > 0.8 else 'Medium' if correlation > 0.5 else 'Low'),
                         font_size=dp(14),
                         color=(0.5, 0.5, 0.5, 1),
                         halign='left',
                         valign='top',
                         size_hint_y=None,
                         height=dp(20))
        sub_label.bind(size=lambda s, w: setattr(sub_label, 'text_size', (w[0], dp(20))))
        
        category_box.add_widget(category_label)
        category_box.add_widget(sub_label)
        
        info_box.add_widget(icon_label)
        info_box.add_widget(category_box)
        
        # Chart section
        chart_title = Label(text='Spending Correlation',
                          font_size=dp(18),
                          bold=True,
                          halign='left',
                          size_hint_y=None,
                          height=dp(30))
        chart_title.bind(size=lambda s, w: setattr(chart_title, 'text_size', (w[0], dp(30))))
        
        # Create chart
        chart_image = create_chart_image(product)
        
        # Description section
        desc_title = Label(text='Analysis',
                         font_size=dp(18),
                         bold=True,
                         halign='left',
                         size_hint_y=None,
                         height=dp(30))
        desc_title.bind(size=lambda s, w: setattr(desc_title, 'text_size', (w[0], dp(30))))
        
        description = Label(text=product['description'],
                          font_size=dp(16),
                          halign='left',
                          size_hint_y=None,
                          height=dp(100))
        description.bind(size=lambda s, w: setattr(description, 'text_size', (w[0], None)))
        description.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        
        # Economic indicators section
        indicators_title = Label(text='Economic Indicators',
                               font_size=dp(18),
                               bold=True,
                               halign='left',
                               size_hint_y=None,
                               height=dp(30))
        indicators_title.bind(size=lambda s, w: setattr(indicators_title, 'text_size', (w[0], dp(30))))
        
        # Recent economic data
        recent_quarter = economic_data['quarters'][-1]
        
        # Create economic indicators cards
        indicators_grid = GridLayout(cols=2, 
                                   spacing=dp(10),
                                   size_hint_y=None,
                                   height=dp(240))
        
        # GDP growth
        gdp_card = BoxLayout(orientation='vertical', 
                           padding=dp(10),
                           size_hint_y=None,
                           height=dp(110))
        
        with gdp_card.canvas.before:
            Color(0.95, 0.95, 1.0, 1)
            RoundedRectangle(pos=gdp_card.pos, size=gdp_card.size, radius=[dp(8),])
        
        gdp_card.bind(pos=lambda obj, pos: setattr(obj.canvas.before.children[-1], 'pos', pos))
        gdp_card.bind(size=lambda obj, size: setattr(obj.canvas.before.children[-1], 'size', size))
        
        gdp_title = Label(text='GDP Growth',
                        font_size=dp(14),
                        color=(0.4, 0.4, 0.4, 1),
                        size_hint_y=None,
                        height=dp(20))
        
        gdp_value = Label(text=f"{economic_data['GDP_growth'][-1]}%",
                        font_size=dp(24),
                        bold=True,
                        size_hint_y=None,
                        height=dp(30))
        
        gdp_trend = Label(text=f"↑ from {economic_data['GDP_growth'][-2]}% ({recent_quarter})",
                        font_size=dp(12),
                        color=(0.2, 0.7, 0.2, 1) if economic_data['GDP_growth'][-1] > economic_data['GDP_growth'][-2] else (0.7, 0.2, 0.2, 1),
                        size_hint_y=None,
                        height=dp(20))
        
        gdp_card.add_widget(gdp_title)
        gdp_card.add_widget(gdp_value)
        gdp_card.add_widget(gdp_trend)
        
        # Inflation rate
        inflation_card = BoxLayout(orientation='vertical', 
                                 padding=dp(10),
                                 size_hint_y=None,
                                 height=dp(110))
        
        with inflation_card.canvas.before:
            Color(1.0, 0.95, 0.95, 1)
            RoundedRectangle(pos=inflation_card.pos, size=inflation_card.size, radius=[dp(8),])
        
        inflation_card.bind(pos=lambda obj, pos: setattr(obj.canvas.before.children[-1], 'pos', pos))
        inflation_card.bind(size=lambda obj, size: setattr(obj.canvas.before.children[-1], 'size', size))
        
        inflation_title = Label(text='Inflation Rate',
                              font_size=dp(14),
                              color=(0.4, 0.4, 0.4, 1),
                              size_hint_y=None,
                              height=dp(20))
        
        inflation_value = Label(text=f"{economic_data['inflation_rate'][-1]}%",
                              font_size=dp(24),
                              bold=True,
                              size_hint_y=None,
                              height=dp(30))
        
        inflation_trend = Label(text=f"↓ from {economic_data['inflation_rate'][-2]}% ({recent_quarter})",
                              font_size=dp(12),
                              color=(0.2, 0.7, 0.2, 1) if economic_data['inflation_rate'][-1] < economic_data['inflation_rate'][-2] else (0.7, 0.2, 0.2, 1),
                              size_hint_y=None,
                              height=dp(20))
        
        inflation_card.add_widget(inflation_title)
        inflation_card.add_widget(inflation_value)
        inflation_card.add_widget(inflation_trend)
        
        # Unemployment rate
        unemployment_card = BoxLayout(orientation='vertical', 
                                    padding=dp(10),
                                    size_hint_y=None,
                                    height=dp(110))
        
        with unemployment_card.canvas.before:
            Color(0.95, 1.0, 0.95, 1)
            RoundedRectangle(pos=unemployment_card.pos, size=unemployment_card.size, radius=[dp(8),])
        
        unemployment_card.bind(pos=lambda obj, pos: setattr(obj.canvas.before.children[-1], 'pos', pos))
        unemployment_card.bind(size=lambda obj, size: setattr(obj.canvas.before.children[-1], 'size', size))
        
        unemployment_title = Label(text='Unemployment',
                                 font_size=dp(14),
                                 color=(0.4, 0.4, 0.4, 1),
                                 size_hint_y=None,
                                 height=dp(20))
        
        unemployment_value = Label(text=f"{economic_data['unemployment_rate'][-1]}%",
                                 font_size=dp(24),
                                 bold=True,
                                 size_hint_y=None,
                                 height=dp(30))
        
        unemployment_trend = Label(text=f"↓ from {economic_data['unemployment_rate'][-2]}% ({recent_quarter})",
                                 font_size=dp(12),
                                 color=(0.2, 0.7, 0.2, 1) if economic_data['unemployment_rate'][-1] < economic_data['unemployment_rate'][-2] else (0.7, 0.2, 0.2, 1),
                                 size_hint_y=None,
                                 height=dp(20))
        
        unemployment_card.add_widget(unemployment_title)
        unemployment_card.add_widget(unemployment_value)
        unemployment_card.add_widget(unemployment_trend)
        
        # Consumer confidence
        confidence_card = BoxLayout(orientation='vertical', 
                                  padding=dp(10),
                                  size_hint_y=None,
                                  height=dp(110))
        
        with confidence_card.canvas.before:
            Color(0.95, 0.95, 1.0, 1)
            RoundedRectangle(pos=confidence_card.pos, size=confidence_card.size, radius=[dp(8),])
        
        confidence_card.bind(pos=lambda obj, pos: setattr(obj.canvas.before.children[-1], 'pos', pos))
        confidence_card.bind(size=lambda obj, size: setattr(obj.canvas.before.children[-1], 'size', size))
        
        confidence_title = Label(text='Consumer Confidence',
                               font_size=dp(14),
                               color=(0.4, 0.4, 0.4, 1),
                               size_hint_y=None,
                               height=dp(20))
        
        confidence_value = Label(text=f"{economic_data['consumer_confidence'][-1]}",
                               font_size=dp(24),
                               bold=True,
                               size_hint_y=None,
                               height=dp(30))
        
        confidence_trend = Label(text=f"↑ from {economic_data['consumer_confidence'][-2]} ({recent_quarter})",
                               font_size=dp(12),
                               color=(0.2, 0.7, 0.2, 1) if economic_data['consumer_confidence'][-1] > economic_data['consumer_confidence'][-2] else (0.7, 0.2, 0.2, 1),
                               size_hint_y=None,
                               height=dp(20))
        
        confidence_card.add_widget(confidence_title)
        confidence_card.add_widget(confidence_value)
        confidence_card.add_widget(confidence_trend)
        
        # Add economic cards to grid
        indicators_grid.add_widget(gdp_card)
        indicators_grid.add_widget(inflation_card)
        indicators_grid.add_widget(unemployment_card)
        indicators_grid.add_widget(confidence_card)
        
        # Add all sections to content layout
        content_layout.add_widget(info_box)
        content_layout.add_widget(chart_title)
        content_layout.add_widget(chart_image)
        content_layout.add_widget(desc_title)
        content_layout.add_widget(description)
        content_layout.add_widget(indicators_title)
        content_layout.add_widget(indicators_grid)
        
        # Add a spacer at the bottom
        spacer = BoxLayout(size_hint_y=None, height=dp(30))
        content_layout.add_widget(spacer)
        
        scroll_container.add_widget(content_layout)
        content_container.add_widget(scroll_container)
        
        # Navigation bar
        nav_bar = NavigationBar()
        
        # Add all elements to main layout
        main_layout.add_widget(status_bar)
        main_layout.add_widget(header)
        main_layout.add_widget(content_container)
        main_layout.add_widget(nav_bar)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='right')
        app.root.current = 'product_list'

class ConsumerFinanceApp(App):
    """
    Main app class
    """
    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Create and add screens
        list_screen = ProductListScreen(name='product_list')
        sm.add_widget(list_screen)
        
        # Set initial screen
        sm.current = 'product_list'
        
        return sm

if __name__ == '__main__':
    # Calculate correlation for use in product detail screen
    for product in products:
        x_data = product['spending_data'][list(product['spending_data'].keys())[0]]
        y_data = product['spending_data']['consumer_spending']
        correlation = np.corrcoef(x_data, y_data)[0, 1]
        product['correlation'] = correlation
    
    # Run the app
    ConsumerFinanceApp().run()