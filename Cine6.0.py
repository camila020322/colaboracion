from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, DictProperty, ListProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import random
import io
import qrcode
from PIL import Image as PILImage

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
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.8, 0, 0, 1
                on_press: root.manager.current = 'main'

<TimeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Label:
            text: 'Selecciona un Horario para ' + root.selected_movie
            font_size: 30
            bold: True
            color: 0.9, 0.9, 0.9, 1
        GridLayout:
            cols: 1
            rows: 3
            spacing: 30
            padding: 30
            Button:
                text: root.times[0]
                font_size: 20
                on_press: root.select_time(root.times[0])
            Button:
                text: root.times[1]
                font_size: 20
                on_press: root.select_time(root.times[1])
            Button:
                text: root.times[2]
                font_size: 20
                on_press: root.select_time(root.times[2])
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.8, 0, 0, 1
                on_press: root.manager.current = 'movies'

<SeatScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: root.selected_movie + ' - ' + root.selected_time
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
                text: 'Aplicar Descuento'
                font_size: 20
                background_color: 0.5, 0, 0.8, 1
                on_press: root.show_discount_popup()
            Button:
                text: 'Comprar Comidas'
                font_size: 20
                background_color: 1, 0.5, 0, 1
                on_press: 
                    root.manager.get_screen('food').is_combined = True
                    root.manager.current = 'food'
            Button:
                text: 'Pagar'
                font_size: 20
                background_color: 0, 0.7, 0, 1
                on_press: root.process_payment('pelicula')
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.8, 0, 0, 1
                on_press: root.manager.current = 'time'

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
                text: 'Continuar' if root.is_combined else 'Pagar Comida'
                font_size: 20
                background_color: 0, 0.7, 0, 1
                on_press: root.handle_payment_or_continue()
            Button:
                text: 'Volver'
                font_size: 20
                background_color: 0.2, 0.6, 1, 1
                on_press: root.handle_back()

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

<DiscountPopup>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        Label:
            text: 'Ingrese código de descuento:'
            font_size: 18
        TextInput:
            id: discount_code
            multiline: False
            font_size: 18
            size_hint_y: 0.3
        BoxLayout:
            size_hint_y: 0.4
            spacing: 10
            Button:
                text: 'Aplicar'
                background_color: 0.2, 0.6, 1, 1
                on_press: root.apply_discount()
            Button:
                text: 'Cancelar'
                background_color: 0.8, 0, 0, 1
                on_press: root.dismiss()

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
                id: receipt_label
                text: root.receipt_text
                font_size: 20
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
            Image:
                id: qr_image
                size_hint_y: None
                height: 200
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
            self.seating[pelicula] = {
                "3:00 PM": {f"{row}{col}": "Disponible" for row in range(1, 11) for col in "ABCDEFGH"},
                "6:00 PM": {f"{row}{col}": "Disponible" for row in range(1, 11) for col in "ABCDEFGH"},
                "9:00 PM": {f"{row}{col}": "Disponible" for row in range(1, 11) for col in "ABCDEFGH"}
            }
    
    def select_movie(self, index):
        self.manager.get_screen('time').selected_movie = self.peliculas[index]
        self.manager.current = 'time'

class TimeScreen(Screen):
    times = ListProperty(["3:00 PM", "6:00 PM", "9:00 PM"])
    selected_movie = StringProperty("")

    def select_time(self, time):
        seats_screen = self.manager.get_screen('seats')
        seats_screen.selected_movie = self.selected_movie
        seats_screen.selected_time = time
        self.manager.current = 'seats'

class SeatScreen(Screen):
    selected_movie = StringProperty("")
    selected_time = StringProperty("")
    costo_asiento = NumericProperty(12000)
    costo_preferencial = NumericProperty(3000)
    selected_seats = ListProperty([])
    discount = NumericProperty(0)
    discount_code = StringProperty("")
    
    def on_pre_enter(self):
        self.load_seats()
        self.discount = 0
        self.discount_code = ""
    
    def load_seats(self):
        grid = self.ids.seats_grid
        grid.clear_widgets()
        
        if not self.selected_movie or not self.selected_time:
            return
            
        for row in range(1, 11):
            for col in "ABCDEFGH":
                asiento = f"{row}{col}"
                estado = App.get_running_app().root.get_screen('movies').seating[
                    self.selected_movie][self.selected_time][asiento]
                
                bg_color = (0.4, 0.8, 0.4, 1)
                if row == 1:
                    bg_color = (0.2, 0.6, 1, 1)
                
                if estado == "Reservado":
                    bg_color = (0.8, 0, 0, 1)
                
                btn = Button(
                    text=asiento,
                    background_color=bg_color,
                    disabled=(estado == "Reservado")
                )
                btn.bind(on_press=lambda instance, a=asiento: self.toggle_seat(a))
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
                    self.selected_movie][self.selected_time][child.text]
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
        subtotal = total + food_total
        discounted_total = subtotal * (1 - self.discount)
        return subtotal, discounted_total
    
    def show_discount_popup(self):
        content = DiscountPopup(apply_callback=self.apply_discount_callback)
        self.discount_popup = Popup(title="Aplicar Descuento", content=content, size_hint=(0.7, 0.4))
        content.popup = self.discount_popup
        self.discount_popup.open()
    
    def apply_discount_callback(self, code):
        valid_codes = {
            "VIP20": 0.2,
            "PELIS10": 0.1,
            "CINE30": 0.3
        }
        
        if code.upper() in valid_codes:
            self.discount = valid_codes[code.upper()]
            self.discount_code = code.upper()
            self.show_popup("Descuento Aplicado", f"Descuento del {int(self.discount*100)}% aplicado con éxito!")
        else:
            self.discount = 0
            self.discount_code = ""
            self.show_popup("Código Inválido", "El código de descuento no es válido")
    
    def process_payment(self, payment_type):
        if not self.selected_seats:
            self.show_popup("Error", "Selecciona al menos un asiento")
            return
        
        subtotal, total = self.calculate_total()
        message = f"Subtotal: ${subtotal:,.0f}\n"
        
        if self.discount > 0:
            message += f"Descuento ({self.discount_code}): -{self.discount*100:.0f}%\n"
            message += f"Total con descuento: ${total:,.0f}\n"
        else:
            message += f"Total: ${total:,.0f}\n"
        
        seats_str = ', '.join(self.selected_seats)
        message += f"Asientos comprados: {seats_str}\n"
        
        message += f"(Entradas: ${subtotal - App.get_running_app().root.get_screen('food').food_total:,.0f} | "
        message += f"Comida: ${App.get_running_app().root.get_screen('food').food_total:,.0f})"
        
        content = PagoPopup(
            message=message,
            process_callback=lambda method: self.finalize_payment(method, subtotal, total),
            payment_type=payment_type
        )
        popup = Popup(title="Método de Pago", content=content, size_hint=(0.8, 0.4))
        content.popup = popup
        popup.open()
    
    def finalize_payment(self, method, subtotal, total):
        success = True
        if method == 'card':
            success = random.random() > 0.1
        
        if success:
            self.completar_reserva()
            food_screen = App.get_running_app().root.get_screen('food')
            food_screen.reset_food()
            self.show_receipt(subtotal, total, method, True)
        else:
            self.show_receipt(subtotal, total, method, False)
            self.show_popup("Error", "Pago con tarjeta fallido. Intente nuevamente.")
    
    def show_receipt(self, subtotal, total, method, success):
        preferencial_seats = [s for s in self.selected_seats if s.startswith('1')]
        normal_seats = [s for s in self.selected_seats if not s.startswith('1')]
        preferencial_count = len(preferencial_seats)
        normal_count = len(normal_seats)
        
        preferencial_total = preferencial_count * self.costo_preferencial
        normal_total = normal_count * self.costo_asiento
        food_screen = App.get_running_app().root.get_screen('food')
        food_total = food_screen.food_total

        receipt_lines = [
            "=== RECIBO DE PAGO ===",
            f"Película: {self.selected_movie}",
            f"Horario: {self.selected_time}",
            "",
            "ASIENTOS COMPRADOS:",
        ]
        
        if preferencial_count > 0:
            receipt_lines.append(f"Preferencial (Fila 1): {preferencial_count} x ${self.costo_preferencial:,} = ${preferencial_total:,}")
            receipt_lines.extend([f"• {seat}" for seat in preferencial_seats])
        
        if normal_count > 0:
            receipt_lines.append(f"Normal: {normal_count} x ${self.costo_asiento:,} = ${normal_total:,}")
            receipt_lines.extend([f"• {seat}" for seat in normal_seats])
        
        receipt_lines.extend([
            "",
            "DETALLE COMIDAS:",
            f"Palomitas: {food_screen.palomitas} x $5,000",
            f"Bebidas: {food_screen.bebidas} x $3,000",
            f"Total comida: ${food_total:,}",
            "",
            "RESUMEN DE PAGO:",
            f"Subtotal entradas: ${preferencial_total + normal_total:,}",
            f"Subtotal comida: ${food_total:,}",
            f"Subtotal total: ${subtotal:,}"
        ])
        
        if self.discount > 0:
            receipt_lines.append(f"Descuento ({self.discount_code}): -{self.discount*100:.0f}%")
            receipt_lines.append(f"Total con descuento: ${total:,}")
        else:
            receipt_lines.append(f"Total general: ${total:,}")

        receipt_lines.extend([
            "",
            f"Método de pago: {method.upper()}",
            f"Estado: {'APROBADO' if success else 'RECHAZADO'}",
            "",
            "¡Gracias por su compra!"
        ])
        
        receipt_text = "\n".join(receipt_lines)
        
        # Guardamos selección para mostrar QR
        self._last_receipt_info = {
            "pelicula": self.selected_movie,
            "horario": self.selected_time,
            "asientos": ', '.join(self.selected_seats)
        }
        
        receipt_screen = self.manager.get_screen('receipt')
        receipt_screen.receipt_text = receipt_text
        
        # Generar QR
        qr_data = (f"Película: {self._last_receipt_info['pelicula']}\n"
                   f"Horario: {self._last_receipt_info['horario']}\n"
                   f"Asientos: {self._last_receipt_info['asientos']}")
        qr_img = qrcode.make(qr_data)
        buf = io.BytesIO()
        qr_img.save(buf, format='PNG')
        buf.seek(0)
        im = PILImage.open(buf)
        tex = self.pil_image_to_texture(im)
        
        qr_widget = receipt_screen.ids.qr_image
        qr_widget.texture = tex
        qr_widget.canvas.ask_update()
        
        self.manager.current = 'receipt'
    
    def pil_image_to_texture(self, pil_image):
        pil_image = pil_image.convert('RGBA')
        w, h = pil_image.size
        pixel_data = pil_image.tobytes()
        texture = Texture.create(size=(w, h))
        texture.blit_buffer(pixel_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture
    
    def completar_reserva(self):
        seating = App.get_running_app().root.get_screen('movies').seating
        for asiento in self.selected_seats:
            seating[self.selected_movie][self.selected_time][asiento] = "Reservado"
        self.selected_seats = []
        self.load_seats()
        self.discount = 0
        self.discount_code = ""
        
        if all(v == "Reservado" for v in seating[self.selected_movie][self.selected_time].values()):
            Clock.schedule_once(lambda dt: self.reiniciar_sala(), 15)
    
    def reiniciar_sala(self):
        seating = App.get_running_app().root.get_screen('movies').seating
        for asiento in seating[self.selected_movie][self.selected_time]:
            seating[self.selected_movie][self.selected_time][asiento] = "Disponible"
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
    is_combined = BooleanProperty(False)
    
    def update_food(self, item, change):
        if item == 'palomitas':
            self.palomitas = max(0, self.palomitas + change)
        elif item == 'bebidas':
            self.bebidas = max(0, self.bebidas + change)
        self.update_total()
    
    def update_total(self):
        self.food_total = (self.palomitas * 5000) + (self.bebidas * 3000)
    
    def handle_payment_or_continue(self):
        if self.is_combined:
            self.manager.current = 'seats'
        else:
            self.process_payment('comida')
    
    def handle_back(self):
        if self.is_combined:
            self.manager.current = 'seats'
        else:
            self.manager.current = 'main'
    
    def process_payment(self, payment_type):
        if self.food_total == 0:
            self.show_popup("Error", "No hay comida seleccionada")
            return
        
        content = PagoPopup(
            message=f"Total a pagar: ${self.food_total:,}",
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
            f"Total: ${self.food_total:,}",
            f"Método de pago: {method.upper()}",
            f"Estado: {'APROBADO' if success else 'RECHAZADO'}",
            "¡Gracias por su compra!"
        ]
        receipt_screen = self.manager.get_screen('receipt')
        receipt_screen.receipt_text = '\n'.join(receipt_text)
        
        # Clear QR image for food-only receipts:
        receipt_screen.ids.qr_image.texture = None
        
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

class DiscountPopup(BoxLayout):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(**kwargs)
        self.apply_callback = apply_callback
    
    def apply_discount(self):
        code = self.ids.discount_code.text
        self.apply_callback(code)
        self.popup.dismiss()

class ReceiptScreen(Screen):
    receipt_text = StringProperty("")

class CinemaApp(App):
    def build(self):
        Window.maximize()  # Abre la ventana maximizada al iniciar la app
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MovieScreen(name='movies'))
        sm.add_widget(TimeScreen(name='time'))
        sm.add_widget(SeatScreen(name='seats'))
        sm.add_widget(FoodScreen(name='food'))
        sm.add_widget(ReceiptScreen(name='receipt'))
        return sm

if __name__ == '__main__':
    CinemaApp().run()

