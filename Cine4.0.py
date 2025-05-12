from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, DictProperty, ListProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import random

Builder.load_string('''
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        Label:
            text: 'CINEMA TICKETS'
            font_size: 40
            bold: True
            color: 1, 0.5, 0, 1
            size_hint_y: 0.3
        BoxLayout:
            spacing: 30
            padding: 30
            size_hint_y: 0.4
            Button:
                text: 'Seleccionar Película'
                font_size: 24
                background_color: 0.2, 0.6, 1, 1
                on_press: root.manager.current = 'movies'
            Button:
                text: 'Comprar Comidas'
                font_size: 24
                background_color: 1, 0.5, 0, 1
                on_press: root.manager.current = 'food'

<MovieScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Label:
            text: 'Selecciona una Película'
            font_size: 30
            bold: True
            color: 0.9, 0.9, 0.9, 1
        GridLayout:
            cols: 2
            rows: 2
            spacing: 30
            padding: 30
            Button:
                text: root.peliculas[0]
                font_size: 20
                background_color: 0.3, 0.4, 0.5, 1
                on_press: root.select_movie(0)
            Button:
                text: root.peliculas[1]
                font_size: 20
                background_color: 0.3, 0.4, 0.5, 1
                on_press: root.select_movie(1)
            Button:
                text: root.peliculas[2]
                font_size: 20
                background_color: 0.3, 0.4, 0.5, 1
                on_press: root.select_movie(2)
            Button:
                text: root.peliculas[3]
                font_size: 20
                background_color: 0.3, 0.4, 0.5, 1
                on_press: root.select_movie(3)

<SeatScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: root.selected_movie
            font_size: 26
            bold: True
            color: 0.9, 0.9, 0.9, 1
        GridLayout:
            id: seats_grid
            cols: 8
            rows: 10
            spacing: 5
            size_hint: 1, 0.8
        BoxLayout:
            size_hint: 1, 0.1
            spacing: 20
            Button:
                text: 'Pagar'
                font_size: 20
                background_color: 0, 0.7, 0, 1
                on_press: root.process_payment('pelicula')
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.8, 0, 0, 1
                on_press: root.manager.current = 'main'

<FoodScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: 'Menú de Comidas'
            font_size: 30
            bold: True
            color: 0.9, 0.9, 0.9, 1
        GridLayout:
            cols: 2
            spacing: 20
            padding: 20
            Label:
                text: 'Palomitas Grandes ($5.000)'
                font_size: 20
            BoxLayout:
                spacing: 10
                Button:
                    text: '-'
                    size_hint_x: 0.2
                    on_press: root.update_food('palomitas', -1)
                Label:
                    text: str(root.palomitas)
                    font_size: 20
                    size_hint_x: 0.4
                Button:
                    text: '+'
                    size_hint_x: 0.2
                    on_press: root.update_food('palomitas', 1)
            
            Label:
                text: 'Bebidas Grandes ($3.000)'
                font_size: 20
            BoxLayout:
                spacing: 10
                Button:
                    text: '-'
                    size_hint_x: 0.2
                    on_press: root.update_food('bebidas', -1)
                Label:
                    text: str(root.bebidas)
                    font_size: 20
                    size_hint_x: 0.4
                Button:
                    text: '+'
                    size_hint_x: 0.2
                    on_press: root.update_food('bebidas', 1)
        
        Label:
            text: f'Total Comida: ${root.food_total}'
            font_size: 24
            bold: True
        
        BoxLayout:
            size_hint_y: 0.2
            spacing: 20
            Button:
                text: 'Pagar Comida'
                font_size: 20
                background_color: 0, 0.7, 0, 1
                on_press: root.process_payment('comida')
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.2, 0.6, 1, 1
                on_press: root.manager.current = 'main'

<PagoPopup>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        Label:
            text: root.message
            font_size: 18
        BoxLayout:
            size_hint_y: 0.4
            spacing: 10
            Button:
                text: 'Tarjeta'
                background_color: 0.2, 0.6, 1, 1
                on_press: root.process('card')
            Button:
                text: 'Efectivo'
                background_color: 0.4, 0.8, 0.4, 1
                on_press: root.process('cash')

<ReceiptScreen>:
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: max(self.minimum_height, root.height)
            padding: 20
            spacing: 10
            Label:
                text: 'RECIBO DE PAGO'
                font_size: 30
                bold: True
                size_hint_y: None
                height: 50
            Label:
                text: root.receipt_text
                font_size: 20
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
            Button:
                text: 'Volver al Menú'
                size_hint_y: None
                height: 50
                background_color: 0.2, 0.6, 1, 1
                on_press: root.manager.current = 'main'
''')

class MainScreen(Screen):
    pass

class MovieScreen(Screen):
    peliculas = ListProperty(["Avengers: Endgame", "Spider-Man: No Way Home", 
                            "The Batman", "Jurassic World Dominion"])
    seating = DictProperty({})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_seats()
    
    def init_seats(self):
        for pelicula in self.peliculas:
            self.seating[pelicula] = {f"{row}{col}": "Disponible" 
                                    for row in range(1, 11) for col in "ABCDEFGH"}
    
    def select_movie(self, index):
        self.manager.get_screen('seats').selected_movie = self.peliculas[index]
        self.manager.get_screen('seats').load_seats()
        self.manager.current = 'seats'

class SeatScreen(Screen):
    selected_movie = StringProperty("")
    costo_asiento = NumericProperty(12000)
    costo_preferencial = NumericProperty(3000)
    selected_seats = ListProperty([])
    
    def load_seats(self):
        grid = self.ids.seats_grid
        grid.clear_widgets()
        for row in range(1, 11):
            for col in "ABCDEFGH":
                asiento = f"{row}{col}"
                estado = App.get_running_app().root.get_screen('movies').seating[
                    self.selected_movie][asiento]
                
                if row == 1:
                    bg_color = (0.2, 0.6, 1, 1) if estado == "Disponible" else (0.8, 0, 0, 1)
                else:
                    bg_color = (0.4, 0.8, 0.4, 1) if estado == "Disponible" else (0.8, 0, 0, 1)
                
                btn = Button(
                    text=asiento,
                    background_color=bg_color,
                    disabled= (estado == "Reservado")
                )
                btn.bind(on_press=lambda x, a=asiento: self.toggle_seat(a))
                grid.add_widget(btn)
    
    def toggle_seat(self, asiento):
        if asiento in self.selected_seats:
            self.selected_seats.remove(asiento)
        else:
            self.selected_seats.append(asiento)
        self.update_seat_colors()
    
    def update_seat_colors(self):
        for child in self.ids.seats_grid.children:
            if child.text in self.selected_seats:
                child.background_color = (1, 0.8, 0, 1)
            else:
                estado = App.get_running_app().root.get_screen('movies').seating[
                    self.selected_movie][child.text]
                fila = int(''.join(filter(str.isdigit, child.text)))
                if fila == 1:
                    child.background_color = (0.2, 0.6, 1, 1) if estado == "Disponible" else (0.8, 0, 0, 1)
                else:
                    child.background_color = (0.4, 0.8, 0.4, 1) if estado == "Disponible" else (0.8, 0, 0, 1)
    
    def calculate_total(self):
        total = 0
        for asiento in self.selected_seats:
            fila = int(''.join(filter(str.isdigit, asiento)))
            if fila == 1:
                total += self.costo_preferencial
            else:
                total += self.costo_asiento
        
        food_total = App.get_running_app().root.get_screen('food').food_total
        return total + food_total
    
    def process_payment(self, payment_type):
        if not self.selected_seats:
            self.show_popup("Error", "Selecciona al menos un asiento")
            return
        
        total = self.calculate_total()
        content = PagoPopup(
            message=f"Total a pagar: ${total}\n(Entradas: ${total - App.get_running_app().root.get_screen('food').food_total} | Comida: ${App.get_running_app().root.get_screen('food').food_total})", 
            process_callback=lambda method: self.finalize_payment(method, total),
            payment_type=payment_type
        )
        popup = Popup(title="Método de Pago", content=content, size_hint=(0.8, 0.4))
        content.popup = popup
        popup.open()
    
    def finalize_payment(self, method, total):
        success = True
        if method == 'card':
            success = random.random() > 0.1
        
        if success:
            self.completar_reserva()
            self.show_receipt(total, method, True)
        else:
            self.show_receipt(total, method, False)
            self.show_popup("Error", "Pago con tarjeta fallido. Intente nuevamente.")
    
    def show_receipt(self, total, method, success):
        receipt_text = [
            "=== RECIBO DE PAGO ===",
            f"Película: {self.selected_movie}",
            f"Asientos: {', '.join(self.selected_seats)}",
            f"Total entradas: ${total - App.get_running_app().root.get_screen('food').food_total}",
            f"Total comida: ${App.get_running_app().root.get_screen('food').food_total}",
            f"Método de pago: {method.upper()}",
            f"Estado: {'APROBADO' if success else 'RECHAZADO'}",
            "Gracias por su compra!"
        ]
        receipt_screen = self.manager.get_screen('receipt')
        receipt_screen.receipt_text = '\n'.join(receipt_text)
        self.manager.current = 'receipt'
    
    def completar_reserva(self):
        seating = App.get_running_app().root.get_screen('movies').seating
        for asiento in self.selected_seats:
            seating[self.selected_movie][asiento] = "Reservado"
        self.selected_seats = []
        self.load_seats()
        
        if all(v == "Reservado" for v in seating[self.selected_movie].values()):
            Clock.schedule_once(lambda dt: self.reiniciar_sala(), 15)
    
    def reiniciar_sala(self):
        seating = App.get_running_app().root.get_screen('movies').seating
        for asiento in seating[self.selected_movie]:
            seating[self.selected_movie][asiento] = "Disponible"
        self.load_seats()
        self.show_popup("Sala Reiniciada", "Todos los asientos están disponibles")
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        content.add_widget(Button(text='Cerrar', on_press=popup.dismiss))
        popup.open()

class FoodScreen(Screen):
    palomitas = NumericProperty(0)
    bebidas = NumericProperty(0)
    food_total = NumericProperty(0)
    
    def update_food(self, item, change):
        if item == 'palomitas':
            self.palomitas = max(0, self.palomitas + change)
        elif item == 'bebidas':
            self.bebidas = max(0, self.bebidas + change)
        self.update_total()
    
    def update_total(self):
        self.food_total = (self.palomitas * 5000) + (self.bebidas * 3000)
    
    def process_payment(self, payment_type):
        if self.food_total == 0:
            self.show_popup("Error", "No hay comida seleccionada")
            return
        
        content = PagoPopup(
            message=f"Total a pagar: ${self.food_total}",
            process_callback=lambda method: self.finalize_payment(method),
            payment_type=payment_type
        )
        popup = Popup(title="Método de Pago", content=content, size_hint=(0.8, 0.4))
        content.popup = popup
        popup.open()
    
    def finalize_payment(self, method):
        success = True
        if method == 'card':
            success = random.random() > 0.1
            
        if success:
            self.show_receipt(method, True)
            self.reset_food()
        else:
            self.show_receipt(method, False)
            self.show_popup("Error", "Pago con tarjeta fallido. Intente nuevamente.")
    
    def show_receipt(self, method, success):
        receipt_text = [
            "=== RECIBO DE COMIDA ===",
            f"Palomitas: {self.palomitas} x $5,000",
            f"Bebidas: {self.bebidas} x $3,000",
            f"Total: ${self.food_total}",
            f"Método de pago: {method.upper()}",
            f"Estado: {'APROBADO' if success else 'RECHAZADO'}",
            "Gracias por su compra!"
        ]
        receipt_screen = self.manager.get_screen('receipt')
        receipt_screen.receipt_text = '\n'.join(receipt_text)
        self.manager.current = 'receipt'
    
    def reset_food(self):
        self.palomitas = 0
        self.bebidas = 0
        self.update_total()
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        content.add_widget(Button(text='Cerrar', on_press=popup.dismiss))
        popup.open()

class PagoPopup(BoxLayout):
    message = StringProperty("")
    popup = ObjectProperty(None)
    
    def __init__(self, message, process_callback, payment_type, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.process_callback = process_callback
        self.payment_type = payment_type
    
    def process(self, method):
        self.popup.dismiss()
        if method == 'card':
            self.show_processing()
        else:
            self.process_callback(method)
    
    def show_processing(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Procesando pago..."))
        popup = Popup(title="Procesando Tarjeta", content=content, size_hint=(0.6, 0.4))
        popup.open()
        Clock.schedule_once(lambda dt: self.finish_payment(popup), 2)
    
    def finish_payment(self, popup):
        popup.dismiss()
        self.process_callback('card')

class ReceiptScreen(Screen):
    receipt_text = StringProperty("")

class CinemaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MovieScreen(name='movies'))
        sm.add_widget(SeatScreen(name='seats'))
        sm.add_widget(FoodScreen(name='food'))
        sm.add_widget(ReceiptScreen(name='receipt'))
        return sm

if __name__ == '__main__':
    CinemaApp().run()