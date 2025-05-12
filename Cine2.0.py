from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, DictProperty, ListProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
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
        Button:
            text: 'Seleccionar Película'
            font_size: 24
            size_hint_y: 0.2
            background_color: 0.2, 0.6, 1, 1
            on_press: root.manager.current = 'movies'

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
                on_press: root.process_payment()
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.8, 0, 0, 1
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
    costo_asiento = 12000
    selected_seats = ListProperty([])
    
    def load_seats(self):
        grid = self.ids.seats_grid
        grid.clear_widgets()
        for row in range(1, 11):
            for col in "ABCDEFGH":
                asiento = f"{row}{col}"
                estado = App.get_running_app().root.get_screen('movies').seating[
                    self.selected_movie][asiento]
                btn = Button(
                    text=asiento,
                    background_color=(0.4, 0.8, 0.4, 1) if estado == "Disponible" else (0.8, 0, 0, 1),
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
                child.background_color = (0.4, 0.8, 0.4, 1) if estado == "Disponible" else (0.8, 0, 0, 1)
    
    def process_payment(self):
        if not self.selected_seats:
            self.show_popup("Error", "Selecciona al menos un asiento")
            return
        
        total = len(self.selected_seats) * self.costo_asiento
        content = PagoPopup(message=f"Total a pagar: ${total}", 
                          process_callback=self.completar_reserva)
        popup = Popup(title="Método de Pago", content=content,
                    size_hint=(0.8, 0.4))
        content.popup = popup
        popup.open()
    
    def completar_reserva(self):
        seating = App.get_running_app().root.get_screen('movies').seating
        for asiento in self.selected_seats:
            seating[self.selected_movie][asiento] = "Reservado"
        self.selected_seats = []
        self.load_seats()
        self.show_popup("Éxito", "Reserva completada con éxito!")
        
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
        popup = Popup(title=title, content=content,
                    size_hint=(0.6, 0.4))
        content.add_widget(Button(text='Cerrar', on_press=popup.dismiss))
        popup.open()

class PagoPopup(BoxLayout):
    message = StringProperty("")
    popup = ObjectProperty(None)
    
    def __init__(self, message, process_callback, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.process_callback = process_callback
    
    def process(self, method):
        self.popup.dismiss()
        if method == 'card':
            self.show_processing()
        else:
            self.process_callback()
    
    def show_processing(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Procesando pago..."))
        popup = Popup(title="Procesando Tarjeta", content=content,
                    size_hint=(0.6, 0.4))
        popup.open()
        Clock.schedule_once(lambda dt: self.finish_payment(popup), 2)
    
    def finish_payment(self, popup):
        popup.dismiss()
        self.process_callback()

class CinemaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MovieScreen(name='movies'))
        sm.add_widget(SeatScreen(name='seats'))
        return sm

if __name__ == '__main__':
    CinemaApp().run()